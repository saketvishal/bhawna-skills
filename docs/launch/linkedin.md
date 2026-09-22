# LinkedIn draft (not posted)

Coding agents are good at the request in front of them and bad at last quarter’s architecture decision.

I open-sourced Bhawna Skills: repository-owned decisions plus a preflight (InvariantGate) that checks a proposed objective before implementation — PASS, REVIEW, or BLOCKED.

v0.2.0 can inspect a repo and surface relevant questions. It does not assume the answers, and it does not auto-enforce discoveries.

Alpha. You bring an OpenAI-compatible model endpoint. PyPI is not live yet.

Repo: https://github.com/saketvishal/bhawna-skills
Docs: https://saketvishal.github.io/bhawna-skills/

If you run agents on a long-lived codebase, I want the cases where you would *not* trust a check like this.
