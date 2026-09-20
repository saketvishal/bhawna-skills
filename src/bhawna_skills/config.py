from __future__ import annotations

from pathlib import Path

import yaml

from .models import InvariantSet

BHAWNA_DIR = ".bhawna"
INVARIANTS_FILE = "invariants.yaml"
CONSTITUTION_FILE = "constitution.md"
DECISIONS_FILE = "decisions.yaml"
EXCEPTIONS_FILE = "exceptions.yaml"


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


def try_load_invariants(root: Path) -> InvariantSet:
    path = root / BHAWNA_DIR / INVARIANTS_FILE
    if not path.exists():
        return InvariantSet(project=root.name)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return InvariantSet.model_validate(data)


def save_invariants(root: Path, inv: InvariantSet) -> Path:
    path = root / BHAWNA_DIR / INVARIANTS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(inv.model_dump(mode="json"), sort_keys=False), encoding="utf-8")
    return path


def load_constitution(root: Path) -> str:
    path = root / BHAWNA_DIR / CONSTITUTION_FILE
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
