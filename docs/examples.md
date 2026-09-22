# Examples

Runnable fixtures live in the repository under [`examples/`](https://github.com/saketvishal/bhawna-skills/tree/main/examples).

## Sample project

[`examples/sample-project/`](https://github.com/saketvishal/bhawna-skills/tree/main/examples/sample-project) has a constitution, invariants, and two objectives (`use-uv.md` vs `use-pip.md`).

```bash
uv run bhawna check examples/sample-project/objectives/use-uv.md \
  --project examples/sample-project --config-only
```

## Decision catalog demos (no LLM)

```bash
uv run python examples/run_decision_demos.py
```

## Config-only demo

```bash
uv run python examples/run_demo.py
```

## Semantic check (requires model env)

```bash
uv run bhawna check examples/sample-project/objectives/use-pip.md \
  --project examples/sample-project
```

Examples are evaluation fixtures, not production matchers for every codebase.
