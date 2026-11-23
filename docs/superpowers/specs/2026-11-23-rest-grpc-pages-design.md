# Design: REST and gRPC concept pages

Date: 2026-11-23. Status: **approved by the owner on 2026-11-23** ("Approve"); built on 2026-11-23 ([plan](../plans/2026-11-23-rest-grpc-pages.md)). Short design (a small change on top of [the communication styles design](2026-11-23-communication-styles-design.md)).

## Why

The owner: REST and gRPC "are the main ones to be understood better". Each gets its own concept page. The other request-response items get a few lines each: an example, pros, cons and use cases. Further doc surveys are paused (Strawberry: "Not now").

## Scope (owner, 2026-11-23)

- "Request-response only": the few-line treatment covers SOAP, JSON-RPC and MCP on the API styles page. GraphQL keeps its column and its full option block there; it gets no page of its own.
- Server push and messaging still get their own pages later, as planned.
- This changes one non-goal of the communication styles design ("a page per item"): REST and gRPC now get one each. No other item does.

## Approaches

1. **Two concept pages from `docs/_template.md`, linked from the API styles page.** Picked. The API styles page stays the side-by-side decision page; the new pages go deep.
2. Grow the REST and gRPC sections of the API styles page. Rejected: the owner asked for separate pages, and the page would get long.
3. One page per style, GraphQL included, with the API styles page reduced to tables. Rejected: more pages than asked.

## The design

| File | Title | Holds |
|---|---|---|
| `01-api-styles.md` | API styles: GraphQL, gRPC, REST | Unchanged comparison; links to the two pages; SOAP and JSON-RPC gain an example, pros, cons and use-when; MCP gains pros and cons |
| `02-rest.md` | REST | Resources and URIs; representations (JSON optional); methods and which are safe to retry; status codes 200, 201, 204, 400, 401, 404, 422, 500; stateless requests; caching GET; OpenAPI and `/docs`; versioning and `deprecated=True`; SSE for push; one line on Fielding's strict REST vs typical JSON APIs |
| `03-grpc.md` | gRPC | RPC first (gRPC is one RPC framework; this covers the "RPC" item); `.proto`, field numbers, generated Stub and Servicer; four call types; HTTP/2 messages with the status in trailers; metadata, deadlines, cancellation, status codes, retries; health, reflection, `grpcurl`; gRPC-Web plus a proxy for browsers |
| `04-server-push.md`, `05-messaging.md` | (planned) | Renumbered from 02 and 03; not built now |

- Each new page: one Mermaid diagram; the code folded in `<details>` blocks, each with one visible line on what it shows. REST code: a FastAPI orders example (create, read, update, delete). gRPC code: a server-streaming call ("order status updates") with a deadline.
- Code runs once in a scratch virtual environment before it goes on a page, like the API styles page. FastAPI and gRPC are not installed in the repo's test setup, so no dependency is added.
- Facts come from the research notes. Only bullets still without a source get new reading (e.g. PATCH, 204, `ETag`, SOAP and JSON-RPC pros and cons, MCP pros and cons), logged in a new research note section.
- Docs kept current: hub links, `llms.txt`, `README.md`, `CONTEXT.md` (new terms), HANDOFF, and the communication styles design's file table.

## Goals, non-goals, anti-goals

- **Goals:** a reader understands how REST and gRPC work, not only how they compare; low cognitive load; every fact cited.
- **Non-goals:** pages for GraphQL, SOAP, JSON-RPC or MCP; server push and messaging pages; new full doc surveys.
- **Anti-goals:** long pages; repeating the comparison tables on the new pages; claims from memory or from shared videos.

## Left to the builder

Exact wording, diagram choice, which status codes and headers get an example, and snippet details, as long as each snippet follows its official tutorial and runs.
