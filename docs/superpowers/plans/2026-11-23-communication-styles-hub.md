# Communication Styles Hub + API Styles Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the communication styles hub page, the API styles decision page (with its own MCP section), a decision-page template, and a runnable JSON-vs-Protobuf payload-size example.

**Architecture:** Markdown pages live in `docs/concepts/communication/` and are written only from the two research notes. One stdlib example lives in `examples/communication/`; the existing `examples/test_examples.py` runs it. The indexes (README, `llms.txt`, `CONTEXT.md`, `examples/README.md`, HANDOFF, spec) are updated at the end.

**Tech Stack:** Markdown + Mermaid, Python 3 stdlib (`json`), pytest, `scripts/check_links.py`.

**Spec:** [docs/superpowers/specs/2026-11-23-communication-styles-design.md](../specs/2026-11-23-communication-styles-design.md). Facts: [communication-styles.md](../../research/communication-styles.md) (cited below as **CS**) and [api-styles.md](../../research/api-styles.md) (cited below as **AS**).

## Global Constraints

- Every factual sentence on a page comes from CS or AS, with the source link from the note. Nothing comes from the video or from memory.
- Neutral wording:
  - Options appear in alphabetical order.
  - Each option gets the same four lines: what it is, pros, cons, use when.
  - No "best" or "fastest" unless quoted from a source, with its citation.
- Spell out every abbreviation at its first use on each page.
- Plain English, one idea per sentence, mostly under 20 words. The owner finds long text tiring: one screen per section.
- Diagrams are Mermaid in the page. No HTML and no PNG.
- Front matter on every page: `title`, `prerequisites`, `grounds`.
- Pages `02-server-push.md` and `03-messaging.md` don't exist yet. Name them in plain text, not as links, or the link checker fails.
- Example code:
  - stdlib only;
  - a docstring with what it is, when to use it and a source;
  - ends with `assert`s;
  - short comments.
- Before each commit, run `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`.
- Commit straight to `main`; push at the end of Task 4. Never commit `.env` files.

## Review Focus

1. **Negative numbers in Protobuf.** `int32 -2` is a 10-byte varint (11 bytes with the tag), so it is bigger than JSON's 8 bytes. Task 1 pins this.
2. **Mermaid labels that break rendering**, such as unquoted `(`, `/` or `?` in node text. Tasks 2 and 3 quote every label and render-check each diagram.
3. **A byte count read as a speed claim.** The page must say the numbers are for one order, uncompressed, and are not a benchmark. Task 2, step 2.
4. **Bias.** Watch for one option getting more lines or warmer words, or tables ordered by preference. Task 2, step 3 checks for it.
5. **A stale placeholder.** The `CONTEXT.md` line "being written" must become real links. Task 4, step 1 checks for it with grep.

---

### Task 1: Payload-size example

**Files:**
- Create: `examples/communication/request_payload_size.py`
- Modify: `examples/README.md` (new "Communication" section)

**Interfaces:**
- Produces:
  - `varint(n: int) -> bytes`
  - `field_int(number: int, value: int) -> bytes`
  - `field_bytes(number: int, data: bytes) -> bytes`
  - `encode_order(order: dict) -> bytes`
  - the constant `ORDER`
  - printed output with the lines `JSON: 143 bytes` and `Protobuf: 40 bytes`
- Task 2 quotes the file path, the schema comment and both numbers.

- [ ] **Step 1: Write the file with the order, the schema comment and the asserts. Leave out the function bodies.**

The order and schema are fixed by this plan:

```python
ORDER = {"id": 42, "customer": "Ali",
         "items": [{"name": "Biryani", "qty": 2, "price_cents": 450},
                   {"name": "Lassi", "qty": 1, "price_cents": 150}],
         "total_cents": 1050}
# message Item  { string name = 1; int32 qty = 2; int32 price_cents = 3; }
# message Order { int32 id = 1; string customer = 2; repeated Item items = 3; int32 total_cents = 4; }
```

The asserts go at the end. The first three are the examples on protobuf.dev "Encoding" (AS §6):

```python
assert field_int(1, 150) == bytes.fromhex("089601")
assert field_bytes(2, b"testing") == bytes.fromhex("120774657374696e67")
assert field_bytes(3, field_int(1, 150)) == bytes.fromhex("1a03089601")
assert len(field_int(1, -2)) == 11                                 # negative int32: 10-byte varint
assert len(json.dumps({"a": -2}, separators=(",", ":"))) == 8
assert len(json_bytes) == 143 and len(proto_bytes) == 40
```

- [ ] **Step 2: Run it and check it fails**

Run: `python3 examples/communication/request_payload_size.py`
Expected: `NameError` (the functions are not defined yet).

- [ ] **Step 3: Implement the four functions**

- `varint`: 7-bit groups, lowest first, with the top bit set on every byte except the last. Negative numbers become 64-bit two's complement first: `n &= (1 << 64) - 1`.
- The tag is `number << 3 | wire_type`. The wire type is 0 for a varint and 2 for length-delimited data.
- `encode_order` encodes the fields in field-number order. Each item is its own submessage under field 3.
- JSON uses `json.dumps(ORDER, separators=(",", ":")).encode()`.
- The file prints `JSON: 143 bytes` and `Protobuf: 40 bytes`.

- [ ] **Step 4: Run it and check it passes**

Run: `python3 examples/communication/request_payload_size.py`
Expected: exit code 0, and the output contains `JSON: 143 bytes` and `Protobuf: 40 bytes`.

- [ ] **Step 5: Add the README row, run the checks, commit**

Add a "Communication" section to `examples/README.md` with a prefix table (`request_`, `push_`, `messaging_`) and one row for this file.

Run: `python3 -m pytest examples scripts`, then `python3 scripts/check_links.py`. Expected: all pass.

```bash
git add examples/communication/request_payload_size.py examples/README.md
git commit -m "feat(examples): JSON vs Protobuf payload size for one order"
```

### Task 2: Decision template and API styles page

**Files:**
- Create: `docs/_template-decision.md`
- Create: `docs/concepts/communication/01-api-styles.md`

**Interfaces:**
- Consumes: Task 1's file path, schema comment, and the numbers 143 and 40.
- Produces: the template that Task 3 and the later pages follow, and the page that Task 3 links to.

- [ ] **Step 1: Write `docs/_template-decision.md`**

Use the same placeholder style as `docs/_template.md`.

- Front matter: `title`, `prerequisites`, `grounds`.
- Sections, in this order:
  1. The problem.
  2. The options: one `###` per option, each with exactly four bullets (**What it is**, **Pros**, **Cons**, **Use when**).
  3. Compare: a table.
  4. Surprises.
  5. The picture: one Mermaid diagram.
  6. Try it.
  7. Remember: 3 bullets.
  8. Sources.

- [ ] **Step 2: Write the page from the template, using AS for every fact and CS §2 for MCP**

- **Front matter:**
  - `title: "API styles: GraphQL, gRPC, REST"`
  - `prerequisites: [How a request travels, Communication styles]`
  - `grounds: [API style, HTTP API, REST, RPC, gRPC, Protobuf, GraphQL, JSON-RPC, SOAP, MCP]`
- **The problem:** 1–2 sentences.
- **Terms, one line each:**
  - "HTTP API" is the umbrella term for any API over HTTP, not an option (AS Terms, OAS).
  - The strict-REST note: Fielding requires links in responses; most APIs called REST skip them (AS §2, Fielding 2008).
- **Options, alphabetical:** GraphQL, gRPC, REST. Four bullets each, taken from AS §2–§4 and §7.
- **Also in this group, one line each:** JSON-RPC and SOAP (AS §1, CS §2).
- **MCP section** (`### MCP (Model Context Protocol)`):
  - what it is;
  - JSON-RPC 2.0 messages between hosts, clients and servers;
  - its two transports, stdio and Streamable HTTP;
  - when to build an MCP server: to let AI apps use your service's tools and data;
  - one line on why MCP is not in the Compare table: it connects AI apps to tools, not any client to any backend. All from CS §2.
- **Compare:** rows from AS §5. Columns in the order GraphQL, gRPC, REST.
- **Surprises:** 4–5 items, each cited. Pick from:
  - gRPC answers HTTP 200 even on errors, with the status in trailers (AS §3);
  - `-2` is bigger in Protobuf than in JSON (Task 1);
  - GraphQL can be cached through GET and persisted documents (AS §4);
  - "gRPC is 7–10× faster" has no source (CS §6 #1);
  - GitHub has both a REST API and a GraphQL API (CS §6 #2).
- **The picture:** one Mermaid sequence diagram. It shows the same task ("get order 42 with its items") as one request shape per style. Claim no call counts that a source doesn't state.
- **Try it:**
  - the command `python3 examples/communication/request_payload_size.py` and its two output lines;
  - the schema comment;
  - one line: "One order, uncompressed. Not a benchmark.";
  - one line: real projects use the `protobuf` library and `.proto` files.
- **Remember:** 3 bullets.
- **Sources:** the URLs from AS and CS that the page uses.

- [ ] **Step 3: Self-check the page**

Pass means all of these hold:
- Every fact traces to an AS or CS line.
- The three options have the same four bullets and similar length.
- No "best" or "fastest" appears outside a quote.
- Every abbreviation is spelled out at first use. Check gRPC, RPC, HTTP, JSON, MCP, SOAP, SSE and IDL.

- [ ] **Step 4: Render-check the Mermaid diagram**

Paste the diagram into a scratch HTML page that loads Mermaid from `https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js`. Open it in the built-in browser.
Expected: an SVG renders and the console shows no "Syntax error".

- [ ] **Step 5: Run the checks and commit**

Run: `python3 scripts/check_links.py`. Expected: exit code 0.

```bash
git add docs/_template-decision.md docs/concepts/communication/01-api-styles.md
git commit -m "docs(concepts): API styles decision page and decision template"
```

### Task 3: Hub page

**Files:**
- Create: `docs/concepts/communication/00-overview.md`

**Interfaces:**
- Consumes: Task 2's page path `01-api-styles.md`.

- [ ] **Step 1: Write the page**

- **Front matter:**
  - `title: "Communication styles: request-response, server push, messaging"`
  - `prerequisites: [How a request travels]`
  - `grounds: [communication style, request-response, server push, messaging]`
- **The problem:** two programs must exchange messages. Three questions decide how: who starts, whether the sender waits, how many receivers there are.
- **The picture:** a Mermaid flowchart with the three questions from the design, worded exactly as there. Each leaf names a group.
- **The groups:** one short block each, with sources from CS §1:
  - request-response links to `01-api-styles.md`;
  - server push and messaging say "page coming", with no link;
  - one line says that "server push" is this repo's own label.
- **All 15 items:** one table with the columns Item | What it is (its source's words) | Group, copied from CS §7.
- **Surprises:** CS §6 claims #1, #2, #5, #7 and #8, one line each, with the source.
- **Remember:** 3 bullets. **Sources:** the URLs used.

- [ ] **Step 2: Self-check and render-check**

Run the same checks as Task 2, steps 3 and 4, on this page.

- [ ] **Step 3: Run the checks and commit**

Run: `python3 scripts/check_links.py`. Expected: exit code 0.

```bash
git add docs/concepts/communication/00-overview.md
git commit -m "docs(concepts): communication styles hub page"
```

### Task 4: Indexes, glossary, HANDOFF; push

**Files:**
- Modify: `CONTEXT.md` (the "Communication styles" section)
- Modify: `README.md` (Contents table, the Concepts row)
- Modify: `llms.txt` (new "Concepts" section)
- Modify: `docs/HANDOFF.md`
- Modify: `docs/superpowers/specs/2026-11-22-learning-hub-design.md` (status line)

- [ ] **Step 1: Glossary**

- In `CONTEXT.md`, replace "Taught in the communication styles pages (being written)" with links to `00-overview.md` and `01-api-styles.md`.
- Add these terms from the page's `grounds`, one line each, with their full names: gRPC, Protobuf (Protocol Buffers), GraphQL, JSON-RPC, SOAP.

Run: `grep -n "being written" CONTEXT.md`. Expected: no output.

- [ ] **Step 2: README and `llms.txt`**

- README: in the Concepts row, link both pages.
- `llms.txt`: add a "Concepts" section with the hub, the API styles page and the example, one line each.

- [ ] **Step 3: HANDOFF and spec**

- HANDOFF:
  - Mark Next 1.5–1.7 done.
  - Under Done, list the two pages and the example.
  - Set "Waiting on the owner" to: review the pages, then say go for server push.
- Spec: change the status line to say the hub and API styles pages are done.

- [ ] **Step 4: Run all checks, commit, push**

Run: `python3 -m pytest examples scripts`, then `python3 scripts/check_links.py`. Expected: all pass.

```bash
git add CONTEXT.md README.md llms.txt docs/HANDOFF.md docs/superpowers/specs/2026-11-22-learning-hub-design.md
git commit -m "docs: index communication styles pages; glossary terms"
git push origin main
```
