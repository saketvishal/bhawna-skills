Bhawna Skills v0.1.0

Reusable, repository-owned guardrails for AI coding agents. InvariantGate checks a proposed objective against `.bhawna/constitution.md` and `invariants.yaml` before implementation starts, and returns PASS, REVIEW, or BLOCKED.

## Try it

From a clone (uv required):

```
uv sync --extra dev
uv run bhawna --help
uv run python examples/run_demo.py
```

PyPI is not part of this GitHub Release until Trusted Publishing is completed on pypi.org. The intended command after publication is:

```
uvx --from bhawna-skills bhawna --help
```

(`uvx bhawna` would look up a different distribution name.)

## Capabilities

- `bhawna init`, `doctor`, `check`
- OpenAI-compatible semantic evaluator (`BHAWNA_MODEL_URL`, `BHAWNA_MODEL`, optional `BHAWNA_API_KEY`)
- `--config-only` validates guardrail files only
- Sample project under `examples/sample-project/`

## Limitations

- Alpha. Semantic quality depends on the model you configure.
- `--config-only` PASS is not semantic validation.
- **Live semantic evaluation was not run** in the environment that published this release (`BHAWNA_MODEL_URL` / `BHAWNA_MODEL` were unset). Do not treat this tag as proof that BLOCKED/PASS paths were live-tested against a model.

## Feedback

https://github.com/saketvishal/bhawna-skills/discussions/1
