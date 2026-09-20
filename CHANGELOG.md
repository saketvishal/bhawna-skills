# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Changed
- Document and test a uv-first install and development workflow.
- Expand README for 30-second understanding, sample project, and packaging notes.
- CI installs with uv, builds the wheel, and smoke-tests the installed CLI.

### Added
- `examples/sample-project` adoption fixture and `examples/run_demo.py`.
- PyPI Trusted Publishing workflow (does not run until a GitHub Release and publisher are configured).
- `docs/publishing.md` and maintainer `docs/RELEASE_NOTES.md`.

## [0.1.0] - 2026-09-19

### Added
- Initial Bhawna Skills project structure.
- InvariantGate repository initialization.
- Project constitution and invariant catalog.
- Semantic preflight through OpenAI-compatible endpoints.
- PASS, REVIEW, and BLOCKED outcomes.
- `bhawna init`, `bhawna doctor`, and `bhawna check` commands.
