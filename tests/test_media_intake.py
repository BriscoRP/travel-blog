"""Tests for the private Media Intake Foundation using synthetic images."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageCms
import yaml

from visit_capture import media_intake


VISIT_ID = "VIS-FICTION-MEDIA-0001"
PLACE_ID = "PLC-FICTION-PLACE-0001"


class FakeVisitStore:
    def __init__(self, place_id=PLACE_ID):
        self.place_id = place_id

    def load(self, visit_id):
        if visit_id != VISIT_ID:
            raise FileNotFoundError(visit_id)
        return {"visit_id": visit_id, "place_id": self.place_id}


class MediaIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temporary.name)
        self.private = self.root / "private"
        self.content = self.root / "content"
        self.public = self.root / "public"
        self.private.mkdir()
        self.content.mkdir()
        self.place = self.content / "fictional-place.md"
        self.place.write_text(
            f"---\ntitle: Fictional Place\nplace_id: {PLACE_ID}\nfictional: true\n"
            "review_only: true\npublication_status: review_prototype\n---\n"
            "Fictional body.\n",
            encoding="utf-8",
        )
        self.patch = patch.object(media_intake, "PLACE_CONTENT_ROOT", self.content)
        self.patch.start()
        self.visit_store = FakeVisitStore()

    def tearDown(self):
        self.patch.stop()
        self.temporary.cleanup()

    def image(self, name="selected.jpg", size=(1200, 800), format="JPEG", **save):
        path = self.private / name
        Image.new("RGB", size, (40, 120, 80)).save(path, format=format, **save)
        return path

    def plan(self, source, **overrides):
        arguments = {
            "place_path": self.place,
            "visit_id": VISIT_ID,
            "role": "hero",
            "alt": "A fictional green landscape used for testing.",
            "visit_store": self.visit_store,
            "public_root": self.public,
        }
        arguments.update(overrides)
        return media_intake.plan_image(source, **arguments)

    def apply(self, source, **overrides):
        arguments = {
            "place_path": self.place,
            "visit_id": VISIT_ID,
            "role": "hero",
            "alt": "A fictional green landscape used for testing.",
            "visit_store": self.visit_store,
            "public_root": self.public,
        }
        arguments.update(overrides)
        return media_intake.apply_image(source, **arguments)

    def metadata(self):
        text = self.place.read_text(encoding="utf-8")
        return yaml.safe_load(text.split("---", 2)[1])

    def test_valid_jpeg_and_png_are_accepted(self):
        for name, format in (("selected.jpg", "JPEG"), ("selected.png", "PNG")):
            with self.subTest(format=format):
                self.assertEqual(self.plan(self.image(name, format=format)).source_width, 1200)

    def test_prepared_webp_is_accepted(self):
        self.assertEqual(self.plan(self.image("selected.webp", format="WEBP")).source_width, 1200)

    def test_unsupported_and_corrupt_inputs_are_rejected(self):
        gif = self.image("selected.gif", format="GIF")
        corrupt = self.private / "corrupt.jpg"
        corrupt.write_bytes(b"not an image")
        for source in (gif, corrupt):
            with self.subTest(source=source.name), self.assertRaises(media_intake.MediaIntakeError):
                self.plan(source)

    def test_extension_content_mismatch_uses_actual_image_data(self):
        source = self.image("misnamed.jpg", format="PNG")
        self.assertEqual(self.plan(source).source_width, 1200)

    def test_exif_orientation_is_applied_before_metadata_is_stripped(self):
        source = self.private / "rotated.jpg"
        exif = Image.Exif()
        exif[274] = 6
        Image.new("RGB", (80, 120), "blue").save(source, exif=exif)
        plan = self.apply(source)
        self.assertEqual((plan.source_width, plan.source_height), (120, 80))
        output = self.public / plan.place_slug / plan.variants[-1].filename
        with Image.open(output) as derivative:
            self.assertEqual(derivative.size, (120, 80))
            self.assertEqual(len(derivative.getexif()), 0)

    def test_valid_icc_profile_is_transformed_to_srgb_then_removed(self):
        profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
        source = self.image(icc_profile=profile)
        before = source.read_bytes()
        transform = media_intake.ImageCms.profileToProfile
        with patch.object(
            media_intake.ImageCms, "profileToProfile", wraps=transform
        ) as colour_transform:
            plan = self.apply(source)
        self.assertGreaterEqual(colour_transform.call_count, 2)
        self.assertEqual(source.read_bytes(), before)
        for output in (self.public / plan.place_slug).glob("*.webp"):
            with Image.open(output) as derivative:
                self.assertNotIn("icc_profile", derivative.info)
                self.assertEqual(len(derivative.getexif()), 0)

    def test_invalid_icc_profile_fails_during_dry_run(self):
        source = self.image(icc_profile=b"not a valid colour profile")
        with self.assertRaisesRegex(media_intake.MediaIntakeError, "ICC colour profile"):
            self.plan(source)
        self.assertFalse(self.public.exists())

    def test_source_without_icc_profile_uses_existing_safe_path(self):
        source = self.image()
        with patch.object(
            media_intake.ImageCms,
            "profileToProfile",
            side_effect=AssertionError("unexpected colour transform"),
        ):
            plan = self.apply(source)
        self.assertEqual(len(list((self.public / plan.place_slug).glob("*.webp"))), 3)

    def test_aspect_ratio_widths_and_no_upscaling(self):
        plan = self.plan(self.image(size=(1200, 800)))
        self.assertEqual([item.width for item in plan.variants], [480, 800, 1200])
        self.assertEqual([item.height for item in plan.variants], [320, 533, 800])
        small = self.plan(self.image("small.png", size=(620, 310), format="PNG"))
        self.assertEqual([item.width for item in small.variants], [480, 620])
        tiny = self.plan(self.image("tiny.png", size=(320, 160), format="PNG"))
        self.assertEqual([item.width for item in tiny.variants], [320])

    def test_filename_is_deterministic_safe_and_does_not_leak_source_name(self):
        plan = self.plan(self.image("Private Family Upload 123.jpg"))
        self.assertEqual(
            [item.filename for item in plan.variants],
            [
                "fictional-place-hero-480.webp",
                "fictional-place-hero-800.webp",
                "fictional-place-hero-1200.webp",
            ],
        )
        self.assertNotIn("private", " ".join(item.filename for item in plan.variants))

    def test_unsafe_place_slug_is_rejected(self):
        unsafe = self.content / "Unsafe Place.md"
        unsafe.write_text(self.place.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaises(media_intake.MediaIntakeError):
            self.plan(self.image(), place_path=unsafe)

    def test_collision_and_second_hero_fail_without_overwrite(self):
        source = self.image()
        target = self.public / "fictional-place"
        target.mkdir(parents=True)
        collision = target / "fictional-place-hero-480.webp"
        collision.write_bytes(b"unrelated")
        with self.assertRaises(media_intake.MediaIntakeError):
            self.plan(source)
        self.assertEqual(collision.read_bytes(), b"unrelated")
        collision.unlink()
        self.apply(source)
        with self.assertRaises(media_intake.MediaIntakeError):
            self.plan(source)

    def test_alt_place_and_visit_are_explicitly_required(self):
        source = self.image()
        for overrides in ({"alt": ""}, {"alt": "words\non two lines"}, {"visit_id": ""}):
            with self.subTest(overrides=overrides), self.assertRaises(media_intake.MediaIntakeError):
                self.plan(source, **overrides)

    def test_visit_must_belong_to_explicit_place(self):
        with self.assertRaisesRegex(media_intake.MediaIntakeError, "does not belong"):
            self.plan(self.image(), visit_store=FakeVisitStore("PLC-OTHER-PLACE"))

    def test_private_source_must_be_outside_repository(self):
        with patch.object(media_intake, "REPOSITORY_ROOT", self.root):
            with self.assertRaises(media_intake.MediaIntakeError):
                self.plan(self.image())

    def test_dry_run_plans_without_public_or_content_changes(self):
        source = self.image()
        before = self.place.read_bytes()
        plan = self.plan(source)
        self.assertEqual(plan.destination, str(self.public / "fictional-place"))
        self.assertFalse(self.public.exists())
        self.assertEqual(self.place.read_bytes(), before)
        self.assertTrue(source.exists())

    def test_apply_creates_complete_set_and_metadata_but_keeps_source(self):
        source = self.image()
        plan = self.apply(source)
        outputs = sorted((self.public / plan.place_slug).glob("*.webp"))
        self.assertEqual(len(outputs), 3)
        hero = self.metadata()["hero_image"]
        self.assertEqual(hero["visit_id"], VISIT_ID)
        self.assertIn("480w", hero["srcset"])
        self.assertEqual(hero["width"], 1200)
        self.assertEqual(hero["height"], 800)
        self.assertTrue(source.exists())
        for output in outputs:
            with Image.open(output) as derivative:
                self.assertEqual(len(derivative.getexif()), 0)

    def test_processing_failure_leaves_no_partial_set_or_metadata(self):
        source = self.image()
        with patch.object(media_intake, "_render_variants", side_effect=OSError("failure")):
            with self.assertRaises(OSError):
                self.apply(source)
        self.assertFalse((self.public / "fictional-place").exists())
        self.assertNotIn("hero_image", self.metadata())

    def test_private_preview_is_outside_repository_and_not_public(self):
        source = self.image()
        plan = self.plan(source)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as preview_root:
            preview = media_intake.create_private_preview(
                source, plan, Path(preview_root) / "preview"
            )
            self.assertEqual(len(list(preview.glob("*.webp"))), 3)
        self.assertFalse(self.public.exists())


if __name__ == "__main__":
    unittest.main()
