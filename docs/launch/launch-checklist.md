# Release / distribution checklist

Reusable (replace `X.Y.Z`).

## Validate

- [ ] Fetch/reconcile `origin/main`; no unexplained local-only commits
- [ ] `uv sync --extra dev`
- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] `uv run mypy .`
- [ ] `uv build`
- [ ] `uvx --from dist/bhawna_skills-*-py3-none-any.whl bhawna --help`
- [ ] Config-only check from the wheel
- [ ] README commands match CLI
- [ ] Remaining `pip install` / `python -m venv` hits are fixtures
- [ ] Semantic canary if `BHAWNA_MODEL_URL` + `BHAWNA_MODEL` set; else `LIVE_SEMANTIC_VALIDATION=NOT_RUN`

## Version / GitHub

- [ ] `pyproject.toml` version matches tag
- [ ] CHANGELOG dated
- [ ] Do not rewrite an existing public tag
- [ ] Tag `vX.Y.Z` on validated `origin/main`
- [ ] GitHub Release notes: capabilities, limitations, model requirement, semantic status, feedback link
- [ ] Discussion announcement
- [ ] README Feedback links

## PyPI

- [ ] Environment `pypi` exists
- [ ] Trusted Publisher on pypi.org (`publish.yml`, env `pypi`)
- [ ] Workflow succeeds
- [ ] `uvx --from bhawna-skills bhawna --help` from public PyPI

## Distribution

- [ ] Update `docs/launch/` drafts if the product story changed
- [ ] Do **not** auto-post HN/Reddit/LinkedIn/X
- [ ] Awesome-list PRs only when the fit is real; disclose affiliation
- [ ] Triage incoming feedback via `docs/feedback-loop.md`
