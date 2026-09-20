# Security Policy

## Reporting a vulnerability

Do not open a public issue for a suspected security vulnerability.

Use [GitHub private vulnerability reporting](https://github.com/saketvishal/bhawna-skills/security/advisories/new) when it is enabled for this repository. If it is not enabled, contact the repository owner through GitHub.

## Data handling

When semantic evaluation is enabled, Bhawna Skills sends the objective, constitution, and invariant catalog to the configured model endpoint. Users are responsible for choosing a provider and deployment mode appropriate for their data classification.

API keys are read from environment variables (`BHAWNA_API_KEY` and similar). They must never be committed to the repository.

`--config-only` does not call a model and does not transmit project content.

## Scope notes

Bhawna Skills does not add telemetry and does not contact a network service unless you run semantic evaluation against an endpoint you configure.
