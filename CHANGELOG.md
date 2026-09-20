# Changelog

All notable changes to this project will be documented here.

## [0.2.0] - 2026-09-20

### Added
- Versioned decision catalog (typed packs, provenance, follow-up chains).
- Deterministic repository discovery and relevance routing.
- `.bhawna/decisions.yaml` knowledge store (confirm / defer / reject / N/A / undecided).
- `bhawna init --guided|--quick|--discovery-only`, `review`, `decisions`, `unresolved`, `explain`, `decision add|propose|supersede`.
- Built-in safety rules: no auto-confirm, no silent overwrite, no fabricated validation.
- Secret-path skipping and `.bhawnaignore`.
- Fixture demos: simple, fullstack, AI decision chain.

### Changed
- InvariantGate consumes confirmed invariants, accepted decision context, safety policy, and exceptions. Unresolved catalog items are not enforced.
- Package version 0.2.0.

## [0.1.0] - 2026-09-19

### Added
- Initial Bhawna Skills project structure.
- InvariantGate repository initialization.
- Project constitution and invariant catalog.
- Semantic preflight through OpenAI-compatible endpoints.
- PASS, REVIEW, and BLOCKED outcomes.
- `bhawna init`, `bhawna doctor`, and `bhawna check` commands.
- uv-first development workflow, sample project, and `examples/run_demo.py`.
- PyPI Trusted Publishing workflow (requires a one-time PyPI publisher).
- GitHub Discussions feedback thread and `docs/launch/` distribution drafts.

### Changed
- README and contributor docs use uv only (`uv sync --extra dev`, `uv run …`).
- CI installs with uv, builds the wheel, and smoke-tests the installed CLI.
