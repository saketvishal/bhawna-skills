# Bhawna Skills

**Decision memory and architecture guardrails for AI coding agents.**

[Docs](https://saketvishal.github.io/bhawna-skills/) · [Getting started](https://saketvishal.github.io/bhawna-skills/getting-started/) · [Feedback](https://github.com/saketvishal/bhawna-skills/discussions/2)

[![CI](https://github.com/saketvishal/bhawna-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/saketvishal/bhawna-skills/actions/workflows/ci.yml)
[![Docs](https://github.com/saketvishal/bhawna-skills/actions/workflows/pages.yml/badge.svg)](https://github.com/saketvishal/bhawna-skills/actions/workflows/pages.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Problem

AI coding agents (Claude Code, Codex, and similar workflows) can forget or contradict architectural decisions, project invariants, and tooling choices. That shows up as architecture drift.

## Who it is for

Developers who run coding agents on a long-lived repository and want repository-owned decision memory plus a preflight before implementation.

## What it does

Bhawna inspects the repo, surfaces **relevant** decision areas, records confirmed choices with provenance, and runs **InvariantGate** so a new objective is checked against confirmed invariants: **PASS**, **REVIEW**, or **BLOCKED**. Unconfirmed catalog suggestions are not enforced.

Docs: [How it works](https://saketvishal.github.io/bhawna-skills/how-it-works/) · [InvariantGate](https://saketvishal.github.io/bhawna-skills/invariant-gate/)

Conceptual example (not production matching logic):

```text
Project invariant:   Python dependency management uses uv.
Proposed objective:  Install dependencies using pip.

Result: BLOCKED
Conflicts with the project's dependency-management invariant.
```

You do not need to know every architectural question up front. Bhawna knows *areas worth asking about*; it does not assume the answers.

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

Realistic (not hard-coded) chain:

```text
PostgreSQL + Qdrant dependencies detected
    → Bhawna asks which store is canonical
    → you confirm PostgreSQL; Qdrant is a derived index
    → an objective that writes canonical state to Qdrant
      is checked against that confirmed invariant
```

## How it works

1. `bhawna init` (or `--guided` / `--quick`) discovers objective facts and lists **relevant** catalog questions. Discoveries stay **PROPOSED** until you confirm them.
2. Confirmed decisions live in `.bhawna/decisions.yaml`. Only accepted invariants are copied into `.bhawna/invariants.yaml` for enforcement.
3. `bhawna check` runs InvariantGate against confirmed invariants, scoped rules, built-in safety policy, and recorded exceptions — not unresolved items.
4. Semantic comparison uses any OpenAI-compatible chat-completions endpoint you configure.

`--config-only` validates that the guardrail files parse. It does **not** claim the objective is architecturally safe.

## Installation

Requires [uv](https://docs.astral.sh/uv/).

**From source (current public path).** PyPI Trusted Publishing is prepared but not yet configured on pypi.org, so `uvx --from bhawna-skills` is not available until that one-time publisher is added.

```bash
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
```

After PyPI publication:

```bash
uvx --from bhawna-skills bhawna --help
```

(`uvx bhawna` looks up a different distribution name.)

## Quick start

### 1. Initialize guardrails in a repository

```bash
uv run bhawna init
uv run bhawna init --guided --answers answers.yaml
uv run bhawna init --quick
uv run bhawna init --discovery-only --json
uv run bhawna review
uv run bhawna decisions
uv run bhawna unresolved
```

`bhawna init` creates `.bhawna/` if needed and records **candidates**. It will not silently overwrite accepted configuration. Use `--answers` to confirm, defer, reject, or mark not applicable.

```text
.bhawna/
├── constitution.md
├── invariants.yaml    # confirmed enforcement surface (v0.1 compatible)
├── decisions.yaml     # all knowledge records + provenance
└── exceptions.yaml    # optional explicit exceptions
```

### 2. Creating project invariants

Edit those files so they describe *your* project's durable rules: architecture, tooling, security, and completion gates. Keep statements specific enough to judge an objective, and treat examples as evaluation fixtures—not production matchers.

### 3. Configure a semantic evaluator

```bash
export BHAWNA_MODEL_URL="https://your-provider.example/v1"
export BHAWNA_MODEL="your-model"
export BHAWNA_API_KEY="..."   # if the provider requires it
```

PowerShell:

```powershell
$env:BHAWNA_MODEL_URL="https://your-provider.example/v1"
$env:BHAWNA_MODEL="your-model"
$env:BHAWNA_API_KEY="..."
```

### 4. Check an objective

```bash
uv run bhawna check objective.md
```

Configuration smoke check (no LLM):

```bash
uv run bhawna check objective.md --config-only
```

## PASS / REVIEW / BLOCKED

| Verdict | Exit code | Meaning |
| --- | ---: | --- |
| `PASS` | `0` | No material conflict found. |
| `REVIEW` | `3` | Ambiguity or a new decision is required before proceeding. |
| `BLOCKED` | `2` | The objective contradicts an explicit invariant. |

`--config-only` always reports configuration validity, not semantic safety.

## Commands

```text
bhawna init [PATH]          Initialize .bhawna/ guardrails
bhawna doctor [PATH]        Validate configuration and prerequisites
bhawna check OBJECTIVE      Run preflight against the repository rules
```

## Agent / tool integration

- **CLI:** any agent or human can run `bhawna check` before implementation.
- **Skill:** [`skills/invariant-gate/SKILL.md`](skills/invariant-gate/SKILL.md) describes the same procedure for coding agents that load skills.
- **This repository:** Bhawna dogfoods its own `.bhawna/` constitution and invariants.

Bhawna does not require a particular coding agent or model vendor. Point `BHAWNA_MODEL_URL` at any OpenAI-compatible endpoint.

## Example project

A tiny adoption example lives in [`examples/sample-project/`](examples/sample-project/). It includes a constitution, invariants, two objectives, and commands you can run today.

Decision-catalog demos (no LLM):

```bash
uv run python examples/run_decision_demos.py
```

Legacy config-only demo:

```bash
uv run python examples/run_demo.py
```

Semantic demo (requires `BHAWNA_MODEL_URL` and `BHAWNA_MODEL`):

```bash
uv run bhawna check examples/sample-project/objectives/use-pip.md --project examples/sample-project
```

## Project structure

```text
.bhawna/                 This repo's own constitution and invariants
src/bhawna_skills/       CLI, config loader, evaluators
skills/invariant-gate/   Agent-facing skill description
examples/                Sample project and demo runner
tests/                   Unit tests
.github/workflows/       CI and (optional) PyPI publish
```

## Development

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run bhawna --help
uv sync --extra dev --extra docs
uv run mkdocs build --strict
```

## Testing

```bash
uv run pytest
```

CI runs the same commands plus a package build and an installed-artifact CLI smoke test. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Feedback & Ideas

- [v0.2.0 feedback discussion](https://github.com/saketvishal/bhawna-skills/discussions/2)
- [GitHub Discussions](https://github.com/saketvishal/bhawna-skills/discussions) (Announcements, Ideas, Q&A, Show and tell)
- [Bug report](https://github.com/saketvishal/bhawna-skills/issues/new?template=bug.yml)
- [Feature request](https://github.com/saketvishal/bhawna-skills/issues/new?template=feature.yml)

Triage: [`docs/feedback.md`](docs/feedback.md). Loop: [`docs/feedback-loop.md`](docs/feedback-loop.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Please follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security

Objectives, constitutions, and invariants may contain proprietary information. Semantic evaluation sends that content to the model endpoint you configure. Review the provider's data-handling terms first.

See [`SECURITY.md`](SECURITY.md).

## Roadmap

- [x] Repo-owned constitution and invariant catalog
- [x] `init`, `doctor`, and `check` CLI
- [x] OpenAI-compatible semantic evaluator
- [x] Explicit PASS / REVIEW / BLOCKED results
- [x] Decision catalog, relevance routing, guided/discovery onboarding
- [ ] JSON/SARIF output for CI and code scanning
- [ ] Multiple independent evaluator support
- [ ] Objective-to-invariant relevance selection for smaller prompts
- [ ] ADR-aware preflight
- [ ] Agent Skills (`SKILL.md`) packaging
- [ ] GitHub Action
- [ ] Drift regression suites
- [ ] Project-specific policy plugins

## License

MIT — see [`LICENSE`](LICENSE).
