# Getting started

Bhawna Skills is a Python CLI for **decision memory** and **architecture guardrails** around AI coding agents.

## Install

Requires [uv](https://docs.astral.sh/uv/). Clone the repository:

```bash
git clone https://github.com/saketvishal/bhawna-skills.git
cd bhawna-skills
uv sync --extra dev
uv run bhawna --help
```

Package name is `bhawna-skills`; the command is `bhawna`. When PyPI Trusted Publishing is configured, use `uvx --from bhawna-skills bhawna`.

## Initialize a project

From a repository you want to protect:

```bash
uv run bhawna init
uv run bhawna doctor
```

`init` writes candidates under `.bhawna/`. It does not overwrite accepted constitution or invariants unless you pass `--force`.

| File | Role |
| --- | --- |
| `constitution.md` | Project narrative and durable rules |
| `invariants.yaml` | Confirmed enforcement surface |
| `decisions.yaml` | All knowledge records and provenance |
| `exceptions.yaml` | Explicit exceptions |

## Guided discovery

```bash
uv run bhawna init --guided --answers answers.yaml
uv run bhawna init --quick
uv run bhawna init --discovery-only --json
uv run bhawna review
uv run bhawna decisions
uv run bhawna unresolved
```

Confirm, defer, reject, or mark items not applicable. Discoveries stay **PROPOSED** until you confirm them.

## Semantic evaluator (optional)

Live comparison uses any OpenAI-compatible chat-completions endpoint:

```bash
export BHAWNA_MODEL_URL="https://your-provider.example/v1"
export BHAWNA_MODEL="your-model"
export BHAWNA_API_KEY="..."   # if required
```

Without these variables, `bhawna check` cannot run live semantic evaluation. `--config-only` still validates that guardrail files parse; it does **not** mean the objective is architecturally safe.

## Check an objective

```bash
uv run bhawna check objective.md
uv run bhawna check objective.md --config-only
```

Verdicts: **PASS** (0), **REVIEW** (3), **BLOCKED** (2). See [InvariantGate](invariant-gate.md).
