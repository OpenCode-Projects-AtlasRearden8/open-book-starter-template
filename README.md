# Write your manual the Asdale way

A copy-ready template repo for publishing your own beginner-friendly
manual as a static HTML site — plain English, step by step, never
condescending. Maintained as an example of the house style of
**Asdale Dynamics, LLC** (Dylan Asdale's small press).

- No frameworks, no installs, no internet needed to build.
- One build script (Python 3, standard library only) turns markdown
  chapters in `docs/` into a polished, styled, navigable site in `out/`.
- MIT licensed — copy it, rename it, make it yours.

## Repository layout

```
README.md                  this tutorial
LICENSE                    MIT, Copyright (c) 2026 Asdale Dynamics, LLC
build.py                   the whole site generator (stdlib only)
assets/style.css           warm, readable stylesheet
docs/
  book.md                  book config: title, author, reading order
  WRITING-A-CHAPTER.md     the house style guide ("like a friend would")
  skeleton/chapter-skeleton.md   copy-paste starter for new chapters
  chapters/                your chapters (markdown, numbered: 01-, 02-...)
out/                       build output (gitignored; run build.py to make it)
templates/                 blank glossary + worksheet templates to copy
tests/test_build.py        tests that validate the build output
RELEASE-CHECKLIST.md       pre-release checks before you share the book
```

## Quickstart (offline, first try)

```bash
python3 build.py
```

Then open `out/index.html` in a browser. That's the whole thing.

## Tutorial: publish your manual in five small steps

### Step 1 — Name your book

Open `docs/book.md` and set `title`, `author`, and a one-line `summary`.
Keep the `chapters:` list empty and chapter order comes from the number
prefixes in the filenames (`01-…`, `02-…`).

### Step 2 — Write your first chapter

Copy `docs/skeleton/chapter-skeleton.md` to
`docs/chapters/01-what-my-book-is.md` and fill in the blanks. Read
`docs/WRITING-A-CHAPTER.md` once — it's short and it's the whole style
guide. The example chapter `docs/chapters/01-what-is-ai-really.md` shows
the exact tone to aim for.

### Step 3 — Add a glossary and worksheets

Blank templates live in `templates/`. Copy them into `docs/chapters/`
(e.g. `04-glossary.md`) and fill in. A good glossary entry is **bold term**
plus one or two friendly sentences. Worksheets are 3-minute tasks, one per
chapter — small wins, not homework.

### Step 4 — Build and skim

```bash
python3 build.py
```

Open `out/index.html`. Check the sidebar order, skim your chapter, and
click Prev/Next. Every chapter gets a navigation sidebar automatically.

### Step 5 — Pass the tests, then release

```bash
python3 -m unittest discover tests -v
```

All green? Walk through `RELEASE-CHECKLIST.md`, commit, and tag your
release. Done — that's a book.

## Tests

`tests/test_build.py` builds the real markdown render and asserts on the
generated HTML: chapters exist, headings render, links and code fences
survive, the index page contains the book title, and the output contains
no unescaped markdown syntax. Run them any time you touch the builder or
your chapters:

```bash
python3 -m unittest discover tests -v
```

## Detachable notes

- **Front matter friendly.** Chapters use a tiny `title:` / `summary:`
  header block so the generator doesn't need YAML — it's markdown everywhere.
- **No secrets, no personal data.** The docs and tests contain none, and
  the build never phones home.
- MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
  Credit: template and house style by Asdale Dynamics, LLC —
  see Dylan Asdale's hub at dylanasdale.github.io.
