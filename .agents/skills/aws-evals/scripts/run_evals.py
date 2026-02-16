#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_VERSION = "1.0.0"

SCENARIOS: dict[str, dict[str, str]] = {
    "associate": {
        "title": "Associate Gate",
        "prompt": (
            "Design a highly available 3-tier web application for a startup with 10x traffic spikes, "
            "p95 latency under 300ms, single-AZ failure tolerance, and backup/restore with RTO/RPO."
        ),
        "rubric": (
            "Pass only if multi-AZ resilience, data-store rationale, baseline security controls, "
            "recovery strategy, and explicit trade-offs are present."
        ),
    },
    "bridge": {
        "title": "Bridge Trade-off",
        "prompt": (
            "Compare synchronous relational architecture vs asynchronous event-driven architecture for order processing "
            "with <1s checkout acknowledgment and asynchronous fulfillment."
        ),
        "rubric": (
            "Pass only if latency, consistency, reliability, and operational trade-offs are explicit and "
            "a clear recommendation with risk controls is provided."
        ),
    },
    "professional": {
        "title": "Professional Gate",
        "prompt": (
            "Design multi-account enterprise architecture with OU guardrails, cross-account IAM, "
            "hub-and-spoke + hybrid connectivity, DR mapped to RTO/RPO, and cost governance controls."
        ),
        "rubric": (
            "Pass only if governance, network segmentation, DR strategy/testing, and FinOps ownership "
            "are explicit and auditable."
        ),
    },
    "failure": {
        "title": "Failure Analysis",
        "prompt": (
            "Analyze incident with 5xx spikes, latency surges, queue backlog growth, AZ dependency errors, "
            "and post-rollback reconciliation gaps."
        ),
        "rubric": (
            "Pass only if root-cause analysis, containment/recovery, reconciliation actions, and validation checks "
            "are explicit."
        ),
    },
}


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
            raise RuntimeError(
                "Could not resolve REPO_ROOT. Walked to filesystem root without finding .git/ or .agents/skills/."
            )
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
    m.setdefault("evals", [])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AWS architecture evaluation prompts and capture notes.")
    parser.add_argument(
        "--scenario",
        choices=["associate", "bridge", "professional", "failure", "all"],
        help="Evaluation scenario to run.",
    )
    parser.add_argument("--system", help="Optional system identifier for manifest logging.")
    parser.add_argument("--notes", help="Inline evaluator notes.")
    parser.add_argument("--notes-file", help="Path to file containing evaluator notes.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Allow prompts for missing values.",
    )
    args = parser.parse_args()

    if not args.scenario:
        if args.interactive:
            try:
                args.scenario = input("Scenario (associate|bridge|professional|failure|all): ").strip()
            except EOFError:
                args.scenario = ""
        if not args.scenario:
            print(
                "Error: missing --scenario. Use --scenario <value> or --interactive.",
                file=sys.stderr,
            )
            return None  # type: ignore[return-value]

    if args.scenario not in {"associate", "bridge", "professional", "failure", "all"}:
        print("Error: invalid scenario value.", file=sys.stderr)
        return None  # type: ignore[return-value]

    if not args.notes and not args.notes_file and not args.interactive:
        print(
            "Error: provide --notes or --notes-file for deterministic mode, or use --interactive.",
            file=sys.stderr,
        )
        return None  # type: ignore[return-value]

    return args


def collect_notes(args: argparse.Namespace, repo_root: Path) -> str:
    if args.notes:
        return args.notes.strip()
    if args.notes_file:
        p = Path(args.notes_file)
        if not p.is_absolute():
            p = (repo_root / p).resolve()
        if not p.exists():
            raise RuntimeError(f"Notes file not found: {p}")
        return p.read_text(encoding="utf-8").strip()
    if args.interactive:
        print("Enter evaluation notes, then submit EOF (Ctrl-D):")
        lines = sys.stdin.read().strip()
        if lines:
            return lines
    raise RuntimeError("No evaluation notes provided.")


def main() -> int:
    args = parse_args()
    if args is None:
        return 2

    try:
        repo_root = resolve_repo_root(Path.cwd())
        selected = list(SCENARIOS.keys()) if args.scenario == "all" else [args.scenario]
        notes = collect_notes(args, repo_root)

        reviews_dir = repo_root / "docs" / "architecture" / "reviews"
        reviews_dir.mkdir(parents=True, exist_ok=True)
        notes_path = reviews_dir / f"EVAL-NOTES-{today_ymd()}.md"

        lines = [
            f"# Evaluation Notes ({today_ymd()})",
            "",
            f"Generated: {now_iso()}",
            f"Workflow version: {WORKFLOW_VERSION}",
            f"Scenarios: {', '.join(selected)}",
            "",
        ]
        for key in selected:
            s = SCENARIOS[key]
            lines.extend(
                [
                    f"## {s['title']}",
                    "",
                    "### Prompt",
                    s["prompt"],
                    "",
                    "### Rubric",
                    s["rubric"],
                    "",
                ]
            )

        lines.extend(
            [
                "## Evaluator Notes",
                "",
                notes,
                "",
            ]
        )

        notes_path.write_text("\n".join(lines), encoding="utf-8")

        for key in selected:
            s = SCENARIOS[key]
            print(f"[{s['title']}]")
            print(f"Prompt: {s['prompt']}")
            print(f"Rubric: {s['rubric']}")
            print("")
        print(f"Wrote notes: {notes_path}")

        if args.system:
            manifest_path = repo_root / "docs" / "architecture" / "manifest" / f"{args.system}.yaml"
            manifest = load_manifest(manifest_path)
            ensure_common_manifest_keys(manifest, repo_root, manifest_path, args.system)
            manifest["evals"].append(
                {
                    "timestamp": now_iso(),
                    "scenarios": selected,
                    "notes_path": str(notes_path),
                }
            )
            manifest["actions"].append(
                {
                    "script": "run_evals.py",
                    "timestamp": now_iso(),
                    "inputs": {
                        "scenario": args.scenario,
                        "system": args.system,
                        "interactive": bool(args.interactive),
                        "notes_file": args.notes_file or "",
                        "has_notes_arg": bool(args.notes),
                    },
                    "outputs": {"notes_path": str(notes_path)},
                    "exit_code": 0,
                    "workflow_version": WORKFLOW_VERSION,
                }
            )
            save_manifest(manifest_path, manifest)
            print(f"Updated manifest: {manifest_path}")

        return 0
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except yaml.YAMLError:
        print("Error: existing manifest is not valid YAML content.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
