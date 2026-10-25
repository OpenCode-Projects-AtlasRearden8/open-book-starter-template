#!/usr/bin/env python3
"""Build a static HTML site from the markdown chapters in docs/.

Usage:
    python3 build.py            # build to out/
    python3 build.py --out DIR  # build to a custom directory

Uses only the Python standard library, so it runs offline with no installs.
Rerun this script any time you edit files under docs/ or assets/.
"""

import argparse
import datetime
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"
DEFAULT_OUT = ROOT / "out"

SUGGESTED_ORDER = 900
LEADING_NUMBER = re.compile(r"^(\d+)")


def parse_front_matter(text):
    """Read a simple 'key: value' header block at the top of a chapter file.

    Tolerates comment (`#`) lines and blank lines before the keys. Body
    splitting is best-effort: for config files only the keys matter.
    """
    meta = {}
    lines = text.splitlines()
    started = False
    end = len(lines)
    for i, raw in enumerate(lines[:20]):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            if started:
                break  # keys are one contiguous block; blank/comment ends it
            continue
        match = re.match(r"^(\w+):\s*(.*)$", stripped)
        if not match:
            if started:
                end = i
            else:
                end = i  # first plain prose line = start of the body
            break
        started = True
        if match.group(2).strip():
            meta[match.group(1).lower()] = match.group(2).strip()
        end = i + 1
    return meta, "\n".join(lines[end:])


def file_list(lines):
    """Turn a markdown bullet list (lines starting with - or *) into file names."""
    items = []
    for line in lines.splitlines():
        bullet = re.match(r"^[-*]\s+(.+)$", line.strip())
        if bullet:
            items.append(bullet.group(1).strip("` "))
    return items


def parse_book_config():
    """Read the simple key/value config at the top of docs/book.md."""
    text = (DOCS / "book.md").read_text(encoding="utf-8")
    meta, _ = parse_front_matter(text)
    return meta


def chapter_files(config):
    """Decide chapter order: explicit 'chapters:' list in book.md wins, else filename order."""
    text = (DOCS / "book.md").read_text(encoding="utf-8")
    _, body = split_at_marker(text)
    listed = file_list(body) if body.strip() else []
    paths = sorted(DOCS.glob("chapters/*.md"))
    if listed:
        found = [p for name in listed for p in paths if p.name.startswith(name) or p.stem == name]
        extra = [p for p in paths if p not in found]
        paths = found + extra
    else:
        paths = sorted(paths, key=lambda p: (numeric_prefix(p.name), p.name))
    return paths


def numeric_prefix(name):
    match = LEADING_NUMBER.match(name)
    return int(match.group(1)) if match else SUGGESTED_ORDER


def split_at_marker(text):
    parts = re.split(r"^-{3,}\s*$", text, maxsplit=1, flags=re.MULTILINE)
    return parts[0], parts[1] if len(parts) > 1 else ""


def inline(md):
    """Inline markdown: code spans, bold, italics, links."""
    text = html.escape(md, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    return text


def render_markdown(md):
    """Render a friendly subset of markdown to HTML. No dependencies, no surprises."""
    blocks = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            fence = line.strip()[3:]
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = ' class="language-%s"' % fence if fence else ""
            blocks.append("<pre%s><code>%s</code></pre>" % (cls, html.escape("\n".join(code))))
            continue
        if re.match(r"^#{1,4}\s", line):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            blocks.append("<h%d>%s</h%d>" % (level, inline(text), level))
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            blocks.append("<ul>%s</ul>" % "".join(items))
            continue
        if re.match(r"^\s*\d+[.)]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*\d+[.)]\s+", "", lines[i])))
                i += 1
            blocks.append("<ol>%s</ol>" % "".join(items))
            continue
        if line.strip() == "---":
            blocks.append("<hr>")
            i += 1
            continue
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(inline(lines[i].lstrip(">").strip()))
                i += 1
            blocks.append("<blockquote>%s</blockquote>" % "<br>".join(quote))
            continue
        if line.strip():
            para = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|```|\s*[-*]\s|\s*\d+[.)]\s|>|---)", lines[i + 1]):
                i += 1
                para.append(lines[i])
            blocks.append("<p>%s</p>" % inline(" ".join(p.strip() for p in para)))
        i += 1
    return "\n".join(blocks)


def chapter_slug(path, index):
    """Filename already numbered (01-foo.md)? Use it as-is; otherwise number by position."""
    if LEADING_NUMBER.match(path.stem):
        return path.stem
    return "%02d-%s" % (index + 1, path.stem)


def build_chapters(config):
    chapters = chapter_files(config)
    toc = []
    pages = []
    for index, path in enumerate(chapters):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)
        title = meta.get("title", path.stem.lstrip("0123456789-").replace("-", " ").title() or "Untitled")
        if not meta:
            first_heading = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = first_heading.group(1).strip() if first_heading else title
        slug = chapter_slug(path, index) + ".html"
        body_html = render_markdown(body)
        toc.append({"title": title, "file": slug})
        pages.append({"title": title, "file": slug, "index": index, "html": body_html,
                      "summary": meta.get("summary", "")})
    for page in pages:
        pos = page["index"]
        page["prev"] = toc[pos - 1]["file"] if pos > 0 else None
        page["next"] = toc[pos + 1]["file"] if pos + 1 < len(toc) else None
    return toc, pages


def page_template(config, title, content, toc, active=None, prev=None, next=None):
    book_title = config.get("title", "My Manual")
    author = config.get("author", "")
    toc_html = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (t["file"], ' class="active"' if t["file"] == active else "", html.escape(t["title"]))
        for t in toc
    )
    nav = []
    if prev:
        nav.append('<a class="nav-btn" href="%s">&larr; Previous</a>' % prev)
    if next:
        nav.append('<a class="nav-btn" href="%s">Next &rarr;</a>' % next)
    return PAGE_SHELL % {
        "book": html.escape(book_title),
        "author": html.escape(author),
        "title": html.escape(title),
        "toc": toc_html,
        "content": content,
        "nav": "\n".join(nav),
        "year": datetime.date.today().year,
    }


def write_pages(config, toc, pages, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        content = '<main class="chapter"><article>' + page["html"] + "</article>"
        nav = []
        if page["prev"]:
            nav.append('<a class="nav-btn" href="%s">&larr; Previous</a>' % page["prev"])
        if page["next"]:
            nav.append('<a class="nav-btn" href="%s">Next &rarr;</a>' % page["next"])
        content += '<nav class="pager">%s</nav></main>' % "\n".join(nav)
        (out_dir / page["file"]).write_text(
            page_template(config, page["title"], content, toc, active=page["file"]), encoding="utf-8")
    content = "<main class='chapter'><h1>%s</h1><p>A calm, friendly manual built from plain markdown.</p><ol class='big-toc'>%s</ol></main>" % (
        html.escape(config.get("title", "My Manual")),
        "".join('<li><a href="%s">%s</a></li>' % (t["file"], html.escape(t["title"])) for t in toc),
    )
    (out_dir / "index.html").write_text(page_template(config, "Home", content, toc), encoding="utf-8")
    if (ASSETS / "style.css").exists():
        shutil.copy(ASSETS / "style.css", out_dir / "style.css")
    (out_dir / "book.json").write_text(
        json.dumps({"title": config.get("title", ""), "author": config.get("author", ""), "toc": toc}, indent=2),
        encoding="utf-8")


PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s — %(book)s</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <a class="home" href="index.html">%(book)s</a>
  <span class="author">%(author)s</span>
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Table of contents"><ol>%(toc)s</ol></nav>
  %(content)s
</div>
<footer><a href="https://github.com/Asdale-Dynamics">Asdale Dynamics, LLC</a> · <span>© %(year)s · MIT License</span></footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build the manual site (offline, stdlib only).")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default: out/)")
    args = parser.parse_args()
    out_dir = Path(args.out)
    if not DOCS.exists():
        print("error: docs/ folder not found", file=sys.stderr)
        return 1
    config = parse_book_config()
    toc, pages = build_chapters(config)
    write_pages(config, toc, pages, out_dir)
    print("Built %d chapter file(s) into %s" % (len(toc) + 1, out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
