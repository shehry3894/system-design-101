# Rules for agents working on this repo

Goal: low cognitive load. Short pages, one idea at a time, real code behind every concept.

- **Sources:** only primary or authoritative ones, in this order: RFCs/specs → official docs → canonical author sites → vendor explainers (cross-check only). Never write from memory. The owner's Google Doc is a topic list, not a source.
- **Per topic:**
  1. Research into `docs/research/<topic>.md`, every claim cited.
  2. Send the owner a short concept brief and wait (foundations pages).
  3. Write the page from `docs/_template.md`.
  4. Write the smallest code (`ponytail`).
  5. Make the HTML visual only if the concept is visual.
  6. Update `llms.txt`, `README.md` and `CONTEXT.md`.
- **Pages:** plain English, one idea per sentence. Every term is explained before a later page relies on it (`prerequisites` / `grounds` front matter).
- **HTML** in `html/` is generated from a page's animation script with `visual-explainer`. Never hand-edit it.
- **Chat** with the owner: short (`caveman`). Pages and code comments stay in normal prose.
- **Checks before commit:** `python3 -m pytest examples scripts` and `python3 scripts/check_links.py`.
- **Secrets:** never commit `.env` files. Only `*.example`.
