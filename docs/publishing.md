# PyPI publishing (human setup)

This repository is **prepared** to publish `bhawna-skills` to PyPI. It does **not** publish automatically from ordinary pushes.

## Trusted Publishing

The workflow [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC). No PyPI token belongs in GitHub secrets.

One-time maintainer steps:

1. Create a PyPI project (or claim the `bhawna-skills` name) for the maintainer account.
2. On PyPI: **Publishing** → **Add a new pending publisher**:
   - Owner: `saketvishal`
   - Repository: `bhawna-skills`
   - Workflow: `publish.yml`
   - Environment: `pypi`
3. In GitHub: create an Environment named `pypi` (optional protection rules / required reviewers).
4. Cut a GitHub Release. The workflow builds with `uv build` and uploads via OIDC.

Until those steps are done, the publish workflow cannot succeed. That is expected.

## Local build check

```bash
uv sync --extra dev
uv build
uvx --from dist/bhawna_skills-0.1.0-py3-none-any.whl bhawna --help
```

Do not commit `dist/` artifacts.
