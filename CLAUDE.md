# Rules for agents working on this repo

Goal: low cognitive load. Short pages, one idea at a time, real code behind every concept.

**Start of a session:** read `docs/HANDOFF.md` (goal, current state, next steps).

**End of every turn that changes anything:** update `docs/HANDOFF.md` so a fresh session (any tool) can continue from it alone: the goal, what is done, what is in progress, what is next, and what is waiting on the owner. Also update every other doc the change touches (`README.md`, `llms.txt`, `CONTEXT.md`, the spec, the Foodpanda build log), so no Markdown file is out of date.

**Scope:** do only what the owner has approved. Never start the next milestone until the owner says so.

- **Sources:** only primary or authoritative ones, in this order: RFCs/specs → official docs → canonical author sites → vendor explainers (cross-check only). Never write from memory. The owner's Google Doc is a topic list, not a source.
- **Per topic:**
  1. Research into `docs/research/<topic>.md`, every claim cited.
  2. Send the owner a short concept brief and wait (foundations pages).
  3. Write the page from `docs/_template.md`.
  4. Write the smallest code (`ponytail`).
  5. Add a Mermaid diagram if the idea is visual.
  6. Update `llms.txt`, `README.md`, `CONTEXT.md` and `docs/HANDOFF.md`.
- **Pages:** plain English, one idea per sentence. Spell out every abbreviation at its first use on a page, e.g. "NAT (Network Address Translation)", and in `CONTEXT.md`. Every term is explained before a later page relies on it (`prerequisites` / `grounds` front matter).
- **Diagrams:** Mermaid inside the `.md` page by default. No PNGs and no static HTML. Build an interactive HTML page in `html/` only when stepping through a flow is the lesson, and only with the owner's OK. It is one self-contained file: inline SVG, CSS and a small JS stepper, with no kit and no CDN, built from the page's animation script.
- **Topics:** each topic is a backend design decision (e.g. REST vs gRPC vs GraphQL, bcrypt vs Argon2id). Read each option's official docs first, then compare them: features, pros and cons, when to use each, and real numbers. Use the technical terms developers use (e.g. access pattern, query pattern). The existing auth_service code does not pick topics; its bad practices go in a separate gaps doc.
- **Skills:** for every task, look for the best available skill and use it unasked: `grilling` + `domain-modeling` (mattpocock's `grill-with-docs`) to sharpen a design, `superpowers:brainstorming` for design work, `mattpocock-skills:research` for sources. Research notes are for the writer and may be long; anything the owner reads stays brief.
- **Code:** Python (FastAPI and its usual libraries). Keep comments short; explanations go in the Markdown page.
- **Chat** with the owner: always use the `caveman` skill for every reply: brief, to the point, structured. Questions to the owner stay in full sentences. Pages and code comments stay in normal prose.
- **Checks before commit:** `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`.
- **Secrets:** never commit `.env` files. Only `*.example`.
