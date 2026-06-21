import os
import re
import yaml
import markdown
from PIL import Image
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURATION & PATHS ---
SRC_DIR = "src"
CONTENT_DIR = os.path.join(SRC_DIR, "content", "places")
IMAGES_DIR = os.path.join(SRC_DIR, "images")
TEMPLATE_DIR = os.path.join(SRC_DIR, "templates")
DIST_DIR = "dist"
ASSETS_DIR = os.path.join(DIST_DIR, "assets")

SITE_URL = "https://travel-blog-c8n.pages.dev"  # Default Cloudflare Pages Subdomain

# Defensive string remapping / Fallback Logic
FALLBACK_MAPS = {
    "terrain": {
        "muddy_woodland": "Muddy Woodland Tracks",
        "coastal_paths": "Coastal Paths & Sand",
        "paved_paths": "Paved Paths & Parks",
        "open_fields": "Open Grassy Fields"
    },
    "parking": {
        "free_onsite": "Free On-Site",
        "paid_parking": "Paid Parking",
        "layby_only": "Layby Only",
        "no_parking": "No Dedicated Parking"
    },
    "dogs": {
        "highly_friendly": "Highly Dog Friendly",
        "lead_only": "Dogs on Lead Only",
        "no_dogs": "No Dogs Allowed"
    },
    "category": {
        "outings": "Outings & Walks",
        "historic": "Historic Sites",
        "day_trips": "Day Trips"
    },
    "tags": {
        "woodland": "Woodland",
        "water": "Water / River",
        "local_essex": "Local Essex",
        "hilly": "Hilly Terrain"
    }
}

def resolve_value(field, key):
    """Safely returns the human-readable string for any given database key."""
    if field in FALLBACK_MAPS and key in FALLBACK_MAPS[field]:
        return FALLBACK_MAPS[field][key]
    return str(key).replace("_", " ").title()

def process_image(img_filename):
    """Processes raw JPEGs into stripped, optimized WebP files and returns dimensions to prevent CLS."""
    src_path = os.path.join(IMAGES_DIR, img_filename)
    dest_filename = os.path.splitext(img_filename)[0] + ".webp"
    dest_path = os.path.join(ASSETS_DIR, dest_filename)
    
    if not os.path.exists(src_path):
        print(f"Warning: Source image {img_filename} not found.")
        return f"/assets/{dest_filename}", 800, 600  # Safe safety defaults
        
    try:
        with Image.open(src_path) as img:
            width, height = img.size
            # Overwrite metadata by rebuilding file data completely (Strips EXIF strings)
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(img.getdata())
            
            # Save format optimization at strict 82% quality constraint
            clean_img.save(dest_path, "WEBP", quality=82)
            print(f"Optimized Image: {dest_filename} ({width}x{height}) EXIF completely stripped.")
            return f"/assets/{dest_filename}", width, height
    except Exception as e:
        print(f"Error processing image {img_filename}: {e}")
        return f"/assets/{dest_filename}", 800, 600

def build_site():
    print("Starting site compilation pipeline...")
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Initialize Template Environments
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # Database flat-file parsing array
    posts = []
    
    if os.path.exists(CONTENT_DIR):
        for file in os.listdir(CONTENT_DIR):
            if file.endswith(".md"):
                file_path = os.path.join(CONTENT_DIR, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content_text = f.read()
                    
                # Split YAML from markdown body parsing blocks
                match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content_text, re.DOTALL)
                if match:
                    frontmatter_raw = match.group(1)
                    body_markdown = match.group(2)
                    
                    meta = yaml.safe_load(frontmatter_raw) or {}
                    html_content = markdown.markdown(body_markdown)
                    
                    # Resolve safe metadata fallback structures
                    meta["resolved_terrain"] = resolve_value("terrain", meta.get("terrain"))
                    meta["resolved_parking"] = resolve_value("parking", meta.get("parking"))
                    meta["resolved_dogs"] = resolve_value("dogs", meta.get("dogs"))
                    meta["resolved_category"] = resolve_value("category", meta.get("category"))
                    meta["resolved_tags"] = [resolve_value("tags", t) for t in meta.get("tags", [])]
                    meta["slug"] = os.path.splitext(file)[0]
                    meta["body"] = html_content
                    
                    # Convert raw thumbnail format properties cleanly
                    if "thumbnail" in meta and meta["thumbnail"]:
                        img_file = os.path.basename(meta["thumbnail"])
                        webp_url, w, h = process_image(img_file)
                        meta["webp_thumbnail"] = webp_url
                        meta["img_width"] = w
                        meta["img_height"] = h
                    
                    posts.append(meta)

    # Sort items sequentially by explicit publication date
    posts.sort(key=lambda x: str(x.get("date", "")), reverse=True)

    # Render Content Templates cleanly (Tackled completely during Phase 3 Frontend rendering loop)
    # Placeholder loop verification logging block
    print(f"Discovered and mapped {len(posts)} total travel place posts.")
    
    # --- STATIC SEO COMPILATION ENGINES ---
    # 1. robots.txt
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml")
    print("SEO Engine: robots.txt written seamlessly.")
        
    # 2. sitemap.xml
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_xml += f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <priority>1.0</priority>\n  </url>\n'
    sitemap_xml += f'  <url>\n    <loc>{SITE_URL}/about</loc>\n    <priority>0.5</priority>\n  </url>\n'
    sitemap_xml += f'  <url>\n    <loc>{SITE_URL}/places</loc>\n    <priority>0.8</priority>\n  </url>\n'
    
    for p in posts:
        sitemap_xml += f'  <url>\n    <loc>{SITE_URL}/places/{p["slug"]}</loc>\n    <priority>0.7</priority>\n  </url>\n'
        
    sitemap_xml += "</urlset>"
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("SEO Engine: sitemap.xml dynamically parsed and compiled successfully.")

if __name__ == "__main__":
    build_site()
