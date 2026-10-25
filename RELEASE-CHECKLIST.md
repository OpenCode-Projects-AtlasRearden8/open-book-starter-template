# RELEASE CHECKLIST — walk through this before you share the book

## Content
- [ ] `docs/book.md` has your real title, author, and summary
- [ ] Chapter list reads well: each title is something you'd say out loud
- [ ] Every chapter has a `summary:` line (it becomes intro text later)
- [ ] Glossary entries are plain English, 1–2 sentences each
- [ ] Worksheets are doable in ~3 minutes each
- [ ] No medical/financial/legal advice — educational only, points to pros
- [ ] No secrets, API keys, or personal data anywhere in the repo
  (`grep -rniE "api[_-]?key|password|token|secret" --exclude-dir=.git .`)

## Build
- [ ] `python3 build.py` succeeds on a clean clone
- [ ] `out/index.html` opens in a browser and looks right (mobile too)
- [ ] Every sidebar link goes somewhere; no dead Prev/Next buttons
- [ ] Code examples render in boxes and are copyable whole

## Tests
- [ ] `python3 -m unittest discover tests -v` — all green

## Release
- [ ] Version noted (git tag like `v0.1.0`)
- [ ] Ship only `out/` folder as the static site (works from `file://` and
      any static host)
- [ ] Credit kept: "Asdale Dynamics, LLC" in README; MIT LICENSE header:
      Copyright (c) 2026 Asdale Dynamics, LLC
- [ ] Never commit `out/` (it's gitignored)
