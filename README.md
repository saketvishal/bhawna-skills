# Bhawna Skills

**Guardrails and reusable skills for reliable AI coding agents.**

Bhawna Skills is an open-source collection of repo-owned skills and utilities that help AI coding agents stay aligned with a project's architecture, decisions, and engineering invariants.

The first utility is **InvariantGate**: a preflight check that reviews an engineering objective *before* implementation starts.

> The goal is simple: catch architectural drift before an agent turns it into code.

## Why

AI coding agents are powerful, but long-running projects accumulate durable decisions that are easy to lose across sessions, agents, and tools. Repeating those decisions in every prompt is expensive and unreliable.

Bhawna Skills keeps the durable rules in the repository and checks proposed work against them before execution.

```text
Objective
   ↓
Repository constitution + invariants
   ↓
InvariantGate semantic preflight
   ↓
PASS / REVIEW / BLOCKED
   ↓
Coding agent
```

## InvariantGate

InvariantGate separates two concerns:

- **Semantic review**: does the proposed objective contradict an architectural decision?
- **Deterministic validation**: is the guardrail configuration itself valid and reproducible?

The first release supports any **OpenAI-compatible chat-completions endpoint**, so teams can choose their own model provider.

### Example

A project invariant:

```yaml
- id: UNDERSTANDING-001
  title: Semantic understanding first
  statement: >
    Free-form user language is interpreted semantically by an LLM.
    Deterministic code validates facts that can be objectively verified.
  severity: block
```

An objective proposes:

```text
Parse known phrases with regexes and map each phrase to an intent.
```

InvariantGate can return:

```text
BLOCKED

UNDERSTANDING-001
The objective proposes phrase-driven intent parsing, which conflicts with the
project's semantic-understanding architecture.
```

## Quick start

### 1. Install for development

```bash
git clone https://github.com/<you>/bhawna-skills.git
cd bhawna-skills
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Initialize guardrails in a repository

From the repository you want to protect:

```bash
bhawna init
```

This creates:

```text
.bhawna/
├── constitution.md
└── invariants.yaml
```

Edit those files to describe your project's durable rules.

### 3. Configure a semantic evaluator

```bash
export BHAWNA_MODEL_URL="https://your-provider.example/v1"
export BHAWNA_MODEL="your-model"
export BHAWNA_API_KEY="..."   # if required by the provider
```

PowerShell:

```powershell
$env:BHAWNA_MODEL_URL="https://your-provider.example/v1"
$env:BHAWNA_MODEL="your-model"
$env:BHAWNA_API_KEY="..."
```

### 4. Check an objective

```bash
bhawna check objective.md
```

Exit codes:

| Code | Meaning |
| ---: | --- |
| `0` | PASS |
| `2` | BLOCKED |
| `3` | REVIEW required |

For CI/configuration smoke checks without an LLM:

```bash
bhawna check objective.md --config-only
```

`--config-only` intentionally does **not** claim semantic safety.

## Commands

```text
bhawna init [PATH]          Initialize .bhawna/ guardrails
bhawna doctor [PATH]        Validate configuration and prerequisites
bhawna check OBJECTIVE      Run preflight against the repository rules
```

## Design principles

1. **Repository-owned truth** — architecture decisions live with the code, not inside one chat session.
2. **Model-neutral** — Bhawna Skills does not require one coding agent or one LLM provider.
3. **Evidence over guessing** — findings must identify the invariant and the objective text that conflicts with it.
4. **Examples are tests, not architecture** — known failures should not become hard-coded production behavior.
5. **Preflight, not replacement** — this project complements SDD, ADRs, tests, code review, and CI; it does not replace them.
6. **Deterministic where possible, semantic where necessary** — machine-checkable constraints should be enforced mechanically; architectural intent often needs semantic review.

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

## Prior art

Bhawna Skills is informed by ideas from projects working on adjacent problems, including GitHub Spec Kit, ASDD, architecture-guardrail projects, agent skills, and drift testing. It focuses specifically on **pre-execution consistency between a proposed objective and a repository's durable decisions**.

See [`docs/prior-art.md`](docs/prior-art.md).

## Security

Objectives, constitutions, and invariants may contain proprietary project information. When semantic evaluation is enabled, that content is sent to the model endpoint you configure. Review your provider's data-handling terms before using it with sensitive repositories.

See [`SECURITY.md`](SECURITY.md).

## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
