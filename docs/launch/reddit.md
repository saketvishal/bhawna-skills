# Reddit / community drafts (not posted)

Do not submit these automatically. Check each community’s self-promotion rules first.

## Candidate post (engineering-first)

**Title:** Preflight for coding-agent objectives: check them against repo-owned invariants before implementation

**Body:**

AI coding agents are good at the current instruction and bad at remembering last month’s architecture decision. I wanted the durable rules to live in the repo and to be checkable *before* an agent starts writing code.

Bhawna Skills (InvariantGate) does that:

- You write a constitution + invariant catalog in `.bhawna/`
- You run `bhawna check objective.md`
- You get PASS, REVIEW, or BLOCKED, with cited invariants

It talks to any OpenAI-compatible endpoint. `--config-only` is a config smoke test only.

Repo: https://github.com/saketvishal/bhawna-skills

I am looking for criticism, not stars: false passes, false blocks, workflows where this would never be trusted, and agents it should plug into.

Feedback thread: https://github.com/saketvishal/bhawna-skills/discussions/1

## Communities (research only — status: not submitted)

| Community | Why relevant | Rules / check needed | Status |
| --- | --- | --- | --- |
| r/LocalLLaMA | Tooling around local/self-hosted models; provider-neutral evaluator fits | Self-promotion often limited to weekends or flair; no spam | **Do not post until rules reviewed the day of posting** |
| r/ClaudeAI | Heavy coding-agent usage | Promo threads are tightly moderated | **Not submitted** |
| r/Python | CLI / packaging audience | “Self-promotion” ratio rules | **Not submitted** |
| r/MachineLearning | Research-adjacent tools | Usually forbids advertising; P papers preferred | **Likely a poor fit; skip unless a technical write-up exists** |
| r/coding / r/ExperiencedDevs | Architecture-drift problem | Self-promo rules vary | **Not submitted** |
| Hacker News (Show HN) | See `show-hn.md` | Show HN guidelines: show the thing, no hype | **Draft only** |

Never post the same copy to many communities in one day.
