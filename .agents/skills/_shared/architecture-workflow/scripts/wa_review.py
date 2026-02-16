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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Well-Architected review from shared template.")
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
        template_path = (
            repo_root
            / ".agents"
            / "skills"
            / "_shared"
            / "architecture-workflow"
            / "templates"
            / "well-architected-review.md"
        )
        if not template_path.exists():
            raise RuntimeError(f"Template file not found: {template_path}")

        out_dir = repo_root / "docs" / "architecture" / "reviews"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"WA-REVIEW-{ymd()}-{slugify(args.system)}.md"

        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{system}}", args.system)
        content = content.replace("{{date}}", args.date or iso_date())
        content = content.replace("{{reviewers}}", "TBD")
        out_path.write_text(content, encoding="utf-8")

        manifest_path = repo_root / "docs" / "architecture" / "manifest" / f"{args.system}.yaml"
        manifest = load_manifest(manifest_path)
        ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
        manifest["wa_reviews"].append(
            {
                "path": str(out_path),
                "date": args.date or iso_date(),
            }
        )
        manifest["actions"].append(
            {
                "script": "wa_review.py",
                "timestamp": now_iso(),
                "inputs": vars(args),
                "outputs": {"wa_review_path": str(out_path)},
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
