# Launch notes (draft)

Maintainer-facing copy. Not posted anywhere automatically.

GitHub Release notes for v0.1.0 should match `docs/launch/` and must state that live semantic evaluation was **not** run in the release environment.

## Short

Bhawna Skills: repository-owned guardrails for AI coding agents. InvariantGate checks a proposed objective against your constitution and invariants before implementation starts — PASS, REVIEW, or BLOCKED.

## Slightly longer

AI coding agents forget durable decisions. Bhawna Skills keeps those decisions in the repo and checks work against them first.

Install with uv:

```text
uvx --from bhawna-skills bhawna --help
uv run bhawna check objective.md
```

InvariantGate talks to any OpenAI-compatible endpoint you configure. `--config-only` validates guardrail files without calling a model.

## Topics (GitHub)

ai-agents, coding-agents, agentic-ai, llm, developer-tools, guardrails, architecture, spec-driven-development, python, cli
