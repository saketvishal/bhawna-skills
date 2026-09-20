from __future__ import annotations

from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "htmlcov",
    ".tox",
}

SKIP_FILE_NAMES = {
    ".env",
    "credentials",
    "credentials.json",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

SKIP_SUFFIXES = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".jks",
}

SKIP_NAME_PARTS = ("secret", "token", "private")


def load_bhawna_ignore(root: Path) -> list[str]:
    path = root / ".bhawnaignore"
    if not path.is_file():
        return []
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def is_secret_or_generated(path: Path, root: Path, extra_ignore: list[str] | None = None) -> bool:
    rel = path.relative_to(root) if path.is_absolute() else path
    parts = set(rel.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    name = path.name
    if name in SKIP_FILE_NAMES or name.startswith(".env."):
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    lowered = name.lower()
    risky_suffix = path.suffix in {".txt", ".json", ".yml", ".yaml", ".pem", ".key"}
    if any(part in lowered for part in SKIP_NAME_PARTS) and risky_suffix:
        return True
    if name.endswith(".egg-info") or path.suffix == ".whl":
        return True
    for pattern in extra_ignore or []:
        if path.match(pattern) or rel.match(pattern):
            return True
    return False


def iter_safe_files(root: Path, extra_ignore: list[str] | None = None) -> list[Path]:
    files: list[Path] = []
    extra = extra_ignore if extra_ignore is not None else load_bhawna_ignore(root)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if is_secret_or_generated(path, root, extra):
            continue
        files.append(path)
    return files
