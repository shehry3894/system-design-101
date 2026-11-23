---
title: <Decision name>
prerequisites: []   # pages or terms the reader needs first
grounds: []         # new terms this page explains (add them to CONTEXT.md)
---

# <Decision name: option A, option B, option C (alphabetical)>

## The problem
<1–2 sentences: what has to be decided, and why it matters.>

## The options
<Alphabetical order. Every option gets exactly these five bullets, about the same length. No "best" or "fastest" unless quoted from a source.>

### <Option A>
- **In real life:** <one everyday analogy, in our own words; one setting (e.g. a restaurant) across the whole page group; no citation>
- **What it is:** <one sentence, in its own source's words; the quote links to its source>
- **Pros:** <2–3 short points>
- **Cons:** <2–3 short points>
- **Use when:** <one sentence>

## Compare
<Each row is a question a developer asks. Each cell gives a concrete example where one exists, e.g. `GET /orders/42`. Over about 8 rows? Split into the two tables below.>

### Design
| | <A> | <B> | <C> |
|---|---|---|---|
| <what you build: contract, payload, ...> | <cell> | <cell> | <cell> |

### Run
| | <A> | <B> | <C> |
|---|---|---|---|
| <how it behaves in production: errors, timeouts, ...> | <cell> | <cell> | <cell> |

## Surprises
- <A fact most developers get wrong, with its source. About one per option. Never a reply to a video or other shared material.>

## Same task, each way
<One Mermaid diagram of the same task done each way. Then, for each option, one visible line on what the code shows, and the smallest code, run once before it goes on the page, folded in a `<details>` block:>

<details>
<summary>Code: <code><file name></code> and a call</summary>

```python
<code>
```

</details>

## Try it
<At most 3 commands, with their output.>

## Remember
- <bullet>
- <bullet>
- <bullet>

## Sources
<Every source the page uses. No [bracket] citations in the text: link a quote or a named source inline instead. The research note keeps a citation on every claim.>
- [<Title>](<primary source URL>)
