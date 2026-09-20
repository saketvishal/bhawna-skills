# Show HN draft (not posted)

**Title:** Show HN: Bhawna Skills – check coding-agent objectives against repo invariants before they ship

**URL:** https://github.com/saketvishal/bhawna-skills

## Body

I kept hitting the same failure with AI coding agents: they follow the current instruction well, then contradict an architectural or tooling decision made earlier in the same project.

Bhawna Skills is a small open-source CLI that keeps those durable decisions in the repository and checks a *proposed objective* against them before implementation starts. The first utility is InvariantGate.

Flow:

```text
objective
  → .bhawna/constitution.md + invariants.yaml
  → InvariantGate
  → PASS | REVIEW | BLOCKED
```

The rules live with the code, not in one chat session. Semantic comparison uses any OpenAI-compatible chat-completions endpoint you configure. `--config-only` only validates that the guardrail files parse; it is not a semantic safety claim.

Tiny example (conceptual): if the repo says “Python deps use uv” and the objective says “install with pip”, InvariantGate should BLOCK. That example is documentation, not hard-coded matching.

Try from a clone:

```text
uv sync --extra dev
uv run bhawna --help
uv run python examples/run_demo.py
```

v0.1.0 is an alpha. Semantic evaluation was not live-tested in the environment that cut the GitHub Release. Feedback I want: where you would not trust this yet, which agents to integrate next, and real false-pass / false-block cases.

Discussion: https://github.com/saketvishal/bhawna-skills/discussions/1
