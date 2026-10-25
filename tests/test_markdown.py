"""Unit tests for the markdown renderer inside build.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build as build_mod  # noqa: E402


class MarkdownRendering(unittest.TestCase):
    def test_headings(self):
        html_out = build_mod.render_markdown("# Big\n## Small")
        self.assertIn("<h1>Big</h1>", html_out)
        self.assertIn("<h2>Small</h2>", html_out)

    def test_paragraph(self):
        html_out = build_mod.render_markdown("First paragraph.\n\nSecond paragraph.")
        self.assertEqual(html_out.count("<p>"), 2)

    def test_bullet_and_numbered_lists(self):
        html_out = build_mod.render_markdown("- a\n- b\n\n1. one\n2. two")
        self.assertIn("<ul><li>a</li><li>b</li></ul>", html_out.replace("\n", ""))
        self.assertIn("<ol><li>one</li><li>two</li></ol>", html_out.replace("\n", ""))

    def test_inline_styles(self):
        html_out = build_mod.render_markdown("**bold** *soft* `tidy` [click me](x.html)")
        self.assertIn("<strong>bold</strong>", html_out)
        self.assertIn("<em>soft</em>", html_out)
        self.assertIn("<code>tidy</code>", html_out)
        self.assertIn('<a href="x.html">click me</a>', html_out)

    def test_code_block_escapes_html(self):
        html_out = build_mod.render_markdown("```text\n_slices <tag> & *__not markdown__\n```")
        self.assertIn("&lt;tag&gt;", html_out)
        self.assertNotIn("<tag>", html_out)
        self.assertIn("__not markdown__", html_out)  # untouched inside fences

    def test_blockquote_and_rule(self):
        html_out = build_mod.render_markdown("> like a friend\n\n---")
        self.assertIn("<blockquote>like a friend</blockquote>", html_out)
        self.assertIn("<hr>", html_out)


class FormatterHelpers(unittest.TestCase):
    def test_front_matter_is_optional(self):
        meta, body = build_mod.parse_front_matter("No\nfront matter here")
        self.assertEqual(meta, {})
        self.assertIn("front matter", body)

    def test_front_matter_keys_are_lowercase(self):
        meta, _ = build_mod.parse_front_matter("Title: Hello\nsummary: ok\n\nbody")
        self.assertEqual(meta["title"], "Hello")
        self.assertEqual(meta["summary"], "ok")

    def test_multi_heading_in_one_block(self):
        html_out = build_mod.render_markdown("## A\n## B\n1. step")
        self.assertIn("<h2>A</h2>", html_out)
        self.assertIn("step", html_out)


if __name__ == "__main__":
    unittest.main()
