# Sample project: adopting Bhawna Skills

This directory is a **tiny fictional app** showing how another developer would adopt InvariantGate. It is not production policy for Bhawna Skills itself.

## Layout

```text
.bhawna/constitution.md
.bhawna/invariants.yaml
objectives/use-uv.md      # aligned with TOOL-001
objectives/use-pip.md     # contradicts TOOL-001 (semantic conflict)
```

## Run from the Bhawna Skills repo root

Validate configuration (deterministic, no LLM):

```bash
uv run bhawna doctor --project examples/sample-project
uv run bhawna check examples/sample-project/objectives/use-pip.md --project examples/sample-project --config-only
```

`--config-only` confirms the files load. It does **not** decide whether `use-pip.md` conflicts with `TOOL-001`.

Semantic preflight (requires `BHAWNA_MODEL_URL` and `BHAWNA_MODEL`):

```bash
uv run bhawna check examples/sample-project/objectives/use-pip.md --project examples/sample-project
uv run bhawna check examples/sample-project/objectives/use-uv.md --project examples/sample-project
```

Expected *semantic* outcomes when the evaluator is working:

| Objective | Typical verdict |
| --- | --- |
| `use-pip.md` | `BLOCKED` — contradicts uv-only dependency management |
| `use-uv.md` | `PASS` — matches the invariant |

Those verdicts come from the model, not from hard-coded phrase matching.
