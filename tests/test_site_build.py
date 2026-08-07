"""Checks for fictional, non-publishable Place review pages."""

from pathlib import Path
import unittest

import build


ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
REVIEW_SLUGS = (
    "willowmere-loop",
    "glasshouse-gardens",
    "lantern-quay",
)


class FictionalPlaceBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build_site()

    def test_three_fictional_place_reviews_are_built(self):
        for slug in REVIEW_SLUGS:
            with self.subTest(slug=slug):
                self.assertTrue((DIST / "places" / slug / "index.html").is_file())

    def test_every_review_page_is_noindex_and_visibly_fictional(self):
        for slug in REVIEW_SLUGS:
            page = (DIST / "places" / slug / "index.html").read_text(
                encoding="utf-8"
            )
            with self.subTest(slug=slug):
                self.assertIn(
                    '<meta name="robots" content="noindex, nofollow">', page
                )
                self.assertIn(
                    "Fictional · review only · not approved for publication",
                    page,
                )
                self.assertNotIn("rel=\"canonical\"", page)

    def test_review_pages_are_excluded_from_sitemap(self):
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        for slug in REVIEW_SLUGS:
            self.assertNotIn(slug, sitemap)

    def test_public_build_contains_no_google_connectivity(self):
        for path in DIST.rglob("*"):
            if path.is_file():
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("googleapis.com", content)
                self.assertNotIn("docs.google.com", content)


if __name__ == "__main__":
    unittest.main()
