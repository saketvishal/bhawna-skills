# Bhawna Skills contributor instructions

Bhawna Skills is an agent-neutral guardrail project.

Before changing behavior:

1. Read `.bhawna/constitution.md` and `.bhawna/invariants.yaml`.
2. Keep the core independent of any single coding agent or LLM provider.
3. Treat examples as tests, not production rules.
4. Add tests for behavior changes.
5. Run the repository validation suite before declaring work complete.
6. Do not weaken guardrails solely to make a test or objective pass.
