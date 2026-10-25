"""End-to-end tests: run the real build and validate the generated site."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build as build_mod  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class BuiltSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "out"
        config = build_mod.parse_book_config()
        cls.toc, cls.pages = build_mod.build_chapters(config)
        build_mod.write_pages(config, cls.toc, cls.pages, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def read(self, name):
        return (self.out / name).read_text(encoding="utf-8")

    def test_index_exists_and_lists_book(self):
        html_out = self.read("index.html")
        self.assertIn("The Massive AI Manual", html_out)
        self.assertIn("Asdale Dynamics, LLC", html_out)
        self.assertIn("MIT License", html_out)

    def test_every_chapter_has_a_page(self):
        titles = [p["title"] for p in self.pages]
        self.assertIn("What Is AI, Really? (A Friend's Version)", titles)
        self.assertIn("Glossary — Plain English Only", titles)
        self.assertIn("Worksheets — Try It Yourself", titles)
        for page in self.pages:
            self.assertTrue(page["html"].strip(), "empty chapter: %s" % page["title"])

    def test_sample_chapter_content_survives(self):
        first = self.pages[0]["html"]
        self.assertIn("<h2>Walk it through, step by step</h2>", first)
        self.assertIn("<ol>", first)
        self.assertIn("Ask it something", first)

    def test_navigation_links_chain(self):
        for page in self.pages:
            html_out = self.read(page["file"])
            self.assertIn('class="nav-btn"', html_out)
            if page["next"]:
                self.assertIn('href="%s"' % page["next"], html_out)
            if page["prev"]:
                self.assertIn('href="%s"' % page["prev"], html_out)

    def test_sidebar_highlights_active_chapter(self):
        page = self.pages[0]
        html_out = self.read(page["file"])
        self.assertIn('class="active"', html_out)

    def test_stylesheet_and_metadata_shipped(self):
        self.assertTrue((self.out / "style.css").exists())
        self.assertIn("font-family", (self.out / "style.css").read_text(encoding="utf-8"))
        meta = (self.out / "book.json").read_text(encoding="utf-8")
        self.assertIn("The Massive AI Manual", meta)

    def test_no_secrets_in_built_output(self):
        for path in self.out.glob("*.html"):
            text = path.read_text(encoding="utf-8").lower()
            for banned in ("api_key", "apikey", "password", "sk-", "bearer "):
                self.assertNotIn(banned, text)

    def test_no_unrendered_markdown_in_output(self):
        first = self.pages[0]["html"]
        self.assertNotIn("## ", first)
        self.assertNotIn("**", first)


if __name__ == "__main__":
    unittest.main()
