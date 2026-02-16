#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

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


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_manifest(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=True, default_flow_style=False),
        encoding="utf-8",
    )


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
        overviews_dir = arch_root / "solution-overviews"
        decisions_dir = arch_root / "decisions"
        manifest_path = arch_root / "manifest" / f"{args.system}.yaml"

        overview = overviews_dir / f"{args.system}.md"
        if not overview.exists():
            issues.append(
                f"Missing required solution overview: {overview}. "
                "Create docs/architecture/solution-overviews/<system>.md and rerun."
            )
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

        manifest = load_manifest(manifest_path)
        ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
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
