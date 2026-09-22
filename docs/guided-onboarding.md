# Guided onboarding

`bhawna init --guided` inspects the repository and asks **relevant** questions only. It is project decision discovery, not a product-opinion survey.

## Modes

| Flag | Behavior |
| --- | --- |
| `--guided` | Interactive relevant questions |
| `--quick` | Shorter path |
| `--discovery-only` | Report candidates; do not write confirmations |
| `--answers FILE` | Non-interactive answers |
| `--json` | Machine-readable discovery |
| `--all` | Broader catalog (use sparingly) |
| `--force` | Allowed overwrite of existing constitution/invariants |

## Decision chains

Follow-ups appear after a parent is answered. Example: persistence detected → which store is canonical → is another store a derived index.

## YAML answers

Unquoted `yes` / `no` / `on` / `off` / `true` / `false` become booleans in YAML. Quote `"yes"` and `"no"` in option lists and `when_answer_in` values.

## After init

```bash
uv run bhawna review
uv run bhawna doctor
```

Review proposed items before treating them as architecture guardrails.
