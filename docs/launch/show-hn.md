# Show HN draft (not posted)

**Title:** Show HN: Bhawna – help AI coding agents remember project decisions

**URL:** https://github.com/saketvishal/bhawna-skills

## Body

I kept watching coding agents follow today’s request while contradicting an architecture or tooling decision made earlier in the same repo.

Bhawna Skills keeps those decisions with the repository and checks a *proposed objective* before implementation. InvariantGate returns PASS, REVIEW, or BLOCKED against *confirmed* invariants only.

v0.2.0 also inspects the repo (lockfiles, manifests) and asks only relevant catalog questions. You do not have to know every architecture question up front. Discoveries stay candidates until you confirm them.

```
uv sync --extra dev
uv run bhawna init --discovery-only
uv run bhawna check objective.md   # needs an OpenAI-compatible endpoint
```

Limitations: alpha; semantic check needs BHAWNA_MODEL_URL + BHAWNA_MODEL; live semantic eval was not run in the release environment; PyPI is not up until Trusted Publishing is configured.

I want false-positives, false-negatives, and “I would not trust this because…”.
