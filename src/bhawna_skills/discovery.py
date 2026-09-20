from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_loader import load_signals
from .models import DiscoveryFact, DiscoveryReport
from .secretscan import is_secret_or_generated, load_bhawna_ignore

MANIFEST_NAMES = {
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "Cargo.toml",
    "go.mod",
    "requirements.txt",
    "Pipfile",
    "composer.json",
    "Gemfile",
    "build.gradle",
    "pom.xml",
    "Package.swift",
}


def _read_if_allowed(path: Path, root: Path, extra: list[str]) -> str | None:
    if is_secret_or_generated(path, root, extra):
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _collect_manifest_text(root: Path, extra: list[str]) -> str:
    chunks: list[str] = []
    for name in MANIFEST_NAMES:
        path = root / name
        if path.is_file():
            text = _read_if_allowed(path, root, extra)
            if text:
                chunks.append(text.lower())
    return "\n".join(chunks)


def discover(root: Path, signals: list[dict[str, Any]] | None = None) -> DiscoveryReport:
    extra = load_bhawna_ignore(root)
    skipped: list[str] = []
    if (root / ".env").exists():
        skipped.append(".env")
    facts: list[DiscoveryFact] = []
    dimensions: set[str] = set()
    manifest = _collect_manifest_text(root, extra)
    configured = signals if signals is not None else load_signals()

    for signal in configured:
        sid = str(signal["id"])
        kind = str(signal.get("kind", "file"))
        dims = list(signal.get("dimensions", []))
        matched = False
        detail = ""
        if kind == "file":
            rel = str(signal["path"])
            path = root / rel
            if path.exists() and not is_secret_or_generated(path, root, extra):
                matched = True
                detail = rel
            elif path.exists():
                skipped.append(rel)
        elif kind == "glob":
            pattern = str(signal["pattern"])
            hits = [
                p
                for p in root.glob(pattern)
                if p.is_file() and not is_secret_or_generated(p, root, extra)
            ]
            if hits:
                matched = True
                detail = f"{pattern} ({len(hits)})"
        elif kind == "dir":
            rel = str(signal["path"])
            if (root / rel).is_dir():
                matched = True
                detail = rel
        elif kind == "token":
            tokens = [str(t).lower() for t in signal.get("tokens", [])]
            found = [t for t in tokens if t in manifest]
            if found:
                matched = True
                detail = ", ".join(found)
        if matched:
            facts.append(DiscoveryFact(id=sid, kind=kind, detail=detail, dimensions=dims))
            dimensions.update(dims)

    lang = {"python", "javascript", "rust", "go", "java", "dotnet"}
    if dimensions & lang:
        dimensions.add("code")
    if not facts:
        dimensions.add("sparse")

    return DiscoveryReport(
        facts=facts,
        dimensions=sorted(dimensions),
        skipped_secret_paths=sorted(set(skipped)),
    )
