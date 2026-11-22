# Learning Hub M0 + M1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the repo into the learning-hub layout (M0). Then ship the first foundations page, "How a request travels", with its research note, Markdown page and chosen HTML visual (M1).

**Architecture:** One repo. Markdown pages in `docs/` are the source of truth. `llms.txt` and the README table of contents index them. HTML visuals in `html/` are generated from each page's animation script. Code lives in `examples/` (snippets) and `project/foodpanda/` (the build). A stdlib link checker keeps relative links honest.

**Tech Stack:** Markdown + Mermaid, Python 3 stdlib + pytest (link checker), Node 22 (visual-explainer `kit/render.mjs`), vendored Claude skills.

**Spec:** `docs/superpowers/specs/2026-11-22-learning-hub-design.md`

M2 (auth-service concept pages) gets its own plan after M1. It depends on the visual tool chosen in Task 8.

## Global Constraints

- Every claim on a page cites a primary source. Trust order: specs/RFCs → official project docs → canonical author sites → vendor explainers (cross-check only).
- The Google Doc is a topic list only, never a source.
- Page sections, in order: The problem, The picture, How it works, In our code, Try it (≤3 commands, optional), Remember (3 bullets), Sources, Animation script (visual topics only).
- Page front matter: `prerequisites` and `grounds`.
- Writing: answer first, one idea per sentence, mostly under 20 words, one term per concept.
- HTML is generated from the animation script. Never hand-edit HTML.
- Foundations pages: send the concept brief to the user and wait for approval before writing the page.
- Example code: smallest code that shows the idea (ponytail). One assert or test if it has logic.
- Vendored skills keep their LICENSE files.
- No real secrets in git: env files are `*.example` with placeholder values.
- Work on branch `learning-hub-m0-m1`. Push only with the user's OK.

## Review Focus

1. A link to a file with a line anchor (`mutex.py#L1-L10`) or heading anchor must count as valid. Test: `test_anchor_and_line_range_stripped` (Task 3).
2. Link-like text inside fenced code blocks must not be flagged. Test: `test_links_in_code_fence_ignored` (Task 3).
3. External links (`https:`, `mailto:`) are not checked, so the checker works offline. Test: `test_external_and_anchor_only_ignored` (Task 3).
4. Anything still pointing at the old root paths (`auth_service/`, `locks/`…) after the move must be caught. Check: Task 5, step 4 runs the checker over the whole repo.
5. Someone cloning and running `docker-compose up` with no `.env` needs a clear first step. Check: the auth_service README "Setup" step `cp .env.example .env` (Task 2).

---

### Task 1: Move existing code into the new layout

**Files:**
- Move: `locks/` → `examples/concurrency/locks/`
- Move: `design_patterns/creational/` → `examples/patterns/creational/`
- Move: `SWE_principles/SOLID/` → `examples/principles/solid/`
- Move: `auth_service/` → `project/foodpanda/services/auth_service/`

**Interfaces:**
- Produces: the paths above. Later tasks link to them.

- [ ] **Step 1:** `git checkout -b learning-hub-m0-m1`
- [ ] **Step 2:** `git mv` each folder to its new path.
- [ ] **Step 3: Verify the snippets still run.** Run `python3 examples/concurrency/locks/mutex.py`. Expected: `200000`. Run `python3 examples/patterns/creational/singleton.py`. Expected: one "Creating" line, then "Reusing" lines.
- [ ] **Step 4:** Check that no file references the old paths: `grep -rn "SWE_principles\|^locks/\|design_patterns/" --exclude-dir=.git .` should match nothing outside `docs/superpowers/`.
- [ ] **Step 5: Commit** `refactor: move code into examples/ and project/foodpanda/`

### Task 2: Replace committed env files with examples

**Files:**
- Delete: `project/foodpanda/services/auth_service/{.env,local.env,test.env}`
- Create: `.env.example`, `local.env.example`, `test.env.example` in the same folder: same keys and comments, placeholder values (`SECRET_KEY=change-me`, `POSTGRES_PASSWORD=change-me`).
- Create: `project/foodpanda/services/auth_service/.gitignore` with `.env`, `local.env`, `test.env`.
- Modify: `project/foodpanda/services/auth_service/README.md`: add a "Setup" step `cp .env.example .env && cp local.env.example local.env && cp test.env.example test.env`. Update the project-structure tree.

- [ ] **Step 1:** Create the three example files. Keep the HS256 vs RS256 comment: M2 uses it.
- [ ] **Step 2:** `git rm --cached` the three real files. Keep them locally, then add `.gitignore`.
- [ ] **Step 3:** Update the README.
- [ ] **Step 4: Verify.** `git ls-files project/foodpanda/services/auth_service | grep -E '(^|/)(\.env|local\.env|test\.env)$'` prints nothing. `grep -c change-me project/foodpanda/services/auth_service/*.example` is ≥1 for each file.
- [ ] **Step 5: Commit** `chore: replace committed env files with .example templates`
- [ ] **Step 6:** Tell the user the old values remain in git history. Rotate them if they are used anywhere real. No history rewrite without their OK.

### Task 3: Link checker

**Files:**
- Create: `scripts/check_links.py`
- Test: `scripts/test_check_links.py`

**Interfaces:**
- Produces: `find_broken_links(root: Path) -> list[tuple[Path, str]]`, returning `(file, target)` for each relative link whose target does not exist.
- Produces: `main() -> int`, printing `<file>: <target>` per broken link and returning 1 if any, else 0. CLI: `python3 scripts/check_links.py [root]`, default root = the repo root.
- Scans `**/*.md` and `llms.txt`. Skips `.git/`, `.claude/`, `node_modules/`. Matches `[text](target)` and `![alt](target)`. Strips `#…` and `?…`. URL-decodes the target. A target starting with `/` resolves from the root; anything else resolves from the file's folder. Skips `http:`, `https:`, `mailto:` and `#`-only targets. Ignores fenced code blocks and inline code.

- [ ] **Step 1: Write failing tests** using `tmp_path`:
  - `test_ok_relative_link`: `a.md` links to `b.md`, which exists → `[]`.
  - `test_broken_link_reported`: `a.md` links to `missing.md` → `[(root/"a.md", "missing.md")]`.
  - `test_anchor_and_line_range_stripped`: links to `x.py#L1-L3` and `b.md#setup`, both files exist → `[]`.
  - `test_external_and_anchor_only_ignored`: `https://x.org`, `mailto:a@b.c`, `#top` → `[]`.
  - `test_links_in_code_fence_ignored`: `[x](nope.md)` inside a code fence → `[]`.
  - `test_skips_dot_claude_dir`: `.claude/s/SKILL.md` links to `nope.md` → `[]`.
  - `test_llms_txt_scanned`: `llms.txt` links to `missing.md` → reported.
- [ ] **Step 2:** Run `python3 -m pytest scripts/test_check_links.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3:** Implement with stdlib only (`re`, `pathlib`, `urllib.parse`).
- [ ] **Step 4:** Run the tests. Expected: 7 passed.
- [ ] **Step 5: Commit** `feat: add relative link checker for docs`

### Task 4: Vendor the skills

**Files:**
- Create: `.claude/skills/visual-explainer/`: copy of `nicobailon/visual-explainer` `plugins/visual-explainer/` plus the repo `LICENSE` (MIT).
- Create: `.claude/skills/markdown-mermaid-writing/`: copy of `K-Dense-AI/scientific-agent-skills` `skills/markdown-mermaid-writing/` plus that repo's LICENSE (Apache-2.0).
- Create: `.claude/skills/ponytail/SKILL.md` + LICENSE (MIT), from `DietrichGebert/ponytail` `skills/ponytail/`.
- Create: `.claude/skills/caveman/SKILL.md` + LICENSE (MIT), from `JuliusBrussee/caveman` `skills/caveman/`.
- Create: `.claude/skills/README.md`: a table of skill, source repo, commit SHA, licence, and why we use it.

- [ ] **Step 1:** Shallow-clone each source into a scratch folder outside the repo. Record `git rev-parse HEAD`.
- [ ] **Step 2:** Copy the folders listed above. Copy each LICENSE.
- [ ] **Step 3:** Write `.claude/skills/README.md`.
- [ ] **Step 4: Verify.** Each of the 4 folders has `SKILL.md` and a `LICENSE*`. Run `node .claude/skills/visual-explainer/kit/render.mjs --help` (or render a one-figure test page in `/tmp`). Expected: no module-not-found error.
- [ ] **Step 5: Commit** `chore: vendor visual-explainer, markdown-mermaid-writing, ponytail, caveman skills`

### Task 5: Hub entry points

**Files:**
- Create: `README.md`: purpose (2–3 lines), "How to use this repo", table of contents (Foundations, Concepts, Project, Examples), and a link to the spec.
- Create: `llms.txt`: H1 `System Design 101`, a one-line blockquote summary, then H2 sections `Foundations`, `Concepts`, `Project`, `Examples`. Each lists `- [Title](path.md): one-line note`. Examples link to their folders' code files.
- Create: `CONTEXT.md`: glossary, in the domain-modeling `CONTEXT-FORMAT.md` style. Empty sections are OK until terms land.
- Create: `docs/_template.md`: the page template from the spec, with front matter `title`, `prerequisites: []`, `grounds: []`, `sources: []`.
- Create: `project/foodpanda/README.md`: build log. One row per step: step, service, concepts used (links). Row 1 is auth_service, with concepts "planned (M2)".
- Create: empty folders with `.gitkeep`: `docs/00-foundations/`, `docs/concepts/{networking,api,security,data,patterns,principles,concurrency,infra}/`, `docs/research/`, `html/`.

- [ ] **Step 1:** Write the files above.
- [ ] **Step 2:** Run `python3 scripts/check_links.py`. Expected: exit 0, no output.
- [ ] **Step 3:** Open `README.md` and `llms.txt` and check that every listed path exists.
- [ ] **Step 4:** Run `python3 scripts/check_links.py` once more over the whole repo, including the moved auth_service README. Fix any old-path links.
- [ ] **Step 5: Commit** `docs: add README, llms.txt, CONTEXT.md, page template, project build log`

**M0 checkpoint:** tell the user M0 is done. Show the new tree in one block.

### Task 6: Research "How a request travels" and get the concept brief approved

**Files:**
- Create: `docs/research/how-a-request-travels.md`

**Scope of the page:** from typing `google.com` to the request reaching the server's front door (gateway/ingress). Covers:
- the client's IP address (private vs public, NAT);
- domain registration (registrant → registrar → registry);
- DNS resolution (stub resolver, recursive resolver, root, TLD, authoritative; caching and TTL);
- the TCP handshake;
- the TLS 1.3 handshake;
- the HTTP request and response;
- where a load balancer or gateway sits.

Out of scope: inside the server (that's M2+).

- [ ] **Step 1:** Run the `mattpocock-skills:research` workflow. Use primary sources: RFC 1034, RFC 1035 (DNS); RFC 9293 (TCP); RFC 8446 (TLS 1.3); RFC 9110 (HTTP semantics); RFC 1918 (private addresses); ICANN pages on registrars and registries. Use Cloudflare Learning only to cross-check.
- [ ] **Step 2:** Write the note. One section per stage. Every claim is followed by its source (RFC number + section, or URL).
- [ ] **Step 3: Reason before writing.** List `prerequisites` (assume the reader knows: what a website and a browser are) and `grounds` (IP address, DNS, domain name, registrar, resolver, TTL, TCP, port, TLS, HTTP request, load balancer). Add these terms to `CONTEXT.md`.
- [ ] **Step 4: Concept brief.** Send the user 5–10 lines covering: the journey in order, the terms it grounds, the sources, and the 2–3 "Try it" commands (`dig google.com +trace`, `curl -v https://google.com`, `traceroute google.com`).
- [ ] **Step 5: GATE.** Wait for user approval or corrections. Apply corrections to the note.
- [ ] **Step 6: Commit** `docs(research): how a request travels`

### Task 7: Write the foundations page

**Files:**
- Create: `docs/00-foundations/01-how-a-request-travels.md` (from `docs/_template.md`)
- Modify: `llms.txt`, `README.md` (add the page), `CONTEXT.md` (final term wording)

- [ ] **Step 1:** Write the page from the research note, following the template and Global Constraints. "The picture" is one Mermaid `sequenceDiagram`: Browser, Resolver, Root, TLD, Authoritative, Server. Write it following `markdown-mermaid-writing`, including `accTitle`/`accDescr`.
- [ ] **Step 2:** "In our code": there's no code for this page yet. Write "None yet. The auth service in M2 is where the request lands." and link `project/foodpanda/services/auth_service/`.
- [ ] **Step 3:** Animation script: numbered steps, one claim each:
  1. Laptop with private IP behind router (NAT) → public IP.
  2. Browser asks the stub resolver for `google.com`.
  3. Cache miss: the recursive resolver walks root → `.com` TLD → authoritative.
  4. The IP comes back and is cached with its TTL.
  5. TCP 3-way handshake to port 443.
  6. TLS 1.3 handshake (1-RTT).
  7. HTTP GET.
  8. Load balancer/gateway.
  9. Response travels back.
- [ ] **Step 4: Verify.**
  - `python3 scripts/check_links.py` exits 0.
  - Every claim has a source in the research note.
  - Front matter `grounds` matches the `CONTEXT.md` entries.
- [ ] **Step 5: Commit** `docs: add foundations page 01, how a request travels`

### Task 8: Visual tooling spike and final visual

**Files:**
- Create (spike): `html/00-foundations/01-how-a-request-travels.visual-explainer.html` (+ its `.src.html`)
- Create (spike): `html/00-foundations/01-how-a-request-travels.plain-svg.html`: one self-contained file, inline SVG + CSS + a small JS stepper, no kit, no CDN.
- Modify: `docs/00-foundations/01-how-a-request-travels.md`: link to the chosen HTML.

**Both versions must:**
- implement the same 9-step animation script from Task 7;
- have Prev/Next step controls and keyboard arrows;
- show one caption per step;
- not rely on colour alone to show state.

- [ ] **Step 1:** Build the visual-explainer version per its `SKILL.md`, as a concept explainer page shape. Render with `node .claude/skills/visual-explainer/kit/render.mjs <file>.src.html`. Expected: no `✗` lines.
- [ ] **Step 2:** Build the plain-SVG version.
- [ ] **Step 3:** Screenshot step 1 and step 5 of each with headless Chrome. Send the 4 images and both HTML files to the user.
- [ ] **Step 4: GATE.** The user picks the default tool.
- [ ] **Step 5:** Rename the chosen file to `html/00-foundations/01-how-a-request-travels.html`. Delete the other version. Link it from the page's "The picture" section. Record the choice and reason in the spec (section 8) as a dated line.
- [ ] **Step 6:** Run `python3 scripts/check_links.py`. Expected: exit 0.
- [ ] **Step 7: Commit** `feat(html): visual for how a request travels; record visual tool choice`

### Task 9: Hand-off

- [ ] **Step 1:** Run `python3 -m pytest scripts/ -q` and `python3 scripts/check_links.py`. Both clean.
- [ ] **Step 2:** `git log --oneline main..` shows the task commits.
- [ ] **Step 3:** Ask the user to push, or to grant push access. Then open a PR titled "Learning hub: M0 setup + foundations page 01".
- [ ] **Step 4:** Propose the M2 plan: auth service concept pages.
