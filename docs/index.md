# Bhawna Skills

**Decision memory and architecture guardrails for AI coding agents.**

AI coding agents follow the request in front of them and can contradict yesterday’s architecture. Bhawna records **project decisions** in the repository and runs **InvariantGate** so a new objective is checked against **confirmed project invariants** before implementation.

[Get started](getting-started.md) · [GitHub](https://github.com/saketvishal/bhawna-skills) · [Feedback](https://github.com/saketvishal/bhawna-skills/discussions/2)

## Problem

Coding-agent workflows (Claude Code, Codex, and similar tools) do not automatically remember repository-owned choices: dependency managers, canonical stores, security rules, or how a change is considered done. That gap shows up as **architecture drift**.

## What Bhawna does

1. Inspects the repo and surfaces **relevant** decision areas (it does not invent the answers).
2. Stores confirmed knowledge in `.bhawna/` with provenance.
3. Checks a proposed objective: **PASS**, **REVIEW**, or **BLOCKED**.

Unconfirmed catalog items stay **PROPOSED**. They are never auto-enforced.

## Tiny example

```text
Project invariant:   Python dependency management uses uv.
Proposed objective:  Install dependencies using pip.

Result: BLOCKED
Conflicts with the project's dependency-management invariant.
```

## Installation

Requires [uv](https://docs.astral.sh/uv/). PyPI is not live yet; install from source:

```bash
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
```

After PyPI publication: `uvx --from bhawna-skills bhawna --help`

## Next

- [Getting started](getting-started.md)
- [How it works](how-it-works.md)
- [InvariantGate](invariant-gate.md)
- [CLI reference](cli.md)
