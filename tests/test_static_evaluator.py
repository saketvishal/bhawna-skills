from bhawna_skills.evaluator import StaticPassEvaluator
from bhawna_skills.models import InvariantSet, Verdict


def test_static_evaluator_is_explicitly_not_semantic() -> None:
    result = StaticPassEvaluator().evaluate("objective", "constitution", InvariantSet())
    assert result.verdict is Verdict.pass_
    assert result.evaluator == "static-pass"
    assert "Semantic evaluation was not run" in result.summary
