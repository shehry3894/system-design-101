# Design: rework of the communication hub and API styles page

Date: 2026-11-23. Status: **approved by the owner on 2026-11-23** ("Yes, rework"). It changes pages built from [2026-11-23-communication-styles-design.md](2026-11-23-communication-styles-design.md).

## Why

The owner reviewed [the hub](../../concepts/communication/00-overview.md) and [the API styles page](../../concepts/communication/01-api-styles.md) and asked for two things:

- **Real-world analogies.** A video the owner watched used a restaurant (give the waiter your order; ask for "just the salad"). Analogies make a concept easy to grasp and remember, which is the hub's low-cognitive-load goal.
- **A better comparison.** Another agent's REST vs gRPC table named each row by a question a developer asks and gave a concrete example in each cell.

Both the video and that table are guides, not sources. Pages must not be shaped around the video's claims.

## Goals

- Every group on the hub and every option on the API styles page has a one-line analogy.
- The compare table answers more developer questions (auth, timeouts, changing the API, debugging, health checks) without becoming one long table.
- The reader sees the same call written in each style.
- Surprises are facts developers get wrong, from sources, not replies to the video.
- The template carries all of this, so later pages follow it.

**Non-goals:** new pages; runnable gRPC or GraphQL examples in `examples/` (they would add libraries); changes to the research method.
**Anti-goals:** an analogy presented as a fact; a table so long it tires the reader; any fact taken from the video or the other agent's table without a primary source; a page that favours one option.

## Approaches

1. **One running restaurant analogy, rework both pages now, and update the template.** Picked by the owner. The reader learns one world and reuses it on every communication page.
2. A different analogy on each page. Rejected: the reader must learn a new world per page.
3. Use the new style only from the server push page onward. Rejected: the owner is reviewing these two pages now.

## Decisions

Owner-approved (the proposal of 2026-11-23):

- **Analogies** run through one restaurant:
  - Request-response: you order from the waiter and wait at your table.
  - Server push: a pager buzzes when your food is ready.
  - Messaging: order tickets go on the kitchen rail, and each cook takes the next one when free.
  - REST: a fixed menu. Each dish has its own number, and the kitchen decides how to plate it.
  - GraphQL: "Just the salad, no bread." You say exactly what goes on the plate.
  - gRPC: a printed order pad that both sides share. The boxes are numbered, not labeled, so it's fast but unreadable without the key (the `.proto` file).
- **Compare** becomes two short tables:
  - **Design:** what you design, contract, payload, response shape, call types, changing the API.
  - **Run:** transport, browsers, errors, auth, timeouts, caching, debugging, health checks, Python library.
  - Each cell gives a concrete example where one exists, such as `GET /orders/42` vs `Orders.GetOrder`, or `404` vs `NOT_FOUND`.
- **Same call, three ways:** "get order 42" as a FastAPI route, as a `.proto` file plus a Python gRPC server, and as a Strawberry query. Each follows its library's official tutorial. The code lives in the page only.
- **Surprises:** the rule "the hub's surprises are video claims that fail" is dropped. Surprises are facts most developers get wrong, each cited, about one per option, none phrased as a reply to the video.
- **Template:** an analogy line for each option, the two-table compare, and the same task done each way.

My calls (the owner can change any of them):

- The analogy bullet is labelled **In real life:** on every page, so the template label fits later topics that are not about restaurants. It comes first in each option. Analogies need no citation; the page marks them as analogies by that label.
- MCP's analogy is the one its own docs use (a USB-C port for AI apps), cited, if the docs still say it.
- "Same call, three ways" replaces "The picture" on the API styles page. The section opens with the existing sequence diagram (the call on the wire), then the code (the call in the server). One section, not two.
- Each snippet is run once in a scratch virtual environment to prove it works. It is not added to `examples/`, so the test suite needs no new libraries.
- Page 01's surprises: "gRPC is 7× faster" goes (a video claim). It is replaced by a fact about changing a Protobuf message (field numbers, not names, are the contract). The GitHub line is reworded to stand on its own: one API can offer two styles.
- The hub's surprises: the MQTT smart-home line goes (a video claim). It is replaced by the RabbitMQ fact: RabbitMQ was built for AMQP 0-9-1, which shares nothing at the wire level with AMQP 1.0, the standard.
- New facts are researched from primary sources into the existing research note, `docs/research/api-styles.md`.

## Left to the builder

- Exact row wording and cell examples.
- Snippet details, as long as each follows its official tutorial and runs.
