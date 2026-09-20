---
name: invariant-gate
description: Check a proposed engineering objective against repository-owned architecture and policy invariants before implementation starts.
---

# InvariantGate

Use this skill before handing a substantial engineering objective to a coding agent.

## Inputs

- proposed objective/spec
- repository constitution
- invariant catalog
- relevant architecture decisions when available

## Procedure

1. Read the repository constitution and invariant catalog before judging the objective.
2. Identify only invariants materially relevant to the proposed work.
3. Compare the objective's proposed approach—not merely its desired outcome—against those invariants.
4. Treat examples as evaluation evidence, not production rules, unless the repository explicitly says otherwise.
5. Return one of:
   - `PASS`: no material conflict found;
   - `REVIEW`: ambiguity or a decision is required;
   - `BLOCKED`: the objective contradicts an explicit invariant.
6. For every non-pass finding, cite the invariant ID and the objective evidence that caused the finding.
7. Do not silently rewrite architectural decisions. If the objective legitimately requires a new architecture decision, stop for review.

## Non-goals

- writing implementation code;
- inventing project rules;
- replacing tests, code review, SDD, or ADRs;
- converting known examples into special-case production logic.
