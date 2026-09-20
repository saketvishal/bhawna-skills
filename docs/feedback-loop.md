# Feedback loop

Lightweight. Do not implement every suggestion. Do not turn comments into invariants automatically.

```text
external feedback (Discussion, issue, PR comment)
        ↓
classify (labels)
        ↓
reproduce / understand
        ↓
source: product | model | catalog | configuration | documentation | usability
        ↓
candidate improvement (optional)
        ↓
review
        ↓
implementation objective only if warranted
```

## Labels

| Label | Meaning |
| --- | --- |
| `bug` | Incorrect CLI, packaging, or documented command |
| `documentation` | Docs/examples wrong or missing |
| `usability` | Hard to understand, install, or run |
| `false-positive` | Flagged a conflict that should not be a conflict (`false-block`) |
| `false-negative` | Missed a meaningful conflict (`false-pass`) |
| `discovery` | Repository discovery/routing missed or over-fired |
| `decision-catalog` | Catalog item quality, packs, follow-ups |
| `invariant-gate` | Preflight check behavior |
| `integration` | Agent/CI/skill wiring |
| `security` | Secrets, scanning, data sent to models |
| `feature-request` / `enhancement` | New capability |

Feedback is evidence until a maintainer reviews it. Unconfirmed catalog suggestions stay PROPOSED.

See [`feedback.md`](feedback.md) for intake URLs.
