# Handoff: current state and next steps

Last updated: 2026-11-23. Read this first, together with `CLAUDE.md`.

## Goal

A from-scratch system design learning hub with **low cognitive load**: short Markdown pages, one idea each, backed by primary sources and runnable code. Each topic is a backend design decision that compares the options. A Foodpanda-style project, starting with `auth_service`, is the worked example. Full design: [docs/superpowers/specs/2026-11-22-learning-hub-design.md](superpowers/specs/2026-11-22-learning-hub-design.md).

## Where we are

- M0 (setup) and M1 (foundations page 01 with its Mermaid diagram) are built.
- M2 (design-decision pages) has started with **API styles**. The owner approved the plan on 2026-11-22.
- The research note is done: [docs/research/api-styles.md](research/api-styles.md). It is long on purpose, for the writer.
- 2026-11-23: the owner shared a video's list of 15 "API styles" (REST, SOAP, gRPC, GraphQL, webhooks, WebSocket, WebRTC, MCP, RPC, SSE, MQTT, AMQP, event-driven, Kafka, AsyncAPI). It is a topic list, not a source. The owner chose **a hub page plus one page per group** (request-response, server push, messaging), API styles first.
- Hub research done from official docs: [docs/research/communication-styles.md](research/communication-styles.md). It classifies all 15 and checks 21 of the video's claims (several fail).
- Design written: [2026-11-23-communication-styles-design.md](superpowers/specs/2026-11-23-communication-styles-design.md) (umbrella term "communication style", file names, a decision-page template, order).
- **Waiting on the owner:** approval of that design. Don't write pages until then.

## Decisions the owner made

- One repo with docs, examples and the Foodpanda project. Commit and push straight to `main`.
- Markdown first (plus `llms.txt`). Hosting is decided later.
- Diagrams: Mermaid in the page by default. No PNGs, no static HTML. An interactive plain-SVG page only when stepping through a flow is the lesson, and only with the owner's OK.
- Spell out every abbreviation at its first use.
- Every doc stays current: each turn that changes anything also updates HANDOFF and any README, `llms.txt`, `CONTEXT.md`, spec or build log it touches.
- Order: a foundations prelude ("how a request travels"), then design-decision pages in the order you design a backend.
- **Concepts drive, not the auth code** (2026-11-22). Each page compares the options: features, pros and cons, when to use each, real numbers (e.g. payload size). Read each option's official docs first. Use the technical terms developers use. The existing auth_service has gaps, so it never picks topics; its bad practices go in a separate gaps doc.
- Code is Python (FastAPI and its usual libraries). Explanations go in Markdown, not long code comments.
- Chat replies always use the `caveman` skill: brief, to the point, structured.
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
- M2 API styles: research note written ([api-styles.md](research/api-styles.md)) and spot-checked.
- M2 communication styles hub: research note written from official docs ([communication-styles.md](research/communication-styles.md)); design doc written.
- History: `git log --oneline`.

## Next

1. **Communication styles: hub + API styles page** (structure approved 2026-11-23):
   1. ~~Survey the API styles in official sources.~~ Done.
   2. ~~Research note `docs/research/api-styles.md`, every claim cited.~~ Done. Spot-checked: GraphQL spec September 2026, GraphQL-over-HTTP September 2026 (status 294, 422), OpenAPI 3.2.1, WebSub, the Fielding §5.1.5 quotes, grpc.io usage scenarios, gRPC-Web streaming limits, and the graphql.org microservices FAQ.
   3. ~~Hub research note `docs/research/communication-styles.md`.~~ Done.
   4. Design doc sent to the owner. **Waiting on approval.** Then `superpowers:writing-plans`.
   5. Template `docs/_template-decision.md`; hub `docs/concepts/communication/00-overview.md`; page `01-api-styles.md`. Each with a Mermaid diagram and sources.
   6. Code `examples/communication/request_payload_size.py`: the same order as JSON and as Protobuf, printing the byte counts, with a test.
   7. Update `CONTEXT.md` (terms: communication style, API style, HTTP API, server push, messaging), `README.md`, `llms.txt`, the spec and this file.
   8. Later, each with the owner's go-ahead: `02-server-push.md`, then `03-messaging.md`, each with its own deep research note.
2. Proposed order after that: password hashing (bcrypt vs scrypt vs Argon2id), sessions vs tokens (JWT), token signing (HS256 vs RS256), then database decisions.
3. Separate task, when the owner says: `project/foodpanda/services/auth_service/GAPS.md` (bad practice, why it is bad, the fix, link to the concept page). The current list is in [project/foodpanda/README.md](../project/foodpanda/README.md).

## Suggested skills

- **In the repo** (`.claude/skills/`): `markdown-mermaid-writing`, `ponytail`, `caveman`. `visual-explainer` is also there but is not the default.
- **Install in Claude Code if missing:**
  - superpowers: `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`.
  - mattpocock skills ([github.com/mattpocock/skills](https://github.com/mattpocock/skills)): `research`, `domain-modeling`, `grilling`, and the grounding rules in `writing-beats`. `grill-with-docs` is `grilling` + `domain-modeling`; it, `grill-me` and `teach` can only be started by the owner.
- **Owner rule:** search for the best skill for each task and use it unasked. Research notes may be long; what the owner reads stays brief.
