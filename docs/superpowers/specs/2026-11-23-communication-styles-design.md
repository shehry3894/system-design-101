# Design: communication styles (hub + group pages)

Date: 2026-11-23. Status: **waiting on the owner's approval.**
Facts behind it: [communication-styles.md](../../research/communication-styles.md) and [api-styles.md](../../research/api-styles.md).

## Why

The owner wants the whole landscape from a video (15 items) explained without bias toward any option, with low cognitive load: usage, pros and cons, when to use what, a table, and surprising facts.

## Goals

- A hub page: what each of the 15 items is, which group it belongs to, and how to pick a group.
- One page per group that compares its options: features, pros and cons, when to use each, real numbers, surprises.
- Every claim comes from an official source.

**Non-goals:** a page per item; WebRTC media internals; Kafka or RabbitMQ operations; MCP security.
**Anti-goals:** a page that crowns a winner; long pages; any claim taken from the video or from memory.

## Approaches

1. **Hub plus one page per group.** Picked by the owner on 2026-11-23. Pages stay short, and each group is a real backend decision.
2. One page with all 15. Rejected: too long.
3. The API styles page plus one-liners for the rest. Rejected: messaging is a real decision, and one-liners hide that.

## Decisions

Owner-approved: the hub plus one page per group, with API styles first.

My calls (the owner can change any of them):

- **Umbrella term: "communication style".** microservices.io uses it for the request/reply versus messaging choice.
- **Groups:**
  - request-response;
  - server push;
  - messaging.

  No source names "server push" as a group, and the page says so.
- **Request-response options are "API styles".**
  - "HTTP API" means any API over HTTP, so it is the umbrella, not an option.
  - "REST" is the name for FastAPI-style APIs. One line covers the strict meaning: Fielding's REST also requires links in responses.
- **Neutral titles.** Options are listed in alphabetical order.
- **Files** go in `docs/concepts/communication/`:

  | File | Title |
  |---|---|
  | `00-overview.md` | Communication styles: request-response, server push, messaging |
  | `01-api-styles.md` | API styles: GraphQL, gRPC, REST |
  | `02-server-push.md` | Server push: SSE, webhooks, WebRTC, WebSocket |
  | `03-messaging.md` | Messaging: AMQP, Kafka, MQTT |

  - `01-api-styles.md` also gives SOAP, JSON-RPC and MCP one line each.
  - `03-messaging.md` opens with event-driven architecture and ends with AsyncAPI in one line.
- **Decision-page template:** a new `docs/_template-decision.md` with these sections:
  1. The problem.
  2. The options: the same four lines for each option (what it is, pros, cons, use when).
  3. Compare: a table.
  4. Surprises.
  5. Picture: one Mermaid diagram.
  6. Try it.
  7. Remember.
  8. Sources.
- **The hub's picture** is a Mermaid flowchart with three questions:
  - Does the caller need the answer now? Yes means request-response.
  - Must the server tell a client the moment something changes? Yes means server push.
  - Are there many receivers, receivers that may be offline, or senders that must not wait? Yes means messaging.
- **The hub's surprises** are 4 or 5 of the video's claims that fail, each cited (research note §6).
- **Code** goes in `examples/communication/`. The file prefix shows the group: `request_`, `push_`, `messaging_`.
  - First file: `request_payload_size.py`. It encodes the same order as JSON and as Protobuf and prints the byte counts, with a test.
- **Order:**
  1. Now: the hub, then the API styles page and its code.
  2. Later: server push, then messaging. Each needs the owner's go-ahead and its own deep research note first.

## Left to the builder

- The Mermaid diagram type on each group page.
- The exact table columns.
- How the Protobuf message is defined in the example (a `.proto` file or built in code).
