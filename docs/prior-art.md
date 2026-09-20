# Prior art and differentiation

Bhawna Skills builds on ideas explored by several open-source projects while targeting a narrower problem: **preventing an engineering objective from contradicting a repository's durable decisions before implementation starts**.

## Relevant projects

- GitHub Spec Kit — constitution and spec-driven development workflow:
  https://github.com/github/spec-kit
- ASDD — repository-owned contribution governance and hard gates:
  https://github.com/OneHillAI/ASDD
- Agent Drift — stress testing for agent goal and instruction drift:
  https://github.com/jhammant/agent-drift
- Tenets — architecture guardrails for AI coding agents:
  https://github.com/bardiakhosravi/tenets
- Spec-Driven Development Skill — drift-resistant agent workflow:
  https://github.com/mariano-aguero/spec-driven-development-skill

## Bhawna Skills focus

Bhawna Skills is intentionally agent-neutral and starts *before* implementation. Its first utility, InvariantGate, evaluates the proposed engineering objective itself against repository-owned architecture and policy invariants.

It is designed to complement, not replace:

- SDD/spec authoring systems
- ADRs
- code review
- tests and CI
- architecture linters
- coding-agent runtimes
