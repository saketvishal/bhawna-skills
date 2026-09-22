Bhawna Skills v0.2.0

Bhawna Skills provides decision memory and architecture guardrails for AI coding agents. It preserves durable engineering decisions directly in the repository (`.bhawna/`) and preflights proposed coding-agent objectives against confirmed rules using InvariantGate before implementation begins.

v0.1.0 introduced InvariantGate (`init` / `doctor` / `check`). This release introduces the versioned decision catalog, deterministic stack discovery, relevance-routed onboarding, scoped decisions, and lifecycle tracking. Discoveries remain PROPOSED until you explicitly confirm them.

## Try it (from source)

PyPI publication is pending one-time Trusted Publisher setup on pypi.org. In the meantime, install and run directly from source:

```bash
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
uv run bhawna init --discovery-only --json
uv run python examples/run_decision_demos.py
```

## What this version does

- **Decision memory**: Keeps project architectural invariants, preferences, procedures, and gates alongside source code in `.bhawna/`.
- **Decision catalog**: Includes 19 packs and 90 catalog items spanning architecture, testing, security, CI/CD, data, and agent workflows.
- **Deterministic discovery**: Inspects lockfiles, manifests, and repository structure without uploading code to an LLM.
- **Relevance routing & guided onboarding**: Asks only relevant catalog questions (`--quick` filters to CRITICAL/HIGH priority).
- **Scoped decisions & provenance**: Tracks decision scope (`global`, `path-prefix`, `tag`) and lifecycle states (`PROPOSED`, `CONFIRMED`, `SUPERSEDED`, `DEFERRED`, `UNDECIDED`).
- **InvariantGate preflight**: Checks proposed coding-agent objectives against confirmed invariants only, returning `PASS`, `REVIEW`, or `BLOCKED`.
- **Built-in safety**: Enforces non-destructive operation — no auto-confirmations, no silent overwrites, no fabricated validation claims.

## Documentation

Full documentation, architecture guides, and CLI reference:
https://saketvishal.github.io/bhawna-skills/

## Limitations

- Alpha release. Semantic `bhawna check` evaluation requires an OpenAI-compatible endpoint configured via `BHAWNA_MODEL_URL` and `BHAWNA_MODEL`.
- `--config-only` validates syntax, schemas, and structural constraints; it is not a semantic safety review.
- **Live semantic evaluation was not run** in the environment that published this release.
- Catalog items represent structured prompts and guidance until confirmed; they are not universal "best practices" or dogma.
- Does not claim to eliminate hallucination, drift, or replace human review.

## Feedback & Discussion

We invite real-world feedback, false-positive/false-negative reports, and architecture edge cases:
https://github.com/saketvishal/bhawna-skills/discussions/2
