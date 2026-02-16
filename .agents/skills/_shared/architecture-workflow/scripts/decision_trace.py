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
MAJOR_DECISION_RE = re.compile(r"^MAJOR_DECISION:\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ymd() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def iso_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-") or "system"


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


def parse_markers(text: str) -> list[tuple[str, str, str]]:
    markers: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        m = MAJOR_DECISION_RE.match(line.strip())
        if m:
            markers.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return markers


def adr_index(decisions_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for adr in decisions_dir.glob("ADR-*.md"):
        slug = adr.stem.split("-", 2)[-1]
        out[slug] = str(adr)
        text = adr.read_text(encoding="utf-8")
        m = re.search(r"^decision_id:\s*\"?([^\n\"]+)\"?\s*$", text, re.M)
        if m:
            out[m.group(1).strip()] = str(adr)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate decision trace linking markers to ADRs.")
    parser.add_argument("--system")
    parser.add_argument("--date", help="YYYY-MM-DD")
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

    try:
        repo_root = resolve_repo_root(Path.cwd())
        arch_root = repo_root / "docs" / "architecture"
        reviews_dir = arch_root / "reviews"
        overviews_dir = arch_root / "solution-overviews"
        decisions_dir = arch_root / "decisions"

        overview = latest_file(overviews_dir, f"*{args.system}*.md")
        wa = latest_file(reviews_dir, f"WA-REVIEW-*-*{args.system}*.md")
        overview_text = overview.read_text(encoding="utf-8") if overview else ""
        wa_text = wa.read_text(encoding="utf-8") if wa else ""

        markers = parse_markers(overview_text) + parse_markers(wa_text)
        adrs = adr_index(decisions_dir)

        out_path = reviews_dir / f"DECISION-TRACE-{ymd()}-{slugify(args.system)}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Decision Trace\n",
            f"System: {args.system}\n",
            f"Date: {args.date or iso_date()}\n\n",
            "## Decision to ADR Mapping\n",
        ]
        if not markers:
            lines.append("No MAJOR_DECISION markers found.\n")
        else:
            for category, key, summary in markers:
                lines.append(f"- Category: {category}\n")
                lines.append(f"  Key: {key}\n")
                lines.append(f"  Summary: {summary}\n")
                lines.append(f"  ADR: {adrs.get(key, 'MISSING')}\n")
        out_path.write_text("".join(lines), encoding="utf-8")

        manifest_path = arch_root / "manifest" / f"{args.system}.yaml"
        manifest = load_manifest(manifest_path)
        ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
        manifest["decision_traces"].append(
            {
                "path": str(out_path),
                "timestamp": now_iso(),
            }
        )
        manifest["actions"].append(
            {
                "script": "decision_trace.py",
                "timestamp": now_iso(),
                "inputs": vars(args),
                "outputs": {"decision_trace_path": str(out_path), "marker_count": len(markers)},
                "exit_code": 0,
                "workflow_version": WORKFLOW_VERSION,
            }
        )
        save_manifest(manifest_path, manifest)

        print(str(out_path))
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
