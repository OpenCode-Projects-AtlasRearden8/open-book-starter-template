# WRITING A CHAPTER — the Asdale way

Read this once before writing. The template repo exists so your manual
has a **consistent tone**: plain English, step by step, never condescending.

## The five rules

1. **Friend, not guru.** Write the way you'd explain it to a colleague you
   like. Short sentences. "You" more than "the user".
2. **One real win per chapter.** The reader finishes the chapter having
   *done* something, not just *read* something.
3. **Steps, not paragraphs**, where action is involved. Number them.
4. **Translate every term.** First use = plain-English definition. If a
   term survives a whole chapter, add it to the glossary chapter.
5. **Doubt is a feature.** Show where AI (or a tool) might be wrong and
   how to double-check. Never pretend a tool is magic.

## Anatomy of a chapter

Copy `docs/skeleton/chapter-skeleton.md` and fill in:

- Title + one-sentence warm summary (front matter at top, key: value lines)
- `What you'll learn` — 2–4 concrete bullets
- `Start with the why` — 2–4 sentences on why this matters today
- `Walk it through, step by step` — numbered, one action per step
- `Watch out for this` — the classic mistake + the friendly fix
- `Try it yourself` — points at the worksheets chapter
- `In plain English` — a short recap paragraph

## Naming and order

- Files: `01-topic-name.md`, `02-next-topic.md` — the number sets reading
  order. No number = goes last.
- Slugs come from the filename; keep them short and real: what the
  reader will say out loud when recommending it.

## Tone checklist (grabbed from real experience)

- Would this sentence sound condescending read out loud? Fix it.
- Is there a concrete example the reader can copy in full? Add one.
- Could a reader do this with a cup of coffee going cold? Good length.
- Anything medical, financial, or legal? Keep it educational, point to a
  real professional. Never advice.

## Misc conventions

- Local files use relative links: `[the glossary](02-glossary.html)` —
  note the `.html`, since the site is static.
- Code examples live inside triple backticks and should be copyable whole.
- Prefer tables of terms in the glossary as short bold term + 1–2 sentence
  entries (that's what the chapter does — check `02-glossary.md`).
