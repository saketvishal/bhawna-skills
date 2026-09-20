# Launch notes (draft)

Maintainer-facing copy. Not posted anywhere automatically.

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
