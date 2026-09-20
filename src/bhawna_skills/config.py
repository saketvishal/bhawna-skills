from __future__ import annotations

from pathlib import Path

import yaml

from .models import InvariantSet

BHAWNA_DIR = ".bhawna"
INVARIANTS_FILE = "invariants.yaml"
CONSTITUTION_FILE = "constitution.md"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / BHAWNA_DIR).is_dir():
            return candidate
    return current


def load_invariants(root: Path) -> InvariantSet:
    path = root / BHAWNA_DIR / INVARIANTS_FILE
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run `bhawna init` first.")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return InvariantSet.model_validate(data)


def load_constitution(root: Path) -> str:
    path = root / BHAWNA_DIR / CONSTITUTION_FILE
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
