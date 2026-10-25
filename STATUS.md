# STATUS — manual-start-template

## What was built

A copy-ready template repo for publishing a beginner-friendly manual as a
static HTML site, in the house style of Asdale Dynamics, LLC:

- `build.py` — entire site generator, Python 3 standard library only
  (no pip installs, no network). Renders a friendly markdown subset to
  styled, navigable HTML: sidebar TOC, active-chapter highlight,
  Prev/Next pager, code fences with HTML escaping, inline bold/italic/
  code/links, blockquotes, numbered lists.
- `docs/` — book config (`book.md`), style guide (`WRITING-A-CHAPTER.md`),
  chapter skeleton (`skeleton/chapter-skeleton.md`), and three sample
  chapters: the tone-setting sample chapter, a plain-English glossary,
  and a worksheet chapter.
- `templates/` — blank glossary and worksheet templates to copy in.
- `README.md` — five-step tutorial crediting Asdale Dynamics, LLC.
- `RELEASE-CHECKLIST.md` — pre-release checks (content, build, tests,
  secrets scan).
- `LICENSE` — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `tests/` — 17 unittest cases: markdown renderer behavior + end-to-end
  build validation (index/chapter pages, nav chaining, active sidebar,
  no unrendered markdown, no secrets in output, CSS + book.json shipped).

## How to run it

```bash
python3 build.py                       # build site into out/
open out/index.html                    # read it
python3 -m unittest discover tests -v  # run the tests
```

## Verification results

- `python3 -m unittest discover tests -v` → **Ran 17 tests ... OK**
- `python3 build.py` → builds 4 pages into `out/` successfully
- Clean-copy check: repo copied to a fresh temp dir, `build.py` and the
  test suite both pass there on the first try (fully offline)
- Secrets scan: no keys/passwords/tokens in source or output; output
  includes a test asserting none of `api_key`, `apikey`, `password`,
  `sk-`, `bearer ` appear in built HTML
- No remote added, nothing pushed, nothing published

## Known gaps

- The markdown renderer covers a friendly subset (headings, lists,
  fenced code, quotes, rules, bold/italic/code, links). No tables,
  images, or nested lists yet — add and test before you need them.
- `build.py` emits relative links only, so the site works from
  `file://` and any static host, but no sitemap/RSS is generated.
- Chapter `summary:` front matter is stored in `book.json` but not yet
  rendered as intro text on chapter pages.
