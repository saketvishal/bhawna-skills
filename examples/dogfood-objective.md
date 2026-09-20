# Objective (dogfood)

Make the Bhawna Skills repository GitHub and public-release ready.

Use uv as the documented and tested Python workflow. Do not introduce pip or
venv as the contributor default. Do not change InvariantGate architecture
except to fix a real defect. Do not add phrase-specific production matching
to make demos pass. Do not publish to PyPI from this work. Do not choose a
new license. Keep the package version at 0.1.0.

Preserve repository-owned constitution and invariants. Treat examples as
documentation and evaluation fixtures.

## Dogfood result (this repository)

Command:

```bash
uv run bhawna check examples/dogfood-objective.md --config-only
```

Result: **PASS** (`evaluator=static-pass`). Configuration is valid. Semantic
evaluation was not run because this environment did not set `BHAWNA_MODEL_URL`.
That limitation is documented rather than faked: `--config-only` is not a
semantic safety claim.
