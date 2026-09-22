# InvariantGate

InvariantGate is the preflight that checks a proposed **objective** against **confirmed project invariants**, built-in safety policy, scoped rules, and recorded exceptions.

It does **not** enforce proposed, deferred, rejected, unresolved, or not-applicable catalog items.

## Verdicts

| Verdict | Exit code | Meaning |
| --- | ---: | --- |
| `PASS` | `0` | No material conflict found. |
| `REVIEW` | `3` | Ambiguity or a new decision is required before proceeding. |
| `BLOCKED` | `2` | The objective contradicts an explicit invariant. |

`--config-only` always reports configuration validity. A config-only PASS is not semantic safety.

## Precedence

1. Built-in Bhawna safety policy
2. Repository-wide confirmed invariant
3. Scoped confirmed rule (`applies_to` / `scope`)
4. Explicit recorded exception

Built-in safety policy includes: no auto-confirm of semantic decisions, retain provenance, do not enforce rejected/deferred/unresolved records, do not fabricate validation status, and do not silently overwrite accepted config.

## Live vs config-only

Live semantic validation requires `BHAWNA_MODEL_URL` and `BHAWNA_MODEL` (plus auth if the provider needs it). If those are unset, treat live evaluation as **not run**.

## Agent use

Any coding-agent workflow that can run a CLI can call `bhawna check`. The same procedure is documented for agents that load skills. Bhawna does not claim a native Claude Code or Codex marketplace integration.

See [project decisions](project-decisions.md) for what may become an invariant.
