# CLI reference

Command: `bhawna` (package `bhawna-skills`).

```text
bhawna init [PATH]                 Initialize .bhawna/ guardrails
bhawna init --guided|--quick|--discovery-only|--answers|--json|--all|--force
bhawna doctor [PATH]               Validate configuration and prerequisites
bhawna review [PATH]               Review proposed knowledge
bhawna decisions [PATH]            List recorded decisions
bhawna unresolved [PATH]           List unresolved items
bhawna explain ID                  Explain a record
bhawna check OBJECTIVE             InvariantGate preflight
bhawna check OBJECTIVE --config-only
bhawna decision add|propose|supersede
```

```bash
uv run bhawna --help
uv run bhawna init --help
uv run bhawna check --help
```

Exit codes for `check`: `0` PASS, `2` BLOCKED, `3` REVIEW. `--config-only` does not change those semantic meanings; it skips live evaluation.

Issue tracker: [github.com/saketvishal/bhawna-skills/issues](https://github.com/saketvishal/bhawna-skills/issues).
