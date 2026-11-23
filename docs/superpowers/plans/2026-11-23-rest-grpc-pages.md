# REST and gRPC concept pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a REST page and a gRPC page that explain how each works, and give SOAP, JSON-RPC and MCP a few lines each (example, pros, cons, use when) on the API styles page.

**Architecture:** Docs-only change. Snippets are proven in a scratch virtual environment, then pasted into the pages word for word inside `<details>` blocks. Each page change is guarded by a scratch check script that fails before the edit and passes after it.

**Tech Stack:** Markdown, Mermaid, Python 3 (FastAPI, `grpcio` + `grpcio-tools`, `pytest`, all only in the scratch venv).

**Spec:** [docs/superpowers/specs/2026-11-23-rest-grpc-pages-design.md](../specs/2026-11-23-rest-grpc-pages-design.md)

## Global Constraints

- Facts come only from primary sources, cited in the page as `[source, section]`, and each fact is in a research note first. If no source states a pro or a con, write fewer bullets; never one from memory.
- Plain English, one idea per sentence. Spell out every abbreviation at its first use on each page (each page stands alone).
- Analogies: reuse page 01's restaurant lines for REST and gRPC, so the pages never disagree. Analogies carry no citation.
- New pages follow `docs/_template.md`. Code goes under `## In our code`, folded in `<details>`, with one visible line above each block saying what it shows.
- No comparison tables on the new pages; they link to page 01 for that.
- Snippets on the pages match the scratch files exactly. No new libraries in `examples/` or the test suite.
- Before each commit: `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`. Commit and push straight to `main`. Never commit `.env` files.
- Each turn that changes anything also updates `docs/HANDOFF.md`.

## Review Focus

1. A fact on a new page with no citation in a research note (status code meanings and header names are the likely slips).
2. A new page contradicting a page 01 cell, e.g. which methods are safe to retry, or gRPC's HTTP 200 with the status in trailers.
3. Page snippets drifting from the files that ran.
4. Pages growing until they tire the reader. Budgets, counting text outside `<details>` and code fences: `02-rest.md` and `03-grpc.md` 110 lines or fewer each; `01-api-styles.md` 150 or fewer (135 today).
5. An abbreviation used before it is spelled out on that page (HTTP, URI, JSON, RPC, HTTP/2, XML).

The checks in Tasks 3–5 pin items 3–5 and the presence of citations. Items 1 and 2 go to the final reviewer.

---

### Task 1: Fill the source gaps

**Files:**
- Modify: `docs/research/api-styles.md` (new `## 10. REST and gRPC pages (2026-11-23)` before `## Open questions`; new Sources entries)

**Interfaces:**
- Produces: §10, cited facts that §1–9 lack. Tasks 3–5 cite only from §1–10 and `communication-styles.md`.

- [ ] **Step 1:** For each item below, grep the research notes first. Read the primary source only when the note lacks it, and write the fact into §10 with its section number.
  - RFC 9110: PATCH is defined in RFC 5789; 201 Created with `Location`; 204 No Content; 400; 401 with `WWW-Authenticate`; 422; 500; which methods are safe and which are idempotent (§9.2.1, §9.2.2); `ETag` with `If-None-Match` giving 304 Not Modified.
  - RFC 9111: `Cache-Control: max-age`.
  - Fielding 2000: statelessness (§5.1.3). Fielding 2008: hypermedia (already in the note; reuse it).
  - FastAPI: `status_code=201` on the decorator (Response Status Code page).
  - grpc.io Python Basics: a response-streaming method is a generator that yields; the client iterates the call; a deadline covers the whole stream.
  - SOAP 1.2 Part 0 (Primer): one small envelope example; a pro, a con and a use-when, each stated by a W3C source.
  - JSON-RPC 2.0: the request/response example, notifications (§4.1), batch (§6), error codes (§5.1); a use-when from a first-party user (e.g. the LSP or MCP spec says it uses JSON-RPC).
  - MCP: a pro and a con from the MCP spec (e.g. its security section), one line each.
- [ ] **Step 2:** Check: `grep -c "^## 10\." docs/research/api-styles.md` is `1`, and every §10 bullet ends with `]` or `(derived)`. Spot-check 3 facts against their URLs.
- [ ] **Step 3:** Commit `docs(research): facts for REST and gRPC pages`.

### Task 2: Prove the snippets run

**Files (scratch only, under `$SCRATCH/snippets2/`):**
- Create: `rest_orders.py`, `track.proto`, `grpc_track_server.py`, `grpc_track_client.py`, `test_pages.py`

**Interfaces:**
- Produces: `rest_orders.app` (FastAPI); `track.proto` with `service Tracking { rpc TrackOrder (TrackRequest) returns (stream Status); }`, `TrackRequest { int32 id = 1; }`, `Status { string state = 1; }`; `grpc_track_server.serve(port: int, delay: float = 0.1) -> grpc.Server`; `grpc_track_client.py`, which iterates `TrackOrder` with `timeout=` and prints each state. Tasks 3 and 4 paste these files word for word.

- [ ] **Step 1: Write the failing test** `test_pages.py`:

```python
def test_rest_crud():
    c = TestClient(rest_orders.app)
    r = c.post("/orders", json={"total_cents": 1050})
    assert r.status_code == 201 and r.json() == {"id": 1, "total_cents": 1050}
    assert c.get("/orders/1").status_code == 200
    assert c.put("/orders/1", json={"total_cents": 900}).json() == c.put("/orders/1", json={"total_cents": 900}).json()
    assert c.delete("/orders/1").status_code == 204
    assert c.get("/orders/1").status_code == 404
    assert c.get("/orders/1").json() == {"detail": "Order not found"}
    assert c.get("/orders/abc").status_code == 422

def test_grpc_stream():   # protoc first, then serve(50098, delay=0)
    assert [s.state for s in stub.TrackOrder(track_pb2.TrackRequest(id=42), timeout=2)] == ["PLACED", "COOKING", "ON_THE_WAY", "DELIVERED"]

def test_grpc_deadline():  # serve(50097, delay=0.5); timeout=0.2
    with pytest.raises(grpc.RpcError) as e: list(stub.TrackOrder(track_pb2.TrackRequest(id=42), timeout=0.2))
    assert e.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED
```

- [ ] **Step 2:** In a scratch venv (`python3 -m venv`, then `pip install "fastapi[standard]" grpcio grpcio-tools pytest`), run `pytest -q test_pages.py`. Expected: fails, modules missing.
- [ ] **Step 3:** Write the three files, each following its official tutorial. The REST app keeps orders in a dict. The server keeps `wait_for_termination()` under `if __name__ == "__main__":`. Each file is 25 lines or fewer.
- [ ] **Step 4:** Run `pytest -q test_pages.py`. Expected: 3 passed. Then start `python grpc_track_server.py` and run `python grpc_track_client.py`. Expected: `PLACED`, `COOKING`, `ON_THE_WAY`, `DELIVERED`, one per line.

### Task 3: Write `02-rest.md`

**Files:**
- Create: `docs/concepts/communication/02-rest.md`
- Create (scratch): `$SCRATCH/check_pages.py` with modes `rest`, `grpc`, `api`, `docs`

**Interfaces:**
- Consumes: §10 facts; Task 2's `rest_orders.py`.

- [ ] **Step 1: Write the failing check** `check_pages.py rest`: the file exists; front matter has `prerequisites` and `grounds`; headings `## The problem`, `## The picture`, `## How it works`, `## In our code`, `## Try it`, `## Remember`, `## Sources` appear in that order; one ```` ```mermaid ```` block with `accTitle`; `rest_orders.py` appears word for word inside a `<details>` block; visible text is 110 lines or fewer; "URI (Uniform Resource Identifier)" and "HTTP (Hypertext Transfer Protocol)" are spelled out before their first bare use; it links to `01-api-styles.md`; every bullet under `## How it works` ends with `]` or contains `[`.
- [ ] **Step 2:** Run `python3 $SCRATCH/check_pages.py rest`. Expected: FAIL (no file).
- [ ] **Step 3:** Write the page. The problem, plus page 01's REST analogy. The picture: a Mermaid sequence of `POST /orders` → `201 Created`, `GET /orders/1` → `200` with `ETag`, the same GET with `If-None-Match` → `304`. How it works, one numbered step per idea: resources and URIs; representations (JSON optional); methods, with a small table of method / safe / idempotent / typical use; status codes 200, 201, 204, 400, 401, 404, 422, 500; stateless requests; caching; the OpenAPI contract and `/docs`; changing the API (versions, `deprecated=True`); push with SSE (Server-Sent Events); one line on Fielding's strict REST vs typical JSON APIs. Try it: at most 3 `curl` calls against `fastapi dev rest_orders.py`, with their real output.
- [ ] **Step 4:** Run `python3 $SCRATCH/check_pages.py rest`, the test suite and the link check. Expected: OK, 27 passed, exit 0.
- [ ] **Step 5:** Commit `docs(concepts): REST page`.

### Task 4: Write `03-grpc.md`

**Files:**
- Create: `docs/concepts/communication/03-grpc.md`
- Modify (scratch): `check_pages.py` mode `grpc`

**Interfaces:**
- Consumes: §3, §9, §10 facts; Task 2's `track.proto`, `grpc_track_server.py` and `grpc_track_client.py`.

- [ ] **Step 1: Write the failing check** `check_pages.py grpc`: same structure checks as `rest`; `track.proto`, `grpc_track_server.py` and `grpc_track_client.py` appear word for word inside `<details>` blocks; the client call shows `timeout=`; "RPC (Remote Procedure Call)" is spelled out before its first bare use; the page names `grpc-status` and trailers; it links to `01-api-styles.md` and `02-rest.md`.
- [ ] **Step 2:** Run `python3 $SCRATCH/check_pages.py grpc`. Expected: FAIL (no file).
- [ ] **Step 3:** Write the page. The problem: calling a function on another service; RPC is the family, gRPC one member (the "RPC" item). Page 01's gRPC analogy. The picture: a Mermaid sequence of one server-streaming call on HTTP/2: request headers (`:path`, `grpc-timeout`, metadata), one request message, several status messages, trailers with `grpc-status: 0`. How it works: the `.proto` file and field numbers; generated Stub and Servicer; the four call types; on the wire (HTTP/2, length-prefixed messages, status in trailers, HTTP 200); metadata; deadlines and cancellation; status codes; retries need a policy; health, reflection and `grpcurl`; browsers need gRPC-Web plus a proxy. Try it: `python grpc_track_server.py`, then a `grpcurl` call or the Python client, with real output.
- [ ] **Step 4:** Run `python3 $SCRATCH/check_pages.py grpc`, the test suite and the link check. Expected: OK, 27 passed, exit 0.
- [ ] **Step 5:** Commit `docs(concepts): gRPC page`.

### Task 5: Few lines for the rest, on the API styles page

**Files:**
- Modify: `docs/concepts/communication/01-api-styles.md` (`### Also in this group`, `### MCP`, a link line under `## The options`, Sources)
- Modify (scratch): `check_pages.py` mode `api`; raise the old `check_rework.py` visible-line budget from 140 to 150

**Interfaces:**
- Consumes: §10 SOAP, JSON-RPC and MCP facts.

- [ ] **Step 1: Write the failing check** `check_pages.py api`: one line under `## The options` links to `02-rest.md` and `03-grpc.md`; `#### JSON-RPC` and `#### SOAP` subsections each have the bullets **Example**, **Pros**, **Cons**, **Use when**; the JSON-RPC example is one visible line of JSON with `"jsonrpc": "2.0"`; the SOAP example is folded in `<details>`; the MCP block has **Pros** and **Cons**; visible text is 150 lines or fewer; GraphQL, gRPC and REST option blocks are unchanged.
- [ ] **Step 2:** Run it. Expected: FAIL.
- [ ] **Step 3:** Edit the page. Options stay alphabetical (JSON-RPC, SOAP). Each bullet one or two sentences, cited.
- [ ] **Step 4:** Run `check_pages.py api`, `check_rework.py page|fold|survey`, the test suite and the link check. Expected: all OK, 27 passed, exit 0.
- [ ] **Step 5:** Commit `docs(concepts): few lines for JSON-RPC, SOAP and MCP`.

### Task 6: Hub, indexes, glossary, HANDOFF

**Files:**
- Modify: `docs/concepts/communication/00-overview.md` (Request-response "Page:" line links both new pages), `llms.txt`, `README.md`, `CONTEXT.md`, `docs/HANDOFF.md`, `docs/superpowers/specs/2026-11-23-communication-styles-design.md` (file table: `02-server-push.md` → `04-server-push.md`, `03-messaging.md` → `05-messaging.md`, with a dated note), the new spec (status: built)

- [ ] **Step 1: Write the failing check** `check_pages.py docs`: hub, `llms.txt` and `README.md` link `02-rest.md` and `03-grpc.md`; `CONTEXT.md` has each term in both pages' `grounds`; the old spec names `04-server-push.md` and `05-messaging.md`; HANDOFF names both pages and the renumbering, and its Next list says server push is `04`.
- [ ] **Step 2:** Run it. Expected: FAIL.
- [ ] **Step 3:** Make the edits. Glossary entries are one line each, cited the same way as existing ones.
- [ ] **Step 4:** Run every check mode, the test suite and the link check. Expected: all OK.
- [ ] **Step 5:** Commit `docs: index, glossary and handoff for REST and gRPC pages`, then push.

### Task 7: Final review

- [ ] **Step 1:** A fresh reviewer on the most capable model reads the whole change against the spec and this plan's Review Focus, and checks every new fact against the research notes.
- [ ] **Step 2:** Re-grade findings by their effect on the reader. Fix Critical and Important ones in one pass, each with a check that fails first. Log minors in HANDOFF.
- [ ] **Step 3:** Run every check, the test suite and the link check; commit and push.
