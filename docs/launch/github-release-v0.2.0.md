Bhawna Skills v0.2.0

Bhawna helps projects remember important engineering decisions and checks a proposed coding-agent objective against *confirmed* rules before implementation starts.

v0.1.0 shipped InvariantGate (`init` / `doctor` / `check`). This release adds a versioned decision catalog, deterministic discovery, and relevance-routed onboarding. Discoveries stay PROPOSED until you confirm them.

## Try it (from source)

PyPI is not published yet (Trusted Publisher still needs a one-time setup on pypi.org).

```
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
uv run bhawna init --discovery-only --json
uv run python examples/run_decision_demos.py
```

## What this version does

- Inspects lockfiles, manifests, and layout (not the whole repo sent to an LLM)
- Asks only relevant catalog questions (`--quick` = CRITICAL/HIGH)
- Records DECISION / INVARIANT / PREFERENCE / PROCEDURE / gates / unresolved items
- Enforces confirmed invariants via InvariantGate (PASS / REVIEW / BLOCKED)
- Built-in safety: no auto-confirm, no silent overwrite, no fabricated validation

## Limitations

- Alpha. Semantic `bhawna check` needs `BHAWNA_MODEL_URL` and `BHAWNA_MODEL`.
- `--config-only` is not a semantic safety review.
- **Live semantic evaluation was not run** in the environment that published this release.
- Catalog items are guidance until confirmed; they are not universal “best practices.”

## Feedback

https://github.com/saketvishal/bhawna-skills/discussions
