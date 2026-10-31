"""Regression checks for stale published measurements and malformed markers."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import check_size


class PublishedSizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, _ in check_size.BUDGET:
            (self.root / name).write_text("test asset\n")
        self.source = "unchanged before\n" + "\n".join(
            f"<!-- size:{key} -->stale<!-- /size:{key} -->"
            for key in check_size.page_values({"tombo.css": 1000, "tombo.js": 100})
        ) + "\nunchanged after"
        for name in check_size.PAGES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.source)

    def run_gate(self, *args):
        with patch.object(check_size, "ROOT", self.root), patch("sys.argv", ["check_size.py", *args]), contextlib.redirect_stdout(io.StringIO()):
            return check_size.main()

    def test_stale_values_fail_and_write_repairs_both_pages(self):
        self.assertEqual(self.run_gate(), 1)
        self.assertEqual((self.root / "index.html").read_text(), self.source)
        self.assertEqual(self.run_gate("--write"), 0)
        self.assertEqual(self.run_gate(), 0)
        for name in check_size.PAGES:
            result = (self.root / name).read_text()
            self.assertNotIn("stale", result)
            self.assertTrue(result.startswith("unchanged before\n"))
            self.assertTrue(result.endswith("\nunchanged after"))

    def test_one_stale_translation_fails(self):
        self.run_gate("--write")
        (self.root / "ja/index.html").write_text(self.source)
        self.assertEqual(self.run_gate(), 1)

    def test_missing_duplicate_or_reversed_markers_fail(self):
        start, end = "<!-- size:css-label -->", "<!-- /size:css-label -->"
        for source in (self.source.replace(start, ""), self.source + start, self.source.replace(start + "stale" + end, end + "stale" + start)):
            with self.subTest(source=source):
                (self.root / "index.html").write_text(source)
                self.assertEqual(self.run_gate("--write"), 1)

    def test_write_does_not_bypass_budget(self):
        with patch.object(check_size, "BUDGET", [("tombo.css", 1), ("tombo.js", 1)]):
            self.assertEqual(self.run_gate("--write"), 1)


if __name__ == "__main__":
    unittest.main()
