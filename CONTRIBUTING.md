# Contributing

Thanks for helping improve Bhawna Skills.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
mypy src
```

On Windows PowerShell use `.venv\Scripts\Activate.ps1`.

## Pull requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Do not weaken a guardrail merely to make a test pass.
- Explain any compatibility or security implications.
- Update documentation when the public CLI or config format changes.

## Design changes

For significant changes, open an issue first. Describe the problem, proposed invariant or capability, alternatives considered, and how the change will be evaluated.
