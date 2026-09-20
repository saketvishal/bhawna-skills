# LinkedIn draft (not posted)

AI coding agents follow today’s prompt. They often forget yesterday’s architecture decision.

Bhawna Skills keeps those decisions in the repository and checks a new objective against them before implementation starts. InvariantGate returns PASS, REVIEW, or BLOCKED.

v0.1.0 is public (MIT). It is an alpha: you bring an OpenAI-compatible model endpoint. `--config-only` only validates config files.

Repo: https://github.com/saketvishal/bhawna-skills

If you run coding agents on a long-lived codebase, I want the cases where you would *not* trust a preflight like this.
