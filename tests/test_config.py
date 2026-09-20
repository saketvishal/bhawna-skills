from pathlib import Path

import yaml

from bhawna_skills.config import load_invariants


def test_load_invariants(tmp_path: Path) -> None:
    directory = tmp_path / ".bhawna"
    directory.mkdir()
    (directory / "invariants.yaml").write_text(
        yaml.safe_dump(
            {
                "project": "demo",
                "version": 1,
                "invariants": [
                    {"id": "X-1", "title": "Rule", "statement": "Do the thing."}
                ],
            }
        ),
        encoding="utf-8",
    )
    loaded = load_invariants(tmp_path)
    assert loaded.invariants[0].id == "X-1"
