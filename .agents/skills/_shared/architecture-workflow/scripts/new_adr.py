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


def today_ymd() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


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


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-") or "decision"


def parse_csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


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
    parser = argparse.ArgumentParser(description="Create ADR and update docs/architecture manifest.")
    parser.add_argument("--system")
    parser.add_argument("--title")
    parser.add_argument("--category")
    parser.add_argument("--status")
    parser.add_argument("--owners", help="Comma-separated owners")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--slug")
    parser.add_argument("--date", help="YYYY-MM-DD")
    parser.add_argument("--supersedes", default="")
    parser.add_argument("--superseded-by", default="")
    parser.add_argument("--template", choices=["short", "full"], default="full")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()

    required = ["system", "title", "category", "status", "owners", "tags"]
    missing = [name for name in required if not getattr(args, name)]

    if missing and not args.interactive:
        print(
            "Error: missing required args: "
            + ", ".join(f"--{m}" for m in missing)
            + ". Use --interactive to provide prompts.",
            file=sys.stderr,
        )
        parser.print_usage(sys.stderr)
        return 2

    if missing and args.interactive:
        for key in missing:
            try:
                setattr(args, key, input(f"{key}: ").strip())
            except EOFError:
                setattr(args, key, "")
        remaining = [name for name in required if not getattr(args, name)]
        if remaining:
            print("Error: required values still missing after interactive prompts.", file=sys.stderr)
            return 2

    try:
        repo_root = resolve_repo_root(Path.cwd())
        manifest_path = repo_root / "docs" / "architecture" / "manifest" / f"{args.system}.yaml"
        decisions_dir = repo_root / "docs" / "architecture" / "decisions"
        index_path = repo_root / "docs" / "architecture" / "index.md"
        template_path = (
            repo_root
            / ".agents"
            / "skills"
            / "_shared"
            / "architecture-workflow"
            / "templates"
            / f"adr-{args.template}.md"
        )

        if not template_path.exists():
            raise RuntimeError(f"Template file not found: {template_path}")

        decisions_dir.mkdir(parents=True, exist_ok=True)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)

        adr_slug = args.slug or slugify(args.title)
        decision_id = adr_slug
        date_display = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        adr_name = f"ADR-{today_ymd()}-{adr_slug}.md"
        adr_path = decisions_dir / adr_name

        owners = parse_csv(args.owners)
        tags = parse_csv(args.tags)
        if not owners:
            raise RuntimeError("No owners provided after parsing --owners.")
        if not tags:
            raise RuntimeError("No tags provided after parsing --tags.")

        template = template_path.read_text(encoding="utf-8")
        replacements = {
            "{{decision_id}}": decision_id,
            "{{system}}": args.system,
            "{{category}}": args.category,
            "{{status}}": args.status,
            "{{owner}}": owners[0],
            "{{date}}": date_display,
            "{{tag}}": tags[0],
            "{{title}}": args.title,
            "{{context}}": "Describe business and technical context.",
            "{{decision}}": "Describe the selected decision clearly.",
            "{{alternative_1}}": "Alternative 1",
            "{{alternative_2}}": "Alternative 2",
            "{{consequence_1}}": "Consequence 1",
            "{{consequence_2}}": "Consequence 2",
            "{{security_notes}}": "Security/compliance implications.",
            "{{cost_notes}}": "Cost implications.",
            "{{operational_notes}}": "Operational implications.",
            "{{reference_1}}": "Reference 1",
            "{{reference_2}}": "Reference 2",
            "{{problem_statement}}": "Problem statement.",
            "{{background}}": "Background.",
            "{{constraint_1}}": "Constraint 1",
            "{{constraint_2}}": "Constraint 2",
            "{{selected_option}}": "Selected option.",
            "{{rationale_1}}": "Rationale 1",
            "{{rationale_2}}": "Rationale 2",
            "{{option_a}}": "Option A",
            "{{option_b}}": "Option B",
            "{{positive_1}}": "Positive impact 1",
            "{{positive_2}}": "Positive impact 2",
            "{{negative_1}}": "Negative impact 1",
            "{{negative_2}}": "Negative impact 2",
        }
        for key, value in replacements.items():
            template = template.replace(key, value)

        template = template.replace('supersedes: ""', f'supersedes: "{args.supersedes}"')
        template = template.replace('superseded_by: ""', f'superseded_by: "{args.superseded_by}"')

        # Replace single-item placeholders with full lists.
        template = re.sub(
            r"owners:\n\s+-\s+\".*?\"",
            "owners:\n" + "\n".join(f'  - "{o}"' for o in owners),
            template,
            count=1,
        )
        template = re.sub(
            r"tags:\n\s+-\s+\".*?\"",
            "tags:\n" + "\n".join(f'  - "{t}"' for t in tags),
            template,
            count=1,
        )

        adr_path.write_text(template, encoding="utf-8")

        if not index_path.exists():
            index_path.write_text("# Architecture Index\n\n", encoding="utf-8")
        idx = index_path.read_text(encoding="utf-8")
        idx_line = f"- ADR: `docs/architecture/decisions/{adr_name}`\n"
        if idx_line not in idx:
            idx += idx_line
            index_path.write_text(idx, encoding="utf-8")

        manifest = load_manifest(manifest_path)
        ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
        manifest["adrs"].append(
            {
                "decision_id": decision_id,
                "slug": adr_slug,
                "category": args.category,
                "status": args.status,
                "owners": owners,
                "date": date_display,
                "path": str(adr_path),
            }
        )
        manifest["actions"].append(
            {
                "script": "new_adr.py",
                "timestamp": now_iso(),
                "inputs": vars(args),
                "outputs": {"adr_path": str(adr_path), "index_path": str(index_path)},
                "exit_code": 0,
                "workflow_version": WORKFLOW_VERSION,
            }
        )
        save_manifest(manifest_path, manifest)

        print(str(adr_path))
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
