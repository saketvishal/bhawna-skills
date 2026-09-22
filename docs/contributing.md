# Contributing

Full contributor guide: [CONTRIBUTING.md](https://github.com/saketvishal/bhawna-skills/blob/main/CONTRIBUTING.md). Code of conduct: [CODE_OF_CONDUCT.md](https://github.com/saketvishal/bhawna-skills/blob/main/CODE_OF_CONDUCT.md).

## Local product checks

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run bhawna --help
```

## Local docs site

```bash
uv sync --extra docs
uv run mkdocs serve
uv run mkdocs build --strict
```

Open http://127.0.0.1:8000/ while `serve` is running.

Do not add Google Analytics, pixels, or product telemetry without an explicit project decision.
