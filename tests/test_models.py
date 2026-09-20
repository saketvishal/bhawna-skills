from bhawna_skills.models import InvariantSet, Severity


def test_invariant_set_parses() -> None:
    parsed = InvariantSet.model_validate(
        {
            "project": "demo",
            "version": 1,
            "invariants": [
                {
                    "id": "ARCH-001",
                    "title": "No hardcoded examples",
                    "statement": "Examples are tests, not production rules.",
                }
            ],
        }
    )
    assert parsed.project == "demo"
    assert parsed.invariants[0].severity is Severity.block
