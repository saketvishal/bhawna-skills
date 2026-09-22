# How it works

Bhawna keeps **repository-owned decision memory** and checks new work against **confirmed** rules. Coding agents (Claude Code, Codex, and others) can run the CLI or load the InvariantGate skill; they do not need a vendor-specific plugin.

## Flow

```text
inspect repository (files, lockfiles, manifests)
        ↓
relevant decision areas only
        ↓
confirm / edit / defer / not applicable / undecided
        ↓
.bhawna decisions + confirmed invariants
        ↓
future objective → InvariantGate → PASS | REVIEW | BLOCKED
```

## Relevance, not a quiz

Deterministic **signals** (files, globs, directories, manifest tokens) plus each catalog item’s `applies_when` decide what is in scope. Follow-up questions stay hidden until the parent is answered. Bhawna does not ask every catalog question and does not impose technology choices.

## Provenance

Every record in `decisions.yaml` carries source and status. Semantic discoveries remain **PROPOSED** until a human confirms them. Confirmed **INVARIANT** records are copied into `invariants.yaml` for enforcement.

## Architecture drift

When a later objective contradicts an accepted invariant—for example writing canonical state to a derived index—InvariantGate reports **BLOCKED** or **REVIEW**. That is how the project notices drift before implementation.

## What is not sent to a model

Discovery skips secrets and generated trees (`.env`, credentials, keys, `.venv`, `node_modules`, `dist`/`build`, egg-info) and honors `.bhawnaignore`. Whole repositories are not uploaded. Semantic evaluation sends the objective plus relevant confirmed rules to the endpoint **you** configure.

## Skills and agents

- CLI: `bhawna check` before implementation.
- Skill: [`skills/invariant-gate/SKILL.md`](https://github.com/saketvishal/bhawna-skills/blob/main/skills/invariant-gate/SKILL.md)

Deeper types and precedence: [Architecture](architecture.md).
