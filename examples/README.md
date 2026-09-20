# Examples

These files are **documentation and evaluation fixtures**, not production matching rules.

| Path | Purpose |
| --- | --- |
| [`sample-project/`](sample-project/) | Tiny adoption example: constitution, invariants, objectives |
| [`demo-simple/`](demo-simple/) | Python CLI discovery demo |
| [`demo-fullstack/`](demo-fullstack/) | API + React relevance demo |
| [`demo-ai/`](demo-ai/) | Persistence + vector store decision chain (answers file, not auto-confirm) |
| [`run_decision_demos.py`](run_decision_demos.py) | Runs the three discovery/guided demos |
| [`run_demo.py`](run_demo.py) | Deterministic `bhawna check --config-only` walkthrough |
| [`objective.md`](objective.md) | Historical fixture used in tests/docs |

```bash
uv run python examples/run_decision_demos.py
uv run python examples/run_demo.py
```
