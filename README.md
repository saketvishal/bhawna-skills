# Bhawna Skills

**Reusable guardrails that keep AI coding agents aligned with a project's durable decisions.**

[![CI](https://github.com/saketvishal/bhawna-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/saketvishal/bhawna-skills/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 30-second understanding

**Problem.** AI coding agents can forget or contradict architectural decisions, project rules, tooling choices, and other established invariants.

**Bhawna Skills.** Reusable, repository-owned guardrails and skills that make those decisions durable and checkable.

**InvariantGate.** Checks a proposed objective or plan against those invariants *before* implementation begins.

Conceptual example (not production matching logic):

```text
Project invariant:   Python dependency management uses uv.
Proposed objective:  Install dependencies using pip.

Result: BLOCKED
Conflicts with the project's dependency-management invariant.
```

```text
objective / plan
        ↓
.bhawna constitution + invariants
        ↓
InvariantGate (semantic preflight)
        ↓
PASS  |  REVIEW  |  BLOCKED
        ↓
coding agent proceeds only when allowed
```

## How it works

1. You write durable rules in the repository (`.bhawna/constitution.md` and `.bhawna/invariants.yaml`).
2. Before an agent implements work, you run `bhawna check` on the objective.
3. A **semantic** evaluator (any OpenAI-compatible chat-completions endpoint) compares the *proposed approach* to those rules.
4. The CLI prints a verdict and exits with a status code you can use in scripts or CI.

`--config-only` validates that the guardrail files parse. It does **not** claim the objective is architecturally safe.

## Installation

Requires [uv](https://docs.astral.sh/uv/).

Once the package is on PyPI:

```bash
uvx --from bhawna-skills bhawna --help
uvx --from bhawna-skills bhawna check objective.md
```

Or install the CLI as a user tool:

```bash
uv tool install bhawna-skills
bhawna --help
```

From a clone (development):

```bash
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
```

## Quick start

### 1. Initialize guardrails in a repository

```bash
uv run bhawna init
```

This creates:

```text
.bhawna/
├── constitution.md
└── invariants.yaml
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

Deterministic demo (configuration path, no LLM):

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
```

## Testing

```bash
uv run pytest
```

CI runs the same commands plus a package build and an installed-artifact CLI smoke test. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Feedback / Ideas

- [v0.1.0 feedback discussion](https://github.com/saketvishal/bhawna-skills/discussions/1)
- [GitHub Discussions](https://github.com/saketvishal/bhawna-skills/discussions) (Ideas, Q&A, Show and tell)
- [Bug report](https://github.com/saketvishal/bhawna-skills/issues/new?template=bug.yml)
- [Feature request](https://github.com/saketvishal/bhawna-skills/issues/new?template=feature.yml)

How reports are triaged: [`docs/feedback.md`](docs/feedback.md).

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
