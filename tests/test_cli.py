from pathlib import Path

from typer.testing import CliRunner

from bhawna_skills.cli import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "init" in result.stdout


def test_init_and_config_only_check(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".bhawna" / "invariants.yaml").exists()
    assert (tmp_path / ".bhawna" / "decisions.yaml").exists()

    objective = tmp_path / "objective.md"
    objective.write_text("Ship a small docs change.", encoding="utf-8")
    check = runner.invoke(
        app,
        ["check", str(objective), "--project", str(tmp_path), "--config-only"],
    )
    assert check.exit_code == 0
    assert "Semantic evaluation was not run" in check.stdout


def test_doctor_on_sample_project() -> None:
    sample = Path("examples/sample-project")
    result = runner.invoke(app, ["doctor", str(sample)])
    assert result.exit_code == 0
    assert "PASS" in result.stdout


def test_init_json_discovery(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", str(tmp_path), "--json"])
    assert result.exit_code == 0
    assert "auto_confirm_semantic_decisions" in result.stdout


def test_decision_propose_not_enforced(tmp_path: Path) -> None:
    runner.invoke(app, ["init", str(tmp_path)])
    prop = runner.invoke(
        app,
        [
            "decision",
            "propose",
            "--id",
            "TMP-1",
            "--statement",
            "maybe use widgets",
            "--project",
            str(tmp_path),
        ],
    )
    assert prop.exit_code == 0
    listed = runner.invoke(app, ["unresolved", str(tmp_path), "--json"])
    assert "TMP-1" in listed.stdout
