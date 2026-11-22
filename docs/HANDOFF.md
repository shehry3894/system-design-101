# Handoff: current state and next steps

Last updated: 2026-11-22. Read this first, together with `CLAUDE.md`.

## What this repo is

A from-scratch system design learning hub, built for **low cognitive load**. The full design is in [docs/superpowers/specs/2026-11-22-learning-hub-design.md](superpowers/specs/2026-11-22-learning-hub-design.md). Don't repeat it here.

## Decisions the owner made

- One repo with docs, examples and the Foodpanda project. Commit and push straight to `main`.
- Markdown first (plus `llms.txt`). HTML visuals come later, generated from each page's animation script. Hosting is decided later.
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
- History: `git log --oneline`.

## Next

1. **Verify the auth_service edits.** They were made without running its tests, because the dependencies couldn't be installed there.
   - `cd project/foodpanda/services/auth_service`
   - `cp test.env.example test.env` (set values)
   - Start Postgres: `docker compose up identity-db`
   - Run the tests (`uv` + `pytest`).
2. **M1**, from the plan [docs/superpowers/plans/2026-11-22-learning-hub-m0-m1.md](superpowers/plans/2026-11-22-learning-hub-m0-m1.md), Tasks 6–8:
   1. Research "How a request travels" from the RFCs.
   2. Send the owner a short concept brief and **wait for approval**.
   3. Write the page.
   4. Visual spike: `visual-explainer` vs plain SVG. **The owner picks.**
3. Auth service step 1: fix the known gaps listed in [project/foodpanda/README.md](../project/foodpanda/README.md), and write its concept pages (M2).

## Suggested skills

- **In the repo** (`.claude/skills/`): `visual-explainer`, `markdown-mermaid-writing`, `ponytail`, `caveman`.
- **Install in Claude Code if missing:**
  - superpowers: `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`.
  - mattpocock skills: `research`, `domain-modeling`, `grilling`, and the grounding rules in `writing-beats`.
