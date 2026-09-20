# Release / distribution checklist

Reusable for future Bhawna Skills versions (replace `0.1.0` / `v0.1.0`).

## Validate main

- [ ] `git checkout main` and `git pull`
- [ ] Working tree clean; no unexplained commits vs `origin/main`
- [ ] `uv sync --extra dev`
- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] `uv run mypy src` (project typecheck; `mypy .` may also scan tests)
- [ ] `uv build`
- [ ] Installed-artifact smoke: `uvx --from dist/bhawna_skills-*-py3-none-any.whl bhawna --help`
- [ ] `bhawna check … --config-only` from the wheel against a sample project
- [ ] README commands match actual CLI
- [ ] Remaining `pip install` / `python -m venv` hits are intentional fixtures

## Semantic canary (when configured)

- [ ] `BHAWNA_MODEL_URL` and `BHAWNA_MODEL` present (do not print secrets)
- [ ] Conflicting objective → expect BLOCKED or REVIEW with cited invariant
- [ ] Aligned objective → expect PASS (or documented REVIEW)
- [ ] If unset: record `LIVE_SEMANTIC_VALIDATION=NOT_RUN` and do not claim otherwise

## Version / tag / GitHub

- [ ] `pyproject.toml` version matches intended tag
- [ ] CHANGELOG has a dated section for this version
- [ ] Tag `vX.Y.Z` on the validated `origin/main` SHA
- [ ] GitHub Release notes: capabilities, limitations, model requirement, semantic-validation status, feedback link
- [ ] Do not recreate an existing tag/release

## PyPI

- [ ] GitHub Environment `pypi` exists
- [ ] PyPI Trusted Publisher pending/active for `saketvishal/bhawna-skills` / `publish.yml` / `pypi`
- [ ] Publish workflow ran on the GitHub Release (or document why not)
- [ ] If published: `uvx --from bhawna-skills bhawna --help` from PyPI

## Feedback / docs / distribution

- [ ] Discussions still enabled; v* feedback thread exists or is created
- [ ] README “Feedback / Ideas” links still valid
- [ ] `docs/launch/` drafts updated if the story changed
- [ ] Watch Discussions + issues; triage with `docs/feedback.md`
- [ ] Do **not** auto-post to HN, Reddit, LinkedIn, or X
