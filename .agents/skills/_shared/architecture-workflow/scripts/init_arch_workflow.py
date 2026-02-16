#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_VERSION = "1.0.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_repo_root(path: Path) -> bool:
    return (path / ".git").exists() or (path / ".agents" / "skills").exists()


def resolve_repo_root(start: Path) -> Path:
    cur = start.resolve()
    while True:
        if is_repo_root(cur):
            return cur
        if cur.parent == cur:
            raise RuntimeError(
                "Could not resolve REPO_ROOT. Walked to filesystem root without finding .git/ or .agents/skills/."
            )
        cur = cur.parent


def ensure_architecture_dirs(repo_root: Path) -> dict[str, str]:
    base = repo_root / "docs" / "architecture"
    required = {
        "decisions": base / "decisions",
        "reviews": base / "reviews",
        "diagrams": base / "diagrams",
        "threat-models": base / "threat-models",
        "runbooks": base / "runbooks",
        "solution-overviews": base / "solution-overviews",
        "manifest": base / "manifest",
    }
    for path in required.values():
        path.mkdir(parents=True, exist_ok=True)
    return {k: str(v) for k, v in required.items()}


def ensure_index(repo_root: Path) -> str:
    index_path = repo_root / "docs" / "architecture" / "index.md"
    lines = [
        "# Architecture Index\n",
        "\n",
        "- Decisions: `docs/architecture/decisions/`\n",
        "- Reviews: `docs/architecture/reviews/`\n",
        "- Diagrams: `docs/architecture/diagrams/`\n",
        "- Threat Models: `docs/architecture/threat-models/`\n",
        "- Runbooks: `docs/architecture/runbooks/`\n",
        "- Solution Overviews: `docs/architecture/solution-overviews/`\n",
        "- Manifest: `docs/architecture/manifest/`\n",
    ]
    if not index_path.exists():
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text("".join(lines), encoding="utf-8")
    else:
        existing = index_path.read_text(encoding="utf-8")
        for line in lines[2:]:
            if line.strip() not in existing:
                existing += line
        index_path.write_text(existing, encoding="utf-8")
    return str(index_path)


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise RuntimeError(f"Manifest at {path} must be a mapping/object.")
        return data
    except yaml.YAMLError:
        raise RuntimeError(
            f"Manifest at {path} is not parseable YAML content. "
            "Fix or remove it, then rerun."
        )


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(manifest, sort_keys=True, default_flow_style=False),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize docs/architecture workflow folders and canonical manifest."
    )
    parser.add_argument("--system", help="System identifier used for manifest naming.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enable prompt mode if required args are missing.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.system:
        if args.interactive:
            try:
                args.system = input("System identifier: ").strip()
            except EOFError:
                args.system = ""
        if not args.system:
            print(
                "Error: missing required argument --system. "
                "Run with --system <name> or add --interactive for prompt mode.",
                file=sys.stderr,
            )
            return 2

    try:
        repo_root = resolve_repo_root(Path.cwd())
        dirs = ensure_architecture_dirs(repo_root)
        index_path = ensure_index(repo_root)

        manifest_path = repo_root / "docs" / "architecture" / "manifest" / f"{args.system}.yaml"
        manifest = load_manifest(manifest_path)

        manifest.setdefault("system", args.system)
        manifest["manifest_path"] = str(manifest_path)
        manifest["repo_root"] = str(repo_root)
        manifest["workflow_version"] = WORKFLOW_VERSION
        manifest["last_updated"] = utc_now()
        manifest.setdefault("artifacts", {})
        manifest.setdefault("adrs", [])
        manifest.setdefault("wa_reviews", [])
        manifest.setdefault("validations", [])
        manifest.setdefault("decision_traces", [])
        manifest.setdefault("actions", [])

        manifest["artifacts"].update(
            {
                "index": index_path,
                "decisions_dir": dirs["decisions"],
                "reviews_dir": dirs["reviews"],
                "diagrams_dir": dirs["diagrams"],
                "threat_models_dir": dirs["threat-models"],
                "runbooks_dir": dirs["runbooks"],
                "solution_overviews_dir": dirs["solution-overviews"],
                "manifest_dir": dirs["manifest"],
            }
        )

        manifest["actions"].append(
            {
                "script": "init_arch_workflow.py",
                "timestamp": utc_now(),
                "inputs": {"system": args.system, "interactive": bool(args.interactive)},
                "outputs": {
                    "index_path": index_path,
                    "manifest_path": str(manifest_path),
                },
                "exit_code": 0,
                "workflow_version": WORKFLOW_VERSION,
            }
        )

        write_manifest(manifest_path, manifest)
        print(f"Initialized architecture workflow for system '{args.system}'.")
        print(f"Manifest: {manifest_path}")
        return 0
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
