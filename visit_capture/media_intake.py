"""Private, explicit image intake for public-safe Place derivatives."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import tempfile
import warnings

from PIL import Image, ImageOps, UnidentifiedImageError
import yaml

from .core import VisitStore, YamlVisitStore


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLACE_CONTENT_ROOT = REPOSITORY_ROOT / "src" / "content" / "places"
PUBLIC_MEDIA_ROOT = REPOSITORY_ROOT / "src" / "assets" / "places"
SAFE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VISIT_ID = re.compile(r"^VIS-[A-Z0-9][A-Z0-9-]{2,63}$")
SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_ALT_LENGTH = 300


@dataclass(frozen=True)
class ImageProfile:
    """Central delivery policy; values remain provisional until layout approval."""

    candidate_widths: tuple[int, ...]
    sizes: str
    webp_quality: int


HERO_IMAGE_PROFILE = ImageProfile(
    candidate_widths=(480, 800, 1200),
    sizes="(min-width: 74rem) 72rem, calc(100vw - 2rem)",
    webp_quality=82,
)


class MediaIntakeError(ValueError):
    """Raised when private media cannot be processed safely."""


@dataclass(frozen=True)
class MediaVariant:
    width: int
    height: int
    filename: str
    public_url: str


@dataclass(frozen=True)
class MediaPlan:
    place_slug: str
    visit_id: str
    role: str
    alt: str
    source_width: int
    source_height: int
    variants: tuple[MediaVariant, ...]
    destination: str


def default_private_intake() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        raise MediaIntakeError(
            "LOCALAPPDATA is unavailable; supply an explicit private source."
        )
    return Path(local_app_data) / "ProjectAtlas" / "media-intake"


def _ensure_private_source(source: Path) -> Path:
    resolved = source.expanduser().resolve()
    try:
        resolved.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise MediaIntakeError("Private source image must be outside the repository.")
    if not resolved.is_file():
        raise MediaIntakeError("Private source image was not found.")
    return resolved


def _ensure_private_directory(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError:
        return resolved
    raise MediaIntakeError("Private Visit store must be outside the repository.")


def _load_place(place_path: Path) -> tuple[dict, str, str]:
    resolved = place_path.resolve()
    try:
        resolved.relative_to(PLACE_CONTENT_ROOT.resolve())
    except ValueError as error:
        raise MediaIntakeError("Place content must be in the Atlas Place source directory.") from error
    slug = resolved.stem
    if not SAFE_SLUG.fullmatch(slug):
        raise MediaIntakeError("Place slug must be lowercase and URL-safe.")
    try:
        text = resolved.read_text(encoding="utf-8")
    except OSError as error:
        raise MediaIntakeError("Place content could not be read.") from error
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        raise MediaIntakeError("Place content has invalid front matter.")
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise MediaIntakeError("Place metadata must be a mapping.")
    return metadata, match.group(2), slug


def _validated_alt(alt: str) -> str:
    value = alt.strip()
    if not value or len(value) > MAX_ALT_LENGTH or "\n" in value:
        raise MediaIntakeError("Informative image alt text is required and must be concise.")
    return value


def _inspect_image(source: Path) -> tuple[int, int]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(source) as image:
                if image.format not in SUPPORTED_FORMATS:
                    raise MediaIntakeError("Only JPEG, PNG and WebP still images are supported.")
                image.verify()
            with Image.open(source) as image:
                oriented = ImageOps.exif_transpose(image)
                return oriented.size
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError,
            Image.DecompressionBombWarning) as error:
        raise MediaIntakeError("Source is corrupt, unsafe or not supported image data.") from error


def _variant_widths(source_width: int, profile: ImageProfile) -> tuple[int, ...]:
    widths = [width for width in profile.candidate_widths if width < source_width]
    widths.append(min(source_width, profile.candidate_widths[-1]))
    return tuple(dict.fromkeys(widths))


def plan_image(
    source: Path,
    *,
    place_path: Path,
    visit_id: str,
    role: str,
    alt: str,
    visit_store: VisitStore,
    public_root: Path = PUBLIC_MEDIA_ROOT,
) -> MediaPlan:
    source = _ensure_private_source(source)
    metadata, _, slug = _load_place(place_path)
    if role != "hero":
        raise MediaIntakeError("V1 Media Intake Foundation supports only the hero role.")
    if not VISIT_ID.fullmatch(visit_id):
        raise MediaIntakeError("An explicit valid Visit ID is required.")
    place_id = metadata.get("place_id")
    if not isinstance(place_id, str) or not place_id.startswith("PLC-"):
        raise MediaIntakeError("Place content requires an explicit opaque Place ID.")
    try:
        visit = visit_store.load(visit_id)
    except Exception as error:
        raise MediaIntakeError("The selected private Visit could not be loaded.") from error
    if visit.get("place_id") != place_id:
        raise MediaIntakeError("The selected Visit does not belong to the selected Place.")
    alt = _validated_alt(alt)
    if metadata.get("hero_image"):
        raise MediaIntakeError("This Place already has a hero image association.")
    source_width, source_height = _inspect_image(source)
    variants = []
    for width in _variant_widths(source_width, HERO_IMAGE_PROFILE):
        height = round(source_height * width / source_width)
        filename = f"{slug}-{role}-{width}.webp"
        variants.append(
            MediaVariant(
                width=width,
                height=height,
                filename=filename,
                public_url=f"/assets/places/{slug}/{filename}",
            )
        )
    destination = public_root / slug
    for variant in variants:
        if (destination / variant.filename).exists():
            raise MediaIntakeError("A planned public derivative already exists.")
    return MediaPlan(
        place_slug=slug,
        visit_id=visit_id,
        role=role,
        alt=alt,
        source_width=source_width,
        source_height=source_height,
        variants=tuple(variants),
        destination=str(destination),
    )


def _render_variants(source: Path, plan: MediaPlan, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
            for variant in plan.variants:
                resized = image.resize(
                    (variant.width, variant.height), Image.Resampling.LANCZOS
                )
                resized.save(
                    destination / variant.filename,
                    format="WEBP",
                    quality=HERO_IMAGE_PROFILE.webp_quality,
                    method=6,
                )


def _media_metadata(plan: MediaPlan) -> dict:
    largest = plan.variants[-1]
    return {
        "role": plan.role,
        "visit_id": plan.visit_id,
        "alt": plan.alt,
        "src": largest.public_url,
        "srcset": ", ".join(
            f"{item.public_url} {item.width}w" for item in plan.variants
        ),
        "sizes": HERO_IMAGE_PROFILE.sizes,
        "width": largest.width,
        "height": largest.height,
    }


def apply_image(
    source: Path,
    *,
    place_path: Path,
    visit_id: str,
    role: str,
    alt: str,
    visit_store: VisitStore,
    public_root: Path = PUBLIC_MEDIA_ROOT,
) -> MediaPlan:
    plan = plan_image(
        source,
        place_path=place_path,
        visit_id=visit_id,
        role=role,
        alt=alt,
        visit_store=visit_store,
        public_root=public_root,
    )
    source = _ensure_private_source(source)
    metadata, body, _ = _load_place(place_path)
    destination = public_root / plan.place_slug
    destination.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            prepared = Path(temporary)
            _render_variants(source, plan, prepared)
            for variant in plan.variants:
                target = destination / variant.filename
                if target.exists():
                    raise MediaIntakeError("A public derivative collision was detected.")
                os.replace(prepared / variant.filename, target)
                created.append(target)
        metadata["hero_image"] = _media_metadata(plan)
        rendered = "---\n" + yaml.safe_dump(
            metadata, sort_keys=False, allow_unicode=True
        ) + "---\n" + body
        descriptor, temporary_name = tempfile.mkstemp(
            dir=place_path.parent, prefix=f".{place_path.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, place_path)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
    except Exception:
        for path in created:
            path.unlink(missing_ok=True)
        if destination.exists() and not any(destination.iterdir()):
            destination.rmdir()
        raise
    return plan


def create_private_preview(source: Path, plan: MediaPlan, preview_root: Path) -> Path:
    resolved = preview_root.expanduser().resolve()
    try:
        resolved.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise MediaIntakeError("Private preview directory must be outside the repository.")
    destination = resolved / plan.place_slug
    if destination.exists():
        raise MediaIntakeError("Private preview destination already exists.")
    _render_variants(_ensure_private_source(source), plan, destination)
    return destination


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare one selected private image for Atlas.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--place", type=Path, required=True)
    parser.add_argument("--visit-id", required=True)
    parser.add_argument("--visit-store", type=Path, required=True)
    parser.add_argument("--role", choices=("hero",), required=True)
    parser.add_argument("--alt", required=True)
    parser.add_argument("--preview-dir", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(arguments)
    try:
        operation = apply_image if args.apply else plan_image
        visit_store_path = _ensure_private_directory(args.visit_store)
        plan = operation(
            args.source,
            place_path=args.place,
            visit_id=args.visit_id,
            role=args.role,
            alt=args.alt,
            visit_store=YamlVisitStore(visit_store_path),
        )
        if args.preview_dir and not args.apply:
            create_private_preview(args.source, plan, args.preview_dir)
    except (MediaIntakeError, OSError) as error:
        print(f"Media intake failed: {error}")
        return 1
    print(f"Place: {plan.place_slug}")
    print(f"Visit: {plan.visit_id}")
    print(f"Role: {plan.role}")
    print(f"Filename base: {plan.place_slug}-{plan.role}")
    print("Responsive widths: " + ", ".join(str(item.width) for item in plan.variants))
    print("Dimensions: " + ", ".join(f"{item.width}x{item.height}" for item in plan.variants))
    print(f"Alt text: {plan.alt}")
    print(f"Destination: src/assets/places/{plan.place_slug}")
    print(f"Applied: {'yes' if args.apply else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
