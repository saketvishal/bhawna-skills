# Reddit drafts (not posted)

## Post

**Title:** Coding agents keep forgetting last month’s architecture decision — I built a repo-owned preflight for that

**Body:**

I kept seeing the same pattern: an agent follows the current prompt, then installs pip in a uv repo, or treats a vector index as canonical state.

Bhawna Skills (https://github.com/saketvishal/bhawna-skills, docs: https://saketvishal.github.io/bhawna-skills/) stores decisions in `.bhawna/` and runs InvariantGate on the *objective* before code. v0.2.0 discovers relevant decision areas from the tree; it does not auto-confirm them.

Not claiming it stops drift or hallucinations. I want critique: false flags, misses, and workflows where you would not use this.

Install today is from source (`uv sync --extra dev`). Semantic check needs your own OpenAI-compatible endpoint.

## Communities (research — not submitted)

| Subreddit | Relevance | Rules / approach | Status |
| --- | --- | --- | --- |
| r/LocalLLaMA | Self-hosted / BYO model fits provider-neutral evaluator | Self-promo often weekend-only or 10% rule; read sidebar the day you post | **Do not post until rules re-checked** |
| r/ClaudeAI | Heavy coding-agent use | Promo threads moderated; lead with a technical question, not a launch | **Not submitted** |
| r/Python | CLI / packaging | Self-promotion ratio; flair if required | **Not submitted** |
| r/MachineLearning | Weak fit (not a paper) | Advertising usually forbidden | **Skip** |
| r/ExperiencedDevs | Architecture-drift anecdote | No product pitches; only if framed as a workplace question without a repo dump | **Likely skip** |

Do not cross-post the same copy the same day.
