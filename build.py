import os
from pathlib import Path
import re
import shutil

import markdown
from PIL import Image
import yaml
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT_DIR = Path(__file__).parent
CONTENT_DIR = ROOT_DIR / "src" / "content" / "places"
IMAGE_DIR = ROOT_DIR / "src" / "images"
TEMPLATE_DIR = ROOT_DIR / "src" / "templates"
STYLE_DIR = ROOT_DIR / "src" / "styles"
DIST_DIR = ROOT_DIR / "dist"
ASSET_DIR = DIST_DIR / "assets"

SITE_NAME = "Project Atlas"
SITE_URL = os.environ.get("ATLAS_SITE_URL", "").rstrip("/")

FALLBACK_MAPS = {
    "terrain": {
        "muddy_woodland": "Muddy Woodland Tracks",
        "coastal_paths": "Coastal Paths & Sand",
        "paved_paths": "Paved Paths & Parks",
        "open_fields": "Open Grassy Fields",
    },
    "parking": {
        "free_onsite": "Free On-Site",
        "paid_parking": "Paid Parking",
        "layby_only": "Layby Only",
        "no_parking": "No Dedicated Parking",
    },
    "dogs": {
        "highly_friendly": "Highly Dog Friendly",
        "lead_only": "Dogs on Lead Only",
        "no_dogs": "No Dogs Allowed",
    },
    "category": {
        "outings": "Outings & Walks",
        "historic": "Historic Sites",
        "day_trips": "Day Trips",
    },
    "tags": {
        "woodland": "Woodland",
        "water": "Water / River",
        "local_essex": "Local Essex",
        "hilly": "Hilly Terrain",
    },
}

PAGES = (
    {
        "template": "index.html",
        "output": "index.html",
        "current": "home",
        "title": "Project Atlas | Genuine family travel experiences",
        "description": (
            "Project Atlas preserves and shares genuine family travel experiences "
            "through carefully reviewed, first-hand guides."
        ),
        "path": "/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
    {
        "template": "places.html",
        "output": "places/index.html",
        "current": "places",
        "title": "Places | Project Atlas",
        "description": (
            "The Project Atlas collection is being carefully prepared. "
            "No Place guides are currently published."
        ),
        "path": "/places/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
    {
        "template": "about.html",
        "output": "about/index.html",
        "current": "about",
        "title": "About Project Atlas",
        "description": (
            "Learn why Project Atlas preserves genuine family journeys and how "
            "human editorial review keeps every published guide trustworthy."
        ),
        "path": "/about/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
    {
        "template": "guides.html",
        "output": "how-we-create-our-guides/index.html",
        "current": "",
        "title": "How We Create Our Guides | Project Atlas",
        "description": (
            "See how genuine family visits, responsible AI assistance and human "
            "editorial review shape every Project Atlas guide."
        ),
        "path": "/how-we-create-our-guides/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
    {
        "template": "privacy.html",
        "output": "privacy/index.html",
        "current": "",
        "title": "Privacy | Project Atlas",
        "description": (
            "Read how the Project Atlas public website protects visitor privacy "
            "and keeps private family evidence separate."
        ),
        "path": "/privacy/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
    {
        "template": "accessibility.html",
        "output": "accessibility/index.html",
        "current": "",
        "title": "Accessibility | Project Atlas",
        "description": (
            "Read about the Project Atlas commitment to a clear, inclusive and "
            "accessible visitor experience."
        ),
        "path": "/accessibility/",
        "robots": "noindex, nofollow",
        "include_in_sitemap": False,
    },
)


def resolve_value(field, key):
    """Return the prototype's human-readable label for a stored key."""
    if field in FALLBACK_MAPS and key in FALLBACK_MAPS[field]:
        return FALLBACK_MAPS[field][key]
    return str(key).replace("_", " ").title()


def process_image(image_filename):
    """Create the prototype's metadata-stripped WebP derivative."""
    source = IMAGE_DIR / image_filename
    destination_name = f"{source.stem}.webp"
    destination = ASSET_DIR / destination_name

    if not source.exists():
        print(f"Warning: Source image {image_filename} not found.")
        return f"/assets/{destination_name}", 800, 600

    try:
        with Image.open(source) as image:
            width, height = image.size
            clean_image = Image.new(image.mode, image.size)
            clean_image.putdata(image.getdata())
            clean_image.save(destination, "WEBP", quality=82)
            print(
                f"Optimized Image: {destination_name} "
                f"({width}x{height}) EXIF completely stripped."
            )
            return f"/assets/{destination_name}", width, height
    except Exception as error:
        print(f"Error processing image {image_filename}: {error}")
        return f"/assets/{destination_name}", 800, 600


def load_prototype_posts():
    """Load the existing prototype content format when content is present."""
    posts = []
    if not CONTENT_DIR.exists():
        return posts

    for file_path in sorted(CONTENT_DIR.glob("*.md")):
        content_text = file_path.read_text(encoding="utf-8")
        match = re.match(
            r"^---\s*\n(.*?)\n---\s*\n(.*)$",
            content_text,
            re.DOTALL,
        )
        if not match:
            continue

        metadata = yaml.safe_load(match.group(1)) or {}
        metadata["resolved_terrain"] = resolve_value(
            "terrain", metadata.get("terrain")
        )
        metadata["resolved_parking"] = resolve_value(
            "parking", metadata.get("parking")
        )
        metadata["resolved_dogs"] = resolve_value("dogs", metadata.get("dogs"))
        metadata["resolved_category"] = resolve_value(
            "category", metadata.get("category")
        )
        metadata["resolved_tags"] = [
            resolve_value("tags", tag) for tag in metadata.get("tags", [])
        ]
        metadata["slug"] = file_path.stem
        metadata["body"] = markdown.markdown(match.group(2))

        if metadata.get("thumbnail"):
            image_file = Path(metadata["thumbnail"]).name
            image_url, width, height = process_image(image_file)
            metadata["webp_thumbnail"] = image_url
            metadata["img_width"] = width
            metadata["img_height"] = height

        posts.append(metadata)

    posts.sort(key=lambda item: str(item.get("date", "")), reverse=True)
    return posts


def render_pages(environment, posts):
    for page in PAGES:
        destination = DIST_DIR / page["output"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        template = environment.get_template(page["template"])
        destination.write_text(
            template.render(
                site_name=SITE_NAME,
                canonical=f"{SITE_URL}{page['path']}" if SITE_URL else "",
                posts=posts,
                now=datetime.now(timezone.utc),
                **page,
            ),
            encoding="utf-8",
        )


def copy_assets():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STYLE_DIR / "site.css", ASSET_DIR / "site.css")


def write_robots():
    (DIST_DIR / "robots.txt").write_text(
        "User-agent: *\nDisallow: /\n",
        encoding="utf-8",
    )


def write_sitemap():
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{page['path']}</loc></url>"
        for page in PAGES
        if page["include_in_sitemap"] and SITE_URL
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    (DIST_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def build_site():
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(("html", "xml")),
        keep_trailing_newline=True,
    )
    copy_assets()
    posts = load_prototype_posts()
    render_pages(environment, posts)
    write_robots()
    write_sitemap()
    print(f"Built {len(PAGES)} public pages in {DIST_DIR}.")


if __name__ == "__main__":
    build_site()
