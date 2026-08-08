"""Checks for fictional, non-publishable Place review pages."""

from pathlib import Path
import unittest

from PIL import Image

import build


ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
REVIEW_SLUGS = (
    "bluebell-wood",
    "hadleigh-country-park",
    "willowmere-loop",
    "glasshouse-gardens",
    "lantern-quay",
)
GENUINE_REVIEW_SLUGS = {"bluebell-wood", "hadleigh-country-park"}


class FictionalPlaceBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build_site()

    def test_all_protected_place_reviews_are_built(self):
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
                if slug in GENUINE_REVIEW_SLUGS:
                    self.assertIn(
                        "Genuine visit · review only · not approved for publication",
                        page,
                    )
                else:
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
            if path.is_file() and path.suffix.lower() in {".html", ".css", ".xml", ".txt"}:
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("googleapis.com", content)
                self.assertNotIn("docs.google.com", content)

    def test_fictional_hero_has_complete_responsive_image_markup(self):
        page = (DIST / "places" / "glasshouse-gardens" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('class="place-hero-image"', page)
        self.assertIn('glasshouse-gardens-hero-480.webp 480w', page)
        self.assertIn('glasshouse-gardens-hero-800.webp 800w', page)
        self.assertIn('glasshouse-gardens-hero-1200.webp 1200w', page)
        self.assertIn('sizes="(min-width: 74rem) 72rem, calc(100vw - 2rem)"', page)
        self.assertIn('width="1200"', page)
        self.assertIn('height="800"', page)
        self.assertIn('fetchpriority="high"', page)
        self.assertNotIn('loading="lazy"', page)
        self.assertIn(
            'alt="A fictional illustrated garden landscape with green hills and a golden sun."',
            page,
        )

    def test_built_fictional_hero_variants_have_no_exif(self):
        root = DIST / "assets" / "places" / "glasshouse-gardens"
        variants = sorted(root.glob("*.webp"))
        self.assertEqual(len(variants), 3)
        for path in variants:
            with self.subTest(path=path.name), Image.open(path) as image:
                self.assertEqual(len(image.getexif()), 0)

    def test_genuine_review_keeps_private_evidence_out_of_public_output(self):
        for slug in GENUINE_REVIEW_SLUGS:
            page = (DIST / "places" / slug / "index.html").read_text(
                encoding="utf-8"
            )
            with self.subTest(slug=slug):
                self.assertNotIn("drive.google.com", page)
                self.assertNotIn("docs.google.com", page)
                self.assertNotIn("RSP-", page)
                self.assertNotIn("EVD-", page)
                self.assertNotIn("VIS-", page)
                self.assertNotIn("hero_image", page)


if __name__ == "__main__":
    unittest.main()
