#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
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


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def ensure_file(
    path: Path,
    content: str,
    *,
    force: bool,
    force_overwrite_allowed: bool,
) -> str:
    if path.exists():
        if force and force_overwrite_allowed:
            path.write_text(content, encoding="utf-8")
            return "overwritten"
        return "exists"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "created"


def baseline_doc_pack(
    repo_root: Path,
    system: str,
    *,
    force: bool,
) -> tuple[dict[str, str], dict[str, list[str]]]:
    arch = repo_root / "docs" / "architecture"
    templates = repo_root / ".agents" / "skills" / "_shared" / "architecture-workflow" / "templates"
    required_templates = {
        "solution": templates / "solution-overview.md",
        "threat": templates / "threat-model-lite.md",
        "runbook": templates / "runbook-baseline.md",
    }
    for key, template_path in required_templates.items():
        if not template_path.exists():
            raise RuntimeError(f"Missing required template '{key}': {template_path}")

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    replacements = {
        "system": system,
        "date": date,
        "owners": "TBD",
    }

    paths = {
        "solution_overview": arch / "solution-overviews" / f"{system}.md",
        "threat_model_lite": arch / "threat-models" / f"{system}-threat-model-lite.md",
        "runbook_baseline": arch / "runbooks" / f"{system}-runbook-baseline.md",
        "diagram_context": arch / "diagrams" / f"{system}-context.md",
        "diagram_containers": arch / "diagrams" / f"{system}-containers.md",
        "diagram_dataflow": arch / "diagrams" / f"{system}-dataflow.md",
        "diagram_network": arch / "diagrams" / f"{system}-network.md",
    }

    states = {"created": [], "exists": [], "overwritten": []}

    solution_state = ensure_file(
        paths["solution_overview"],
        render_template(required_templates["solution"], replacements),
        force=force,
        force_overwrite_allowed=True,
    )
    states[solution_state].append(str(paths["solution_overview"]))

    threat_state = ensure_file(
        paths["threat_model_lite"],
        render_template(required_templates["threat"], replacements),
        force=force,
        force_overwrite_allowed=True,
    )
    states[threat_state].append(str(paths["threat_model_lite"]))

    runbook_state = ensure_file(
        paths["runbook_baseline"],
        render_template(required_templates["runbook"], replacements),
        force=force,
        force_overwrite_allowed=True,
    )
    states[runbook_state].append(str(paths["runbook_baseline"]))

    diagram_placeholders = {
        "diagram_context": "# Diagram Placeholder: Context\n\nDefine system context, external actors, and trust boundaries.\n",
        "diagram_containers": "# Diagram Placeholder: Containers\n\nDefine runtime containers/services and key interactions.\n",
        "diagram_dataflow": "# Diagram Placeholder: Data Flow\n\nDefine primary data paths, stores, and transformation boundaries.\n",
        "diagram_network": "# Diagram Placeholder: Network\n\nDefine VPC/VNet topology, subnets, routing, and ingress/egress controls.\n",
    }
    for key, content in diagram_placeholders.items():
        state = ensure_file(
            paths[key],
            content,
            force=force,
            force_overwrite_allowed=False,
        )
        states[state].append(str(paths[key]))

    return {k: str(v) for k, v in paths.items()}, states


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        # No YAML parser available in runtime: preserve deterministic behavior
        # by treating non-empty manifests as opaque and starting a fresh mapping.
        return {}
    try:
        data = yaml.safe_load(text)
    except Exception as exc:
        raise RuntimeError(f"Manifest at {path} is not parseable YAML content: {exc}")
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Manifest at {path} must be a mapping/object.")
    return data


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml is None:
        content = fallback_yaml_dump(manifest) + "\n"
    else:
        content = yaml.safe_dump(manifest, sort_keys=True, default_flow_style=False)
    path.write_text(content, encoding="utf-8")


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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite template-derived baseline files (solution overview, threat model, runbook).",
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
        baseline_paths, baseline_states = baseline_doc_pack(repo_root, args.system, force=bool(args.force))

        manifest_path = resolve_manifest_path(repo_root, args.system)
        migrated_manifest_from = migrate_legacy_manifest(repo_root, args.system)
        manifest = normalize_manifest(load_manifest(manifest_path))

        manifest.setdefault("system", args.system)
        manifest["manifest_path"] = str(manifest_path)
        manifest["repo_root"] = str(repo_root)
        manifest["workflow_version"] = WORKFLOW_VERSION
        manifest["last_updated"] = utc_now()

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
        manifest["artifacts"]["baseline_doc_pack"] = {
            "solution_overview": baseline_paths["solution_overview"],
            "threat_model_lite": baseline_paths["threat_model_lite"],
            "runbook_baseline": baseline_paths["runbook_baseline"],
            "diagrams": {
                "context": baseline_paths["diagram_context"],
                "containers": baseline_paths["diagram_containers"],
                "dataflow": baseline_paths["diagram_dataflow"],
                "network": baseline_paths["diagram_network"],
            },
        }

        manifest["actions"].append(
            {
                "script": "init_arch_workflow.py",
                "timestamp": utc_now(),
                "inputs": {
                    "system": args.system,
                    "interactive": bool(args.interactive),
                    "force": bool(args.force),
                },
                "outputs": {
                    "index_path": index_path,
                    "manifest_path": str(manifest_path),
                    "baseline_doc_pack": baseline_paths,
                    "baseline_created": baseline_states["created"],
                    "baseline_existing": baseline_states["exists"],
                    "baseline_overwritten": baseline_states["overwritten"],
                },
                "exit_code": 0,
                "workflow_version": WORKFLOW_VERSION,
            }
        )
        if migrated_manifest_from:
            manifest["actions"][-1]["migrated_manifest_from"] = migrated_manifest_from

        write_manifest(manifest_path, manifest)
        print(f"Initialized architecture workflow for system '{args.system}'.")
        print(f"Manifest: {manifest_path}")
        print(f"Baseline created: {len(baseline_states['created'])}")
        print(f"Baseline existing: {len(baseline_states['exists'])}")
        print(f"Baseline overwritten: {len(baseline_states['overwritten'])}")
        return 0
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
