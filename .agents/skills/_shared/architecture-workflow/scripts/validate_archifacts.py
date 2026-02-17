#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

WORKFLOW_VERSION = "1.0.0"
PILLARS = [
    "Operational Excellence",
    "Security",
    "Reliability",
    "Performance Efficiency",
    "Cost Optimization",
    "Sustainability",
]
MAJOR_DECISION_RE = re.compile(r"^MAJOR_DECISION:\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$")


def fallback_yaml_dump(data: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key in sorted(data.keys()):
            value = data[key]
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(fallback_yaml_dump(value, indent + 2))
            else:
                if value is None:
                    rendered = "null"
                elif isinstance(value, bool):
                    rendered = "true" if value else "false"
                elif isinstance(value, (int, float)):
                    rendered = str(value)
                else:
                    text = str(value).replace('"', '\\"')
                    rendered = f"\"{text}\""
                lines.append(f"{pad}{key}: {rendered}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(fallback_yaml_dump(item, indent + 2))
            else:
                if item is None:
                    rendered = "null"
                elif isinstance(item, bool):
                    rendered = "true" if item else "false"
                elif isinstance(item, (int, float)):
                    rendered = str(item)
                else:
                    text = str(item).replace('"', '\\"')
                    rendered = f"\"{text}\""
                lines.append(f"{pad}- {rendered}")
        return "\n".join(lines)
    if data is None:
        return f"{pad}null"
    if isinstance(data, bool):
        return f"{pad}{'true' if data else 'false'}"
    if isinstance(data, (int, float)):
        return f"{pad}{data}"
    text = str(data).replace('"', '\\"')
    return f"{pad}\"{text}\""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_repo_root(path: Path) -> bool:
    return (path / ".git").exists() or (path / ".agents" / "skills").exists()


def resolve_repo_root(start: Path) -> Path:
    cur = start.resolve()
    while True:
        if is_repo_root(cur):
            return cur
        if cur.parent == cur:
            raise RuntimeError("Could not resolve REPO_ROOT; .git/ or .agents/skills/ was not found.")
        cur = cur.parent


def resolve_manifest_path(repo_root: Path, system: str) -> Path:
    return Path(os.path.join(repo_root, f"{system}.yaml"))


def migrate_legacy_manifest(repo_root: Path, system: str) -> str | None:
    manifest_path = resolve_manifest_path(repo_root, system)
    legacy_manifest_path = repo_root / "docs" / "architecture" / "manifest" / f"{system}.yaml"
    if legacy_manifest_path.exists() and not manifest_path.exists():
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(legacy_manifest_path, manifest_path)
        return str(legacy_manifest_path)
    return None


def normalize_manifest(m: Any) -> dict[str, Any]:
    manifest = m if isinstance(m, dict) else {}
    if not isinstance(manifest.get("adrs"), list):
        manifest["adrs"] = []
    if not isinstance(manifest.get("wa_reviews"), list):
        manifest["wa_reviews"] = []
    if not isinstance(manifest.get("validations"), list):
        manifest["validations"] = []
    if not isinstance(manifest.get("decision_traces"), list):
        manifest["decision_traces"] = []
    if not isinstance(manifest.get("actions"), list):
        manifest["actions"] = []
    if not isinstance(manifest.get("artifacts"), dict):
        manifest["artifacts"] = {}
    return manifest


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(text)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def save_manifest(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml is None:
        content = fallback_yaml_dump(data) + "\n"
    else:
        content = yaml.safe_dump(data, sort_keys=True, default_flow_style=False)
    path.write_text(content, encoding="utf-8")


def ensure_common_manifest_keys(m: dict[str, Any], repo_root: Path, manifest_path: Path, system: str) -> None:
    m.setdefault("system", system)
    m["manifest_path"] = str(manifest_path)
    m["repo_root"] = str(repo_root)
    m["workflow_version"] = WORKFLOW_VERSION
    m["last_updated"] = now_iso()
    m.setdefault("artifacts", {})
    m.setdefault("adrs", [])
    m.setdefault("wa_reviews", [])
    m.setdefault("validations", [])
    m.setdefault("decision_traces", [])
    m.setdefault("actions", [])


def latest_file(path: Path, pattern: str) -> Path | None:
    files = sorted(path.glob(pattern), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def parse_scores(wa_text: str) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    scores: dict[str, str] = {}
    for pillar in PILLARS:
        section = re.search(rf"^##\s+{re.escape(pillar)}\s*$", wa_text, re.M)
        if not section:
            issues.append(f"Missing WA pillar section: {pillar}")
            continue
        following = wa_text[section.end() :]
        next_section = re.search(r"^##\s+", following, re.M)
        chunk = following[: next_section.start()] if next_section else following
        score_match = re.search(r"^Score:\s*(Pass|Needs Work|Fail)\s*$", chunk, re.M)
        if not score_match:
            issues.append(f"Missing score for pillar: {pillar}")
            continue
        scores[pillar] = score_match.group(1)
    return scores, issues


def parse_major_decisions(*texts: str) -> tuple[list[tuple[str, str, str]], list[str]]:
    markers: list[tuple[str, str, str]] = []
    issues: list[str] = []
    for text in texts:
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("MAJOR_DECISION:"):
                continue
            m = MAJOR_DECISION_RE.match(line)
            if not m:
                issues.append(f"Invalid MAJOR_DECISION grammar: {line}")
                continue
            markers.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return markers, issues


def adr_keys(decisions_dir: Path) -> set[str]:
    keys: set[str] = set()
    for adr in decisions_dir.glob("ADR-*.md"):
        slug = adr.stem.split("-", 2)[-1]
        keys.add(slug)
        text = adr.read_text(encoding="utf-8")
        m = re.search(r"^decision_id:\s*\"?([^\n\"]+)\"?\s*$", text, re.M)
        if m:
            keys.add(m.group(1).strip())
    return keys


def required_baseline_paths(arch_root: Path, system: str) -> dict[str, Path]:
    return {
        "solution_overview": arch_root / "solution-overviews" / f"{system}.md",
        "threat_model_lite": arch_root / "threat-models" / f"{system}-threat-model-lite.md",
        "runbook_baseline": arch_root / "runbooks" / f"{system}-runbook-baseline.md",
        "diagram_context": arch_root / "diagrams" / f"{system}-context.md",
        "diagram_containers": arch_root / "diagrams" / f"{system}-containers.md",
        "diagram_dataflow": arch_root / "diagrams" / f"{system}-dataflow.md",
        "diagram_network": arch_root / "diagrams" / f"{system}-network.md",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate architecture artifacts and WA gating.")
    parser.add_argument("--system")
    parser.add_argument("--max-needs-work", type=int, default=2)
    parser.add_argument("--allow-fail-pillars", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()

    if not args.system:
        if args.interactive:
            try:
                args.system = input("system: ").strip()
            except EOFError:
                args.system = ""
        if not args.system:
            print("Error: missing --system. Use --interactive for prompt mode.", file=sys.stderr)
            parser.print_usage(sys.stderr)
            return 2

    exit_code = 0
    issues: list[str] = []

    try:
        repo_root = resolve_repo_root(Path.cwd())
        arch_root = repo_root / "docs" / "architecture"
        reviews_dir = arch_root / "reviews"
        decisions_dir = arch_root / "decisions"
        manifest_path = resolve_manifest_path(repo_root, args.system)
        migrated_manifest_from = migrate_legacy_manifest(repo_root, args.system)

        baseline = required_baseline_paths(arch_root, args.system)
        for label, path in baseline.items():
            if not path.exists():
                issues.append(
                    f"Missing required baseline artifact ({label}): {path}. "
                    "Run init_arch_workflow.py --system <system> to create it."
                )

        overview = baseline["solution_overview"]
        if not overview.exists():
            overview_text = ""
        else:
            overview_text = overview.read_text(encoding="utf-8")

        wa = latest_file(reviews_dir, f"WA-REVIEW-*-*{args.system}*.md")
        if not wa:
            issues.append(f"Missing WA review for system '{args.system}' in {reviews_dir}")
            wa_text = ""
            scores = {}
        else:
            wa_text = wa.read_text(encoding="utf-8")
            scores, score_issues = parse_scores(wa_text)
            issues.extend(score_issues)

        fail_count = sum(1 for v in scores.values() if v == "Fail")
        nw_count = sum(1 for v in scores.values() if v == "Needs Work")
        if fail_count > 0 and not args.allow_fail_pillars:
            issues.append("Gate failure: at least one pillar is Fail. Use --allow-fail-pillars to override.")
        if nw_count > args.max_needs_work:
            issues.append(
                f"Gate failure: Needs Work count ({nw_count}) exceeds max ({args.max_needs_work})."
            )

        markers, marker_issues = parse_major_decisions(overview_text, wa_text)
        issues.extend(marker_issues)

        keys = adr_keys(decisions_dir)
        for category, key, summary in markers:
            if key not in keys:
                issues.append(
                    f"Missing ADR mapping for MAJOR_DECISION key '{key}' ({category} | {summary})."
                )

        result = "pass" if not issues else "fail"
        if issues:
            exit_code = 1

        manifest = normalize_manifest(load_manifest(manifest_path))
        ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
        manifest["artifacts"].setdefault("baseline_doc_pack", {})
        manifest["artifacts"]["baseline_doc_pack"].update(
            {
                "solution_overview": str(baseline["solution_overview"]),
                "threat_model_lite": str(baseline["threat_model_lite"]),
                "runbook_baseline": str(baseline["runbook_baseline"]),
                "diagrams": {
                    "context": str(baseline["diagram_context"]),
                    "containers": str(baseline["diagram_containers"]),
                    "dataflow": str(baseline["diagram_dataflow"]),
                    "network": str(baseline["diagram_network"]),
                },
            }
        )
        manifest["validations"].append(
            {
                "timestamp": now_iso(),
                "result": result,
                "issues": issues,
                "gate": {
                    "allow_fail_pillars": bool(args.allow_fail_pillars),
                    "max_needs_work": int(args.max_needs_work),
                },
            }
        )
        manifest["actions"].append(
            {
                "script": "validate_archifacts.py",
                "timestamp": now_iso(),
                "inputs": vars(args),
                "outputs": {"result": result, "issues_count": len(issues)},
                "exit_code": exit_code,
                "workflow_version": WORKFLOW_VERSION,
            }
        )
        if migrated_manifest_from:
            manifest["actions"][-1]["migrated_manifest_from"] = migrated_manifest_from
        save_manifest(manifest_path, manifest)

        if issues:
            print("Validation failed with actionable issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
        else:
            print("Validation passed.")

        return exit_code
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
