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
- The owner approved the design on 2026-11-23 and asked where MCP was. MCP now gets its own short section on the API styles page; it stays out of the comparison table (it connects AI apps to tools).
- Glossary terms resolved and added to `CONTEXT.md` (communication style, request-response, server push, messaging, API style, HTTP API, REST, RPC, MCP; from the rework: introspection, metadata, deadline, server reflection, health check).
- Plan written: [2026-11-23-communication-styles-hub.md](superpowers/plans/2026-11-23-communication-styles-hub.md) (4 tasks: example, API styles page + template, hub, indexes).
- The owner chose native execution. The plan ran on 2026-11-23: all 4 tasks done, pages written, checks green. A fresh reviewer then checked the whole change; its fixes are in (wording of the `-2` surprise, a `.proto` con, abbreviations, WebRTC marked peer-to-peer, stale paths), and everything is pushed.
  - [Communication styles](concepts/communication/00-overview.md) (hub) and [API styles: GraphQL, gRPC, REST](concepts/communication/01-api-styles.md), with a [decision-page template](_template-decision.md).
  - Example: [request_payload_size.py](../examples/communication/request_payload_size.py) (JSON 143 bytes, Protobuf 40 bytes for one order).
- The owner reviewed the two pages on 2026-11-23, and the rework from that review is built (below). The next page is "Server push" (`02-server-push.md`). It needs its own deep research note first, and it waits for the owner's go.
- 2026-11-23: the owner said "fix minors first", and all 7 minor review notes are fixed. Groups are now in alphabetical order, our own terms are flagged as ours, page 01 has a REST surprise, and the example skips proto3 default values and sends UTF-8 JSON. (The hub's surprises were failing video claims then; the rework replaced them with sourced facts.)
- Carry over to the messaging page: the smallest MQTT packet (`PINGREQ`) is 2 bytes [MQTT 5.0 §3.12]. The RabbitMQ AMQP 0-9-1 fact is back on the hub as a surprise.
- Video claims not used on any page: #3 (the GraphQL name), #11 (AMQP "older sibling"), #15 (Kafka per second) and #20 (gRPC at Netflix and Uber). Their verdicts are only "no source" or "not found", too weak for a surprise.
- 2026-11-23, owner review feedback:
  - The video is not a source, and pages should not lean on its claims. It was shared to show missing topics and its good real-world analogies, such as ordering from a waiter, or asking for "just the salad" (GraphQL).
  - The owner also shared another agent's REST vs gRPC table as a layout idea, not a source. Its rows are questions a developer asks, and its cells give concrete examples. Its rows for auth/metadata, timeouts, changing the API, debugging and health checks are missing from ours.
- The owner approved the rework ("Yes, rework") and confirmed its scope: GraphQL, gRPC and REST stay the table's columns, "REST and gRPC are the main ones", and the goal is low cognitive load with a deep grasp of each. Design: [2026-11-23-api-pages-rework-design.md](superpowers/specs/2026-11-23-api-pages-rework-design.md). Plan: [2026-11-23-api-pages-rework.md](superpowers/plans/2026-11-23-api-pages-rework.md).
- Rework built on 2026-11-23:
  - Restaurant analogies ("In real life:") on the hub and page 01. MCP uses its own docs' USB-C line, cited.
  - Page 01's Compare is now a Design table and a Run table (auth, timeouts, debugging, health checks added).
  - "Same call, three ways": the sequence diagram, then runnable GraphQL, gRPC and REST code for "get order 42". Each snippet was run once in a scratch virtual environment; none is in `examples/`.
  - Sourced surprises: RabbitMQ's AMQP 0-9-1 on the hub; Protobuf field numbers on page 01.
  - New facts are in the research note §9, with a cell-by-cell source map in §9.10.
  - A fresh reviewer checked the whole rework: no critical findings. The fix pass made the REST analogy mention query parameters, explained server reflection, completed the install line and the gRPC client call, sharpened the HTTPX timeout and the Protobuf surprise, and added RabbitMQ's AMQP 1.0 advice to the hub.
  - Small notes left for later: the messaging analogy shows a queue only, not a copy to every station (owner's call); "methods" and "number" mean different things for REST and gRPC; "USB is Universal Serial Bus." dangles, and HTML, JPEG and RFC are not spelled out on page 01; the cell-source link could point at §9.10.
- 2026-11-23: the owner chose to fold page 01's code into `<details>` blocks; each option keeps one visible line on what its code shows. The template does the same.
- 2026-11-23: the owner asked whether all of grpc.io/docs was read. It was not: 9 of 24 guides had been. The other 15 and the Python generated-code page are now in the research note §9.11. From them, page 01 gained gRPC's built-in retries (a pro), the error message beside the status code, and gRPC's own compression. The rest are operations topics (keepalive, load balancing, and so on), outside this page.
- 2026-11-23: the owner said "Yes, survey them": the same full survey for graphql.org (all 29 Learn pages and the FAQ, research note §9.12) and FastAPI's docs (154 pages, §9.13). Every quote used was checked against the fetched text. Page 01 cells changed:
  - GraphQL: 2xx status beside partial data (Errors), no built-in file uploads (Payload), `curl` (Debugging).
  - REST: OpenAPI 3.1 and client generation (Contract), SSE built into FastAPI (Call types), `deprecated=True` (Changing the API), `{"detail": ...}` and `422` (Errors), Swagger UI at `/docs` (Debugging).
  - The open question on OpenAPI 3.2 is answered: FastAPI emits 3.1.0 only. graphql.org's own pages disagree on 422 for validation errors (§9.12; the page does not use it).
  - Strawberry's docs have not had a full survey; only the pages the snippets needed were read. The owner said "Not now" and paused further surveys.
- 2026-11-23: the owner asked for **separate REST and gRPC pages**, since they are "the main ones to be understood better". The other request-response items get a few lines each (example, pros, cons, use when). Scope: "Request-response only", so SOAP, JSON-RPC and MCP get the few lines on page 01, and server push and messaging keep their own pages (renumbered to `04` and `05`).
  - Design approved: [2026-11-23-rest-grpc-pages-design.md](superpowers/specs/2026-11-23-rest-grpc-pages-design.md).
  - Plan written: [2026-11-23-rest-grpc-pages.md](superpowers/plans/2026-11-23-rest-grpc-pages.md) (7 tasks). **Waiting on the owner:** plan review and the execution method.

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
- **Real-world analogies** (2026-11-23): explain concepts with everyday examples, like a restaurant waiter, so they are easy to grasp and remember. We write them in our own words. Analogies need no source; facts still do.
- Material the owner shares (videos, other agents' answers) guides topics and layout only. It is never a source, and pages are not shaped around its claims.
- **Keep everything short.** The owner finds long text tiring, so chat replies, pages and comments must all be brief.
- On decision pages, code folds into `<details>` blocks (2026-11-23), so the page reads short and the code is a click away.
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
- M2 rework from the owner's review: analogies, Design and Run tables, the same call in code (2026-11-23).
- M2 pages: [Communication styles](concepts/communication/00-overview.md), [API styles](concepts/communication/01-api-styles.md), [decision template](_template-decision.md), example [request_payload_size.py](../examples/communication/request_payload_size.py).
- History: `git log --oneline`.

## Next

1. **Communication styles: hub + API styles page** (structure approved 2026-11-23):
   1. ~~Survey the API styles in official sources.~~ Done.
   2. ~~Research note `docs/research/api-styles.md`, every claim cited.~~ Done. Spot-checked: GraphQL spec September 2026, GraphQL-over-HTTP September 2026 (status 294, 422), OpenAPI 3.2.1, WebSub, the Fielding §5.1.5 quotes, grpc.io usage scenarios, gRPC-Web streaming limits, and the graphql.org microservices FAQ.
   3. ~~Hub research note `docs/research/communication-styles.md`.~~ Done.
   4. ~~Design doc approved; plan written.~~ Done.
   5. ~~Template, hub page, API styles page.~~ Done.
   6. ~~Code `examples/communication/request_payload_size.py`.~~ Done.
   7. ~~Update `CONTEXT.md`, `README.md`, `llms.txt`, the spec and this file.~~ Done.
   8. ~~Rework from the owner's review (analogies, two tables, same call in code).~~ Done.
   9. **Now:** `02-rest.md` and `03-grpc.md`, plus few lines for SOAP, JSON-RPC and MCP on page 01 (plan above, waiting on the owner's plan review).
   10. **After that, when the owner says go:** `04-server-push.md`, then `05-messaging.md`, each with its own deep research note.
2. Proposed order after that: password hashing (bcrypt vs scrypt vs Argon2id), sessions vs tokens (JWT), token signing (HS256 vs RS256), then database decisions.
3. Separate task, when the owner says: `project/foodpanda/services/auth_service/GAPS.md` (bad practice, why it is bad, the fix, link to the concept page). The current list is in [project/foodpanda/README.md](../project/foodpanda/README.md).

## Suggested skills

- **In the repo** (`.claude/skills/`): `markdown-mermaid-writing`, `ponytail`, `caveman`. `visual-explainer` is also there but is not the default.
- **Install in Claude Code if missing:**
  - superpowers: `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`.
  - mattpocock skills ([github.com/mattpocock/skills](https://github.com/mattpocock/skills)): `research`, `domain-modeling`, `grilling`, and the grounding rules in `writing-beats`. `grill-with-docs` is `grilling` + `domain-modeling`; it, `grill-me` and `teach` can only be started by the owner.
- **Owner rule:** search for the best skill for each task and use it unasked. Research notes may be long; what the owner reads stays brief.
