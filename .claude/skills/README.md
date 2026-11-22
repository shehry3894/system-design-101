# Vendored skills

Copies of agent skills this repo uses. Any Claude Code session opened here loads them.

| Skill | What we use it for | Source (commit) | Licence |
|---|---|---|---|
| `visual-explainer` | HTML visuals: SVG diagrams, step-by-step animations | [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) `plugins/visual-explainer` (`9d5f880`) | MIT |
| `markdown-mermaid-writing` | Markdown pages + Mermaid diagrams | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) `skills/markdown-mermaid-writing` (`ec59a29`) | Repo: MIT (`LICENSE.md`); skill front matter says Apache-2.0 |
| `ponytail` | Smallest code that fully works | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) `skills/ponytail` (`ebd8654`) | MIT |
| `caveman` | Short chat replies (never for pages) | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) `skills/caveman` (`70f4f34`) | MIT |

**visual-explainer setup:**
- Render a page: `node .claude/skills/visual-explainer/kit/render.mjs <page>.src.html`
- For the browser check, run this once first: `npm install --no-save --prefix .claude/skills/visual-explainer playwright-core`

To update a skill, copy the folder again from its source and update the commit here.
