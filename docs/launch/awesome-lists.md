# Awesome-list / directory candidates

Do **not** open third-party PRs under the maintainer’s identity from this automation. Local PR text is below.

Spam / “150+ AI tools 2026” style lists are omitted.

| Name | URL | Fit | How to submit | Requirements | Why Bhawna fits | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Awesome LLM Guardrails | https://github.com/royalpinto007/awesome-llm-guardrails | Guardrails for LLM apps (mostly runtime I/O safety) | PR / issue per their README | Open-source, described accurately | Adjacent: Bhawna is *pre-implementation* architecture preflight, not PII/jailbreak scanning. Only submit if they have a “policy / architecture” section; otherwise it is a mismatch. | **Candidate — verify category before PR** |
| Awesome Agent Loops | https://github.com/rudy2steiner/awesome-agent-loops | Verification & guardrails in coding-agent loops | PR; humans approve | Real tool, not a prompt dump | InvariantGate is a verification step *before* a loop implements work. | **Good fit — draft PR locally, do not send** |
| Awesome LLM Agents | https://github.com/kaushikb11/awesome-llm-agents | Frameworks; has Safety/Security & Evaluation | CONTRIBUTING + `data/frameworks/` | Structured metadata, generated README | Stretch: Bhawna is a CLI/skill, not an agent framework. Only if they accept tooling. | **Maybe — read CONTRIBUTING first** |
| Awesome Engineering Agents | https://github.com/usejina/awesome-engineering-agents | Engineering agents and stack | PR | Curated; avoid hype | Bhawna is guardrail tooling *around* those agents. | **Maybe — “Code Analysis & Maintenance” or similar** |
| Awesome AI Agent Tools | https://github.com/michielhdoteth/awesome-ai-agent-tools | Skills/hooks/tools for coding agents | Their install/provenance format | Must be installable with their scheme | SKILL.md exists but is not that catalog’s install format. | **Poor fit until a skill package is published** |
| Awesome TUI | https://awesometui.com/ai | Terminal tools | Claim/submit on site | TUI-oriented | Bhawna is a CLI, not a TUI. | **Skip** |
| sindresorhus/awesome | https://github.com/sindresorhus/awesome | Meta-list | Extremely high bar | Popular, well-documented lists only | Bhawna is a single project, not a list. | **Skip** |

## Local PR blurb (Agent Loops — not sent)

Suggested bullet under Verification & Guardrails:

```markdown
- [Bhawna Skills](https://github.com/saketvishal/bhawna-skills) — CLI that checks a proposed coding-agent objective against repository-owned invariants (PASS / REVIEW / BLOCKED) before implementation.
```
