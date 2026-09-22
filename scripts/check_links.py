"""Lightweight markdown link checker (stdlib)."""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("mailto:", "#")
SKIP_HTTP_SUBSTRINGS: tuple[str, ...] = ()
TIMEOUT = 15

TARGETS = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "docs" / "index.md",
    ROOT / "docs" / "getting-started.md",
    ROOT / "docs" / "how-it-works.md",
    ROOT / "docs" / "invariant-gate.md",
    ROOT / "docs" / "cli.md",
    ROOT / "docs" / "search-console.md",
]


def iter_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [m.group(1).strip().split()[0] for m in LINK_RE.finditer(text)]


def check_local(href: str, from_path: Path) -> str | None:
    if href.startswith(("http://", "https://")):
        return None
    if href.startswith(SKIP_PREFIXES):
        return None
    target = (from_path.parent / href.split("#")[0]).resolve()
    if not target.exists():
        return f"{from_path}: missing local {href}"
    return None


def check_http(url: str) -> str | None:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "bhawna-linkcheck"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            if resp.status >= 400:
                return f"HTTP {resp.status} {url}"
    except urllib.error.HTTPError as exc:
        if exc.code in {405, 403}:
            try:
                req = urllib.request.Request(url, method="GET", headers={"User-Agent": "bhawna-linkcheck"})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    if resp.status >= 400:
                        return f"HTTP {resp.status} {url}"
            except Exception as exc2:  # noqa: BLE001
                return f"{url}: {exc2}"
        else:
            return f"HTTP {exc.code} {url}"
    except Exception as exc:  # noqa: BLE001
        return f"{url}: {exc}"
    return None


def main() -> int:
    errors: list[str] = []
    seen_http: set[str] = set()
    for path in TARGETS:
        if not path.exists():
            errors.append(f"missing file {path}")
            continue
        for href in iter_links(path):
            local = check_local(href, path)
            if local:
                errors.append(local)
            if href.startswith("https://") and href not in seen_http:
                seen_http.add(href)
                if any(s in href for s in SKIP_HTTP_SUBSTRINGS):
                    continue
                remote = check_http(href)
                if remote:
                    errors.append(f"{path}: {remote}")
    for err in errors:
        print(err, file=sys.stderr)
    if errors:
        print(f"LINK_CHECK=FAIL count={len(errors)}")
        return 1
    print("LINK_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
