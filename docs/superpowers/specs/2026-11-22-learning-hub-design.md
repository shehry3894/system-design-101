# System Design 101: Learning Hub Design

Date: 2026-11-22
Status: draft, waiting for approval

## 1. Intent

Build a from-scratch learning hub for system design. Anyone can clone one repo and go page by page.
The main goal is **low cognitive load**: short pages, one idea at a time, a picture when the idea is visual, and real code behind every concept.

Content is written as Markdown first (readable on GitHub, friendly to LLMs). HTML visuals are generated from the Markdown later. Hosting is decided later.

## 2. Goals, non-goals, anti-goals

**Goals**
- A foundations prelude: "what happens when you open google.com" (client, IP, DNS, domain registration, TCP, TLS, HTTP, the request reaching the gateway).
- Then a project-first path: build a Foodpanda-style system service by service, starting with the existing `auth_service`. Each build step pulls in the concepts it needs (JWT, REST vs gRPC, singleton, KISS, mutex, and so on).
- Each concept page is reusable: later steps link to it instead of explaining it again.
- Every claim comes from official or authoritative sources, cited on the page.
- Every concept links to the exact code that shows it.

**Non-goals (for now)**
- Hosting, a custom domain, or a site generator.
- Video output.
- Covering the whole Google Doc. The doc is a topic list only.

**Anti-goals (failure even if it "works")**
- Walls of text.
- Pages written from memory, or from the Google Doc, without checking primary sources.
- Visuals that decorate instead of explain.
- HTML that drifts from its Markdown source.
- Over-built example code.

## 3. Constraints

- Free GitHub Pages works only from public repos. A private repo plus Pages needs a paid plan, and even then the site is public unless the org uses Enterprise Cloud. This is why hosting is deferred.
- `auth_service/.env`, `local.env` and `test.env` are committed with a `SECRET_KEY` and DB passwords. They move to `.env.example` files. Rotate the values if they are used anywhere real.
- This session has read-only access to the repo. Pushing needs push access or the user pushes.
- Python stays the example language, matching the existing code.

## 4. Approaches considered

| | Approach | Trade-off | Decision |
|---|---|---|---|
| A | One repo: content, examples and the project together | One clone, relative links never break; repo mixes content and project | **Chosen** (Claude's call; the user handed over the how) |
| B | Two repos: content + `foodpanda` monorepo | Cleaner project; cross-repo links break on renames; two clones | Rejected for now. The project can be split out later with `git subtree split`, keeping history |
| C | One repo per service under a GitHub org | Too much setup for no learning gain yet | Rejected. "Polyrepo vs monorepo" can become a lesson page |

Visual tooling is decided per concept, by a spike on the first page (section 8).

## 5. Repo layout

```
system-design-101/
├── README.md                  start here: purpose + table of contents
├── llms.txt                   index of every .md page (llmstxt.org format)
├── CONTEXT.md                 glossary: one short definition per term
├── .claude/skills/            vendored skills (section 7)
├── docs/
│   ├── 00-foundations/        numbered prelude pages
│   │   └── 01-how-a-request-travels.md
│   ├── concepts/              reusable pages, grouped by area
│   │   ├── networking/  api/  security/  data/
│   │   ├── patterns/  principles/  concurrency/  infra/
│   ├── research/              cited research notes, one per topic
│   └── superpowers/specs/     design docs like this one
├── html/                      generated visuals, same path as their .md
├── examples/                  standalone snippets (moved from the root)
│   ├── concurrency/locks/
│   ├── patterns/creational/
│   └── principles/solid/
└── project/foodpanda/
    ├── README.md              build log: each step and the concepts it uses
    └── services/auth_service/ (moved from the root)
```

Moving the existing folders is Claude's call. It keeps the root clean and separates "snippet" code from "project" code.

`llms.txt` follows llmstxt.org: an H1 title, a one-line blockquote summary, then H2 sections that list Markdown links with a short note each.

## 6. The page template

Every concept or foundations page has the same sections, in this order. A section is dropped only when it does not apply.

1. **The problem**: 1–2 sentences. Why this exists.
2. **The picture**: one Mermaid diagram that displays on GitHub. Skipped for principles like KISS.
3. **How it works**: numbered steps or short paragraphs, one idea per sentence.
4. **In our code**: links to exact files (and line ranges) in `examples/` or `project/`.
5. **Try it** (optional): at most 3 commands, for example `dig google.com`.
6. **Remember**: 3 bullets.
7. **Sources**: the primary sources used.
8. **Animation script** (visual topics only): a numbered list of what the HTML visual shows at each step. The HTML is built from this. Nobody edits the HTML by hand.

Front matter on each page: `prerequisites` (pages or terms the reader needs first) and `grounds` (terms this page introduces). This keeps the order honest: a page never leans on a term that no earlier page introduced.

Writing style: plain, simple English. Answer first, one idea per sentence, mostly under 20 words, one term per concept.

## 7. Skills and what each one does

| Step | Skill | Where it lives |
|---|---|---|
| Research from primary sources | `mattpocock-skills:research` | user's account (already installed) |
| Order of ideas, grounding each term before use | `writing-beats` / `writing-shape` grounding rules | user's account |
| Glossary of terms | `mattpocock-skills:domain-modeling` (`CONTEXT.md`) | user's account |
| Stress-test a plan or concept | `mattpocock-skills:grilling` | user's account |
| Markdown + Mermaid diagrams | `markdown-mermaid-writing` (K-Dense, Apache-2.0) | vendored in `.claude/skills/` |
| HTML visuals: SVG, steppers, flow dots | `visual-explainer` (nicobailon, MIT) | vendored in `.claude/skills/`; not the default (section 8) |
| Minimal example code | `ponytail` | user's account + vendored |
| Terse chat replies (not pages) | `caveman` | user's account |
| Charts, when a page has numbers | `dataviz` | built in |

Vendoring means any Claude Code session opened on the repo gets the same skills. Each vendored skill keeps its LICENSE file.

**Considered and rejected:**
- The other K-Dense skills: they target science, and most need an OpenRouter API key.
- Manim skills: they output video, which is heavier to make and not interactive.
- Excalidraw skills: static diagrams only.
- AI-image infographic skills: they need paid image APIs, and the images can't be edited.

## 8. Per-topic workflow

For each topic, in order:

1. **Pick** the next topic from the roadmap. The Google Doc suggests topics; the project's current step decides the order.
2. **Research** with the `research` skill. Use primary sources only, in this order of trust:
   1. Specs and standards (RFCs, W3C, IETF).
   2. Official project docs (nginx.org, kubernetes.io, grpc.io, parquet.apache.org, temporal.io, docs.python.org).
   3. The original author or canonical home (microservices.io by Chris Richardson, martinfowler.com, the GoF book via sources like gofpattern.com).
   4. Reputable vendor explainers (IBM, Cloudflare Learning) only to cross-check.

   Output: `docs/research/<topic>.md`, with every claim cited.
3. **Reason before writing.** List the page's prerequisites and the terms it grounds. Check every claim against the research note. Add or adjust terms in `CONTEXT.md`.
4. **Concept brief, for the user to check.** A 5–10 line summary, the grounding list and the sources. The user says go or corrects it.
5. **Write the page** using the template (section 6), with Mermaid via `markdown-mermaid-writing`.
6. **Write the code** (`ponytail`): the smallest example that shows the idea, with one assert or test if it has logic. It goes in `examples/` or the project service.
7. **Make the visual** (only for visual topics): turn the animation script into a self-contained plain-SVG page at `html/<path>.html`.
8. **Update the indexes**: `llms.txt`, the README table of contents, `CONTEXT.md`, and the project build log.
9. **Check**:
   - Every link resolves (a small script).
   - Code runs.
   - The visual renders with no errors.
   - Facts match the cited sources.

**Visual tooling spike (first page only):** build the "how a request travels" visual twice:
- with `visual-explainer` (hand-drawn SVG plus a stepper);
- as a plain self-contained SVG/CSS page with no kit.

The user compares them and picks the default. Later topics can still pick another tool when the concept needs it.

- 2026-11-22: **Plain SVG chosen as the default.** It is 10 KB instead of 57 KB and needs no build step. Its current step stands out more, and its arrow keys work anywhere on the page. `visual-explainer` stays vendored for concepts that need it.

## 9. Milestones

- **M0, setup:**
  - Move folders into the new layout.
  - Replace the committed `.env` files with `.env.example`.
  - Add README, `llms.txt`, `CONTEXT.md` and the vendored skills.
  - Add a link-check script.
- **M1, foundations page 1:** "How a request travels", from the client to the server's front door. Includes the visual spike. Sources: RFC 1034/1035 (DNS), RFC 9293 (TCP), RFC 8446 (TLS 1.3), RFC 9110 (HTTP semantics), plus registry docs (ICANN) for domain registration.
- **M2, project step 1, auth service:** read the existing code, then write the concept pages it already uses:
  - JWT;
  - HS256 vs RS256 (the `.env` comment already raises this);
  - password hashing;
  - REST;
  - dependency injection via FastAPI `Depends`.

  Link each page to the code.
- **Later:** API gateway with nginx (rate limiting, authentication), REST vs gRPC, data formats, Docker, Kubernetes, Temporal. Each comes in when the project needs it.

## 10. Left to the builder

- The exact Mermaid diagram type per page.
- File names inside `concepts/<area>/`.
- The link-check script's implementation.
- Styling details inside the visual-explainer kit.
