# Contributing

Thanks for helping improve Bhawna Skills.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/). This project does not document pip/venv workflows.

## Development

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run bhawna --help
```

## Documentation site

```bash
uv sync --extra docs
uv run mkdocs serve
uv run mkdocs build --strict
uv run python scripts/check_links.py
```

Public site: https://saketvishal.github.io/bhawna-skills/

## Pull requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Do not weaken a guardrail merely to make a test or demo pass.
- Do not add example-specific production matching.
- Explain any compatibility or security implications.
- Update documentation when the public CLI or config format changes.

Use the pull request template. Validation should match CI: `uv sync --extra dev`, lint, typecheck, tests.

## Design changes

For significant changes, open an issue first. Describe the problem, proposed invariant or capability, alternatives considered, and how the change will be evaluated.

See also [`.bhawna/constitution.md`](.bhawna/constitution.md), [`AGENTS.md`](AGENTS.md), and [`docs/feedback.md`](docs/feedback.md).
