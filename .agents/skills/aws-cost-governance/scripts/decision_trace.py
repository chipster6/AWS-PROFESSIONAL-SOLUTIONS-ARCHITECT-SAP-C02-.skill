#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ALLOWED = {
    "init_arch_workflow.py",
    "new_adr.py",
    "wa_review.py",
    "validate_archifacts.py",
    "decision_trace.py",
}


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


def resolve_python_command(repo_root: Path) -> Path | str:
    venv_python = repo_root / ".venv" / "bin" / "python"
    return venv_python if venv_python.exists() else "python3"


def main() -> int:
    script_name = Path(__file__).name
    if script_name not in ALLOWED:
        print(
            f"Error: wrapper script '{script_name}' is not in allowed dispatch set: {sorted(ALLOWED)}",
            file=sys.stderr,
        )
        return 1
    try:
        repo_root = resolve_repo_root(Path.cwd())
        shared = (
            repo_root
            / ".agents"
            / "skills"
            / "_shared"
            / "architecture-workflow"
            / "scripts"
            / script_name
        )
        if not shared.exists():
            print(f"Error: shared script not found: {shared}", file=sys.stderr)
            return 1
        proc = subprocess.run(
            [str(resolve_python_command(repo_root)), str(shared), *sys.argv[1:]],
            check=False,
        )
        return proc.returncode
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
