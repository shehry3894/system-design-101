# Handoff: current state and next steps

Last updated: 2026-11-22. Read this first, together with `CLAUDE.md`.

## Goal

A from-scratch system design learning hub with **low cognitive load**: short Markdown pages, one idea each, backed by primary sources and runnable code. It is learned by building a Foodpanda-style project, starting with `auth_service`. Full design: [docs/superpowers/specs/2026-11-22-learning-hub-design.md](superpowers/specs/2026-11-22-learning-hub-design.md).

## Where we are

- M0 (setup) and M1 (foundations page 01 with its Mermaid diagram) are built. The owner is reviewing them.
- **On hold:** M2. Don't start it until the owner says so.

## Decisions the owner made

- One repo with docs, examples and the Foodpanda project. Commit and push straight to `main`.
- Markdown first (plus `llms.txt`). Hosting is decided later.
- Diagrams: Mermaid in the page by default. No PNGs, no static HTML. An interactive plain-SVG page only when stepping through a flow is the lesson, and only with the owner's OK.
- Spell out every abbreviation at its first use.
- Every doc stays current: each turn that changes anything also updates HANDOFF and any README, `llms.txt`, `CONTEXT.md`, spec or build log it touches.
- Order: a foundations prelude ("how a request travels"), then project-first (auth_service is step 1).
- Sources: official or authoritative docs only. The owner's Google Doc "System Design" is a **topic list only**, never a source.
- No HTML visual for non-visual ideas (e.g. KISS). Use a short code example instead.
- **Keep everything short.** The owner finds long text tiring, so chat replies, pages and comments must all be brief.
- Example naming: the prefix shows the purpose.
  - `concurrency/`: `lock_`, `limit_`, `wait_`.
  - `patterns/`: `creational_`, then `structural_` and `behavioral_`.
  - SOLID: `s_`, `o_`, `l_`, `i_`, `d_`.
- The owner may share a Google Sheet of topics later. The plan is to add a sheet that tracks topics one by one.

## Done

- M0: restructure, fixed and simplified examples, `.env` → `*.example`, link checker, vendored skills, README / `llms.txt` / `CONTEXT.md` / template.
- Ponytail pass and comment review on all Python, including auth_service.
- auth_service tests verified: 6 pass against Postgres. Fixed two dependency breaks (psycopg 3 driver, `bcrypt<5`). `uv.lock` committed.
- M1 Tasks 6–7: research note approved; foundations page 01 written ([01-how-a-request-travels.md](00-foundations/01-how-a-request-travels.md)).
- M1 Task 8: visual spike done. Plain SVG won over `visual-explainer`, then the owner chose **Mermaid only** for simple diagrams, so page 01 has no HTML. See the spec, section 8.
- Docs audit: all Markdown brought in line with the decisions above (spec, plan status, `CLAUDE.md`, glossary, Foodpanda and auth_service READMEs).
- History: `git log --oneline`.

## Next

1. Finish M0/M1 review with the owner.
2. Only when the owner says so, M2 (auth service step 1): fix the known gaps listed in [project/foodpanda/README.md](../project/foodpanda/README.md), and write its concept pages (M2).

## Suggested skills

- **In the repo** (`.claude/skills/`): `markdown-mermaid-writing`, `ponytail`, `caveman`. `visual-explainer` is also there but is not the default.
- **Install in Claude Code if missing:**
  - superpowers: `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`.
  - mattpocock skills: `research`, `domain-modeling`, `grilling`, and the grounding rules in `writing-beats`.
