# Feedback triage

Lightweight process. Do not open an implementation issue for every comment.

Primary intake:

- [Discussions](https://github.com/saketvishal/bhawna-skills/discussions) (ideas, Q&A, show-and-tell)
- [v0.1.0 feedback thread](https://github.com/saketvishal/bhawna-skills/discussions/1)
- [Bug report](https://github.com/saketvishal/bhawna-skills/issues/new?template=bug.yml)
- [Feature request](https://github.com/saketvishal/bhawna-skills/issues/new?template=feature.yml)

## Categories

| Tag | Use when |
| --- | --- |
| BUG | CLI, packaging, or documented command is wrong |
| USABILITY | Hard to install, understand, or run |
| FALSE_PASS | Should have BLOCKED or REVIEW but passed |
| FALSE_BLOCK | BLOCKED or REVIEW when the objective was allowed |
| MISSING_INVARIANT_CAPABILITY | The catalog/evaluator cannot express a needed rule |
| AGENT_INTEGRATION | Skill/hook/CI for a specific coding agent |
| DOCUMENTATION | Docs/examples are wrong or missing |
| ARCHITECTURE_IDEA | Change to InvariantGate design; discuss first |

GitHub labels: `bug`, `usability`, `false-pass`, `false-block`, `agent-integration`, `documentation`, `architecture`, `enhancement`.

## What a useful report answers

1. What happened?
2. What was expected?
3. Which agent/workflow?
4. Which invariant and objective (redact secrets)?
5. Is this product behavior, model behavior, configuration, or documentation?

`--config-only` PASS is not evidence of semantic safety.

Promote a Discussion to an issue only when the category is clear and a maintainer can act on it. Do not weaken invariants to make a report pass.
