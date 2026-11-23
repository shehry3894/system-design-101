# API pages rework Implementation Plan

> **Status: done (2026-11-23). Kept as a record.** A later owner decision overrides it: page 01's code now folds into `<details>` blocks. Current state: [docs/HANDOFF.md](../../HANDOFF.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add real-world analogies, a two-table comparison, the same call written three ways, and sourced surprises to the communication hub and the API styles page, and carry the new shape into the decision template.

**Architecture:** Docs-only change, plus code snippets that are proven in a scratch virtual environment and then pasted into the page word for word. Each page change is guarded by a scratch check script that fails before the edit and passes after it.

**Tech Stack:** Markdown, Mermaid, Python 3 (FastAPI, `grpcio` + `grpcio-tools`, `strawberry-graphql`, all only in the scratch venv).

**Spec:** [docs/superpowers/specs/2026-11-23-api-pages-rework-design.md](../specs/2026-11-23-api-pages-rework-design.md)

## Global Constraints

- Facts come only from primary sources, cited in the page as `[source, section]`. Never from the video or the other agent's table.
- An analogy is a bullet labelled `**In real life:**`, first in each option, written in our own words, without a citation. The exception is MCP, which uses its own docs' analogy, with a citation.
- Plain English, one idea per sentence. Spell out every abbreviation at its first use on the page.
- Options stay in alphabetical order (GraphQL, gRPC, REST). No option is called best.
- Code is Python. Snippets on the page match the scratch files exactly.
- No new libraries in `examples/` or the test suite.
- Before each commit: `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`. Commit and push straight to `main`.
- Each turn that changes anything also updates `docs/HANDOFF.md`.

## Review Focus

1. An analogy that implies something false. For example, "fixed menu" must not suggest REST can't take query parameters. Every analogy needs checking against the option's facts.
2. A table cell stating a fact that has no citation in the research note.
3. Snippets on the page that drift from the files that ran.
4. Pages growing until they tire the reader. Budgets: `01-api-styles.md` 190 lines or fewer, `00-overview.md` 115 lines or fewer.
5. Strawberry turns `total_cents` into `totalCents`, so the GraphQL query must use `totalCents`.

The checks in Tasks 3 and 4 pin items 3–5. Items 1 and 2 go to the final reviewer.

---

### Task 1: Research the new facts

**Files:**
- Modify: `docs/research/api-styles.md` (new §9, before `## Open questions`; new Sources entries)

**Interfaces:**
- Produces: §9, with cited facts for status codes, auth, timeouts, health checks, debugging tools, REST versioning, Protobuf renames, the three snippets, and MCP's USB-C analogy. Tasks 2–4 cite only from §9 and the earlier sections.

- [x] **Step 1:** A background research agent writes §9 from primary sources. Questions it can't answer are marked "Not found".
- [x] **Step 2:** Check that `grep -c "^## 9\." docs/research/api-styles.md` is `1` and every §9 bullet ends with `]`. Spot-check 3 facts against their URLs: the health service name, the `auto_camel_case` default, and the MCP quote.
- [x] **Step 3:** Commit `docs(research): facts for API pages rework`.

### Task 2: Prove the three snippets run

**Files (scratch only, under `$SCRATCH/snippets/`):**
- Create: `rest_app.py`, `shop.proto`, `grpc_server.py`, `graphql_app.py`, `test_snippets.py`

**Interfaces:**
- Consumes: §9 snippet facts.
- Produces: the five files whose text Task 3 pastes into the page word for word.

- [x] **Step 1: Write the failing test** `test_snippets.py`:

```python
def test_rest():      # FastAPI TestClient
    assert client(rest_app.app).get("/orders/42").json() == {"id": 42, "total_cents": 1050}
    assert client(rest_app.app).get("/orders/abc").status_code == 422
def test_grpc():      # server from grpc_server.serve(port), stub call with timeout=2
    assert (reply.id, reply.total_cents) == (42, 1050)
def test_graphql():   # POST /graphql through FastAPI TestClient
    assert r.json() == {"data": {"order": {"id": 42, "totalCents": 1050}}}
```

- [x] **Step 2:** Run `pytest -q test_snippets.py` in the scratch venv. Expected: it fails because the modules don't exist yet.
- [x] **Step 3:** Write the four snippet files, each following its official tutorial (§9). The server exposes `serve(port)` so the test can start it, and keeps `wait_for_termination()` under `if __name__ == "__main__":`. Each file stays at 15 lines or fewer.
- [x] **Step 4:** Run `pytest -q test_snippets.py`. Expected: 3 passed.

### Task 3: Rework the template and the API styles page

**Files:**
- Modify: `docs/_template-decision.md`, `docs/concepts/communication/01-api-styles.md`
- Test: `$SCRATCH/check_rework.py` (the page part)

**Interfaces:**
- Consumes: the Task 2 files and research §1–9.

- [x] **Step 1: Write the failing checks** in `check_rework.py`:
  - Each of `### GraphQL`, `### gRPC`, `### REST` and `### MCP` has `- **In real life:**` as its first bullet.
  - `## Compare` has `### Design` with these rows: What you design, Contract, Payload, Response shape, Call types, Changing the API.
  - `## Compare` has `### Run` with these rows: Transport, From a browser, Errors, Auth, Timeouts, HTTP caching, Debugging, Health checks, Python library.
  - `## Same call, three ways` exists and holds the `sequenceDiagram`. It contains every Task 2 snippet file verbatim, minus `test_snippets.py`.
  - `## The picture` is gone, and the page has no `7×`.
  - The surprises name field numbers, and the GitHub line no longer says "offers both".
  - The page is 190 lines or fewer.
  - The template has `**In real life:**`, `### Design`, `### Run` and `## Same task, each way`.
- [x] **Step 2:** Run `python3 check_rework.py page`. Expected: FAIL on the first check.
- [x] **Step 3:** Edit the template and the page to the spec. Use the analogies from the spec. Each table cell gives a concrete example where one exists. Abbreviations are spelled out (for example, Uniform Resource Identifier).
- [x] **Step 4:** Run `python3 check_rework.py page`, the pytest suite and the link check. Expected: all pass.
- [x] **Step 5:** Commit `docs(concepts): analogies, two compare tables, same call three ways`.

### Task 4: Rework the hub

**Files:**
- Modify: `docs/concepts/communication/00-overview.md`
- Test: `$SCRATCH/check_rework.py` (the hub part)

- [x] **Step 1: Write the failing checks:**
  - Each block under `## The three groups` has `- **In real life:**` as its first bullet.
  - The hub has no "smart home".
  - Surprises contain `0-9-1` cited `[RabbitMQ, Protocols]`, and Sources link `https://www.rabbitmq.com/docs/protocols`.
  - The hub is 115 lines or fewer.
- [x] **Step 2:** Run `python3 check_rework.py hub`. Expected: FAIL.
- [x] **Step 3:** Edit the hub to the spec.
- [x] **Step 4:** Run `python3 check_rework.py hub`, the suite and the link check. Expected: all pass.
- [x] **Step 5:** Commit `docs(concepts): hub analogies; sourced surprises`.

### Task 5: Spec, indexes, HANDOFF

**Files:**
- Modify:
  - `docs/superpowers/specs/2026-11-23-communication-styles-design.md`: mark the "video claims" surprise rule as superseded, with a link to the rework spec.
  - `CONTEXT.md`: add terms the page now grounds that are missing there, such as health check and server reflection.
  - `README.md` and `llms.txt`: only if their descriptions of these pages are now wrong.
  - `docs/HANDOFF.md`.

- [x] **Step 1:** Run `grep -n "video" docs/superpowers/specs/2026-11-23-communication-styles-design.md docs/concepts/communication/*.md`. Expected: no rule or page text that still relies on the video.
- [x] **Step 2:** Make the edits, then run the suite and the link check.
- [x] **Step 3:** Commit `docs: rework indexes and handoff`, then push.

### Task 6: Final review

- [x] **Step 1:** A fresh reviewer, on the most capable model, reads the diff from the plan's start commit, the spec, and Review Focus items 1–2.
- [x] **Step 2:** Re-grade the findings. Fix Critical and Important ones in one pass, each guarded by a check that fails first. Record minors for the owner.
- [x] **Step 3:** Commit and push. Update HANDOFF.
