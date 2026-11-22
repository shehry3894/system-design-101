# Rules for agents working on this repo

Goal: low cognitive load. Short pages, one idea at a time, real code behind every concept.

**Start of a session:** read `docs/HANDOFF.md` (current state and next steps).

- **Sources:** only primary or authoritative ones, in this order: RFCs/specs → official docs → canonical author sites → vendor explainers (cross-check only). Never write from memory. The owner's Google Doc is a topic list, not a source.
- **Per topic:**
  1. Research into `docs/research/<topic>.md`, every claim cited.
  2. Send the owner a short concept brief and wait (foundations pages).
  3. Write the page from `docs/_template.md`.
  4. Write the smallest code (`ponytail`).
  5. Make the HTML visual only if the concept is visual.
  6. Update `llms.txt`, `README.md` and `CONTEXT.md`.
- **Pages:** plain English, one idea per sentence. Every term is explained before a later page relies on it (`prerequisites` / `grounds` front matter).
- **HTML** in `html/` is one self-contained file per visual page: inline SVG, CSS and a small JS stepper, with no kit and no CDN. Build it from the page's animation script, starting from a copy of [01-how-a-request-travels.html](html/00-foundations/01-how-a-request-travels.html). Keep the steps and captions in sync with the script.
- **Chat** with the owner: short (`caveman`). Pages and code comments stay in normal prose.
- **Checks before commit:** `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`.
- **Secrets:** never commit `.env` files. Only `*.example`.
