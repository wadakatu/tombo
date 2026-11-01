#!/usr/bin/env python3
"""Regression checks for the generated agent reference, without network access."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_agent_docs as docs


class AgentDocsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        self.source = self.root / "docs/guide.md"
        self.source.write_text("# Guide\n\n[Example](../example.html#form)\n")
        (self.root / "example.html").write_text('<section id="form"></section>')
        self.patch = patch.object(docs, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.sources = patch.object(docs, "SOURCES", [("docs/guide.md", "Guide", "Usage")])
        self.sources.start()
        self.addCleanup(self.sources.stop)

    def test_resolves_links_and_preserves_code(self):
        sample = '```html\n[Example](missing.html)\n```\n'
        self.source.write_text(self.source.read_text() + sample)
        output = docs.render()["llms-full.txt"]
        self.assertIn(docs.BASE + "example.html#form", output)
        self.assertIn(sample, output)
        self.assertEqual(docs.render(), docs.render())

    def test_missing_nested_reference_fails(self):
        (self.root / "example.html").unlink()
        with self.assertRaisesRegex(ValueError, "Missing link target"):
            docs.render()

    def test_repository_root_links_keep_repository_prefix(self):
        self.source.write_text('[Example](/example.html?view=full#form)\n')
        output = docs.render()["llms-full.txt"]
        self.assertIn(f'[Example]({docs.BASE}example.html?view=full#form)', output)

    def test_root_link_preserves_encoded_path(self):
        (self.root / "docs/usage notes.md").write_text("# Notes\n")
        self.assertEqual(
            docs.resolve_link("docs/guide.md", "/docs/usage%20notes.md#notes"),
            docs.BASE + "docs/usage%20notes.md#notes",
        )

    def test_missing_root_reference_fails(self):
        with self.assertRaisesRegex(ValueError, "Missing link target"):
            docs.resolve_link("docs/guide.md", "/missing.md")

    def test_missing_indexed_source_fails(self):
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "Missing indexed source"):
            docs.render()

    def test_outside_repository_fails(self):
        for link in ("../../outside.md", "/../outside.md", "/%2e%2e/outside.md"):
            with self.subTest(link=link), self.assertRaisesRegex(ValueError, "escapes repository"):
                docs.resolve_link("docs/guide.md", link)

    def test_external_and_directory_links(self):
        for link in ("https://example.com/guide", "mailto:team@example.com"):
            self.assertEqual(docs.resolve_link("docs/guide.md", link), link)
        self.assertEqual(docs.resolve_link("docs/guide.md", "../docs/"), docs.BASE + "docs/")
        self.assertEqual(docs.resolve_link("docs/guide.md", "/docs/"), docs.BASE + "docs/")
        self.assertEqual(docs.resolve_link("docs/guide.md", "//example.com/guide"), "https://example.com/guide")


if __name__ == "__main__":
    unittest.main()
