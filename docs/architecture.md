# Architecture

## V0.1 flow

```text
objective.md
    │
    ├── .bhawna/constitution.md
    └── .bhawna/invariants.yaml
             │
             ▼
      Semantic evaluator
             │
             ▼
   PASS / REVIEW / BLOCKED
```

## Boundaries

The CLI owns loading, schema validation, evaluator invocation, result validation, rendering, and exit codes.

The model evaluator owns semantic comparison. It does not mutate project files or execute implementation work.

Project configuration remains repository-owned.

## Future direction

Likely additions include relevance selection, multiple independent judges, ADR-aware evaluation, SARIF output, GitHub Actions, and portable Agent Skills packages.
