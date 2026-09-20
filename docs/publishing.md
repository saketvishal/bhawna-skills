# PyPI publishing (human setup)

This repository is **prepared** to publish `bhawna-skills` to PyPI. Ordinary pushes do not publish.

GitHub Environment `pypi` exists. The remaining **first-time** step is on PyPI itself (Trusted Publisher). No API token belongs in GitHub secrets.

## Trusted Publishing

Workflow: [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) ([OIDC](https://docs.pypi.org/trusted-publishers/)).

One-time maintainer steps (if not already done on PyPI):

1. Sign in at https://pypi.org (create an account if needed).
2. **Publishing** → **Add a new pending publisher**:
   - PyPI project name: `bhawna-skills`
   - Owner: `saketvishal`
   - Repository: `bhawna-skills`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`
3. After a GitHub Release is published, the workflow should upload the sdist and wheel.

Until the pending publisher is saved on PyPI, the publish job will fail. That is expected.

## After publication

```bash
uvx --from bhawna-skills bhawna --help
```

`uvx bhawna` looks up a distribution named `bhawna`, which this project does not use.

Do not commit `dist/` artifacts.
