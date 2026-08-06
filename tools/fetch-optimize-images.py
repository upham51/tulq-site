#!/usr/bin/env python3
"""
Pull the site's remote imagery down into assets/ and re-encode it.

Both sites previously loaded ~15 images from four third-party CDNs
(postimg, unsplash, pexels, ytimg). That is four extra DNS + TLS handshakes
before a single decorative photo can start painting, which is the wrong
trade for the rural / low-bandwidth audience this site is built for.

Run from the repo root:

    python3 tools/fetch-optimize-images.py

Downloads each source once, re-encodes to WebP (JPEG for the social card,
because some scrapers still refuse WebP), writes into assets/, and mirrors
everything into care/assets/. Rewriting the HTML references is a separate
step - see tools/rewrite-image-refs.py.
"""

import io
import shutil
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CARE_ASSETS = ROOT / "care" / "assets"

# name -> (source url, max width, format, quality)
IMAGES = {
    # Social card. JPEG on purpose: a few social scrapers still refuse WebP.
    "og-cover": (
        "https://i.postimg.cc/VLkjXvXD/Gemini-Generated-Image-vi4poovi4poovi4p-(1).png",
        1200, "JPEG", 82,
    ),
    # Hero atmosphere, right side, decorative.
    "hero-forest": (
        "https://i.postimg.cc/ZqbBzDjd/Gemini-Generated-Image-al7rqyal7rqyal7r-(1).png",
        1400, "WEBP", 74,
    ),
    # Clinical director portrait - a real content image, displayed small.
    "jayson-portrait": (
        "https://i.postimg.cc/nLXxm4Lb/Screenshot-2026-05-15-at-6-16-15-PM.png",
        700, "WEBP", 80,
    ),
    # Decorative full-bleed scene photos behind each section.
    "scene-petroglyph": (
        "https://images.pexels.com/photos/31733436/pexels-photo-31733436.jpeg?auto=compress&cs=tinysrgb&w=1920",
        1600, "WEBP", 70,
    ),
    "scene-premise": (
        "https://images.pexels.com/photos/5109343/pexels-photo-5109343.jpeg?auto=compress&cs=tinysrgb&w=1800",
        1600, "WEBP", 70,
    ),
    "scene-bio": (
        "https://images.unsplash.com/photo-1740085837769-67c4a8c37896?fm=jpg&q=60&w=1800&auto=format&fit=crop",
        1600, "WEBP", 70,
    ),
    "scene-totem": (
        "https://images.unsplash.com/photo-1570998103225-83a725716e28?fm=jpg&q=60&w=1400&auto=format&fit=crop",
        1400, "WEBP", 70,
    ),
    "scene-why": (
        "https://images.unsplash.com/photo-1737309150415-eaa7564b9e07?fm=jpg&q=60&w=1800&auto=format&fit=crop",
        1600, "WEBP", 70,
    ),
    "scene-pines": (
        "https://images.pexels.com/photos/5107843/pexels-photo-5107843.jpeg?auto=compress&cs=tinysrgb&w=1920",
        1600, "WEBP", 70,
    ),
    "scene-story": (
        "https://images.unsplash.com/photo-1584345735668-5bce6952b2d6?fm=jpg&q=60&w=2400&auto=format&fit=crop",
        1600, "WEBP", 70,
    ),
    "scene-contact": (
        "https://images.pexels.com/photos/7195308/pexels-photo-7195308.jpeg?auto=compress&cs=tinysrgb&w=1400",
        1400, "WEBP", 70,
    ),
    "scene-serve": (
        "https://images.pexels.com/photos/31499386/pexels-photo-31499386.jpeg?auto=compress&cs=tinysrgb&w=1400",
        1400, "WEBP", 70,
    ),
}

UA = {"User-Agent": "Mozilla/5.0 (compatible; tulq-site-build/1.0)"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def process(name: str, url: str, max_w: int, fmt: str, quality: int) -> Path:
    raw = fetch(url)
    im = Image.open(io.BytesIO(raw))

    if fmt == "JPEG":
        # Social cards want 1.91:1. Center-crop rather than letterbox.
        target = (1200, 630)
        src_ratio = im.width / im.height
        dst_ratio = target[0] / target[1]
        if src_ratio > dst_ratio:
            new_w = int(im.height * dst_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            new_h = int(im.width / dst_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
        im = im.convert("RGB").resize(target, Image.LANCZOS)
        out = ASSETS / f"{name}.jpg"
        im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    else:
        if im.width > max_w:
            h = round(im.height * max_w / im.width)
            im = im.resize((max_w, h), Image.LANCZOS)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA")
        out = ASSETS / f"{name}.webp"
        im.save(out, "WEBP", quality=quality, method=6)

    return out


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    CARE_ASSETS.mkdir(parents=True, exist_ok=True)

    total = 0
    for name, (url, max_w, fmt, quality) in IMAGES.items():
        try:
            out = process(name, url, max_w, fmt, quality)
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"  !! {name}: {exc}", file=sys.stderr)
            continue
        size = out.stat().st_size
        total += size
        with Image.open(out) as check:
            dims = f"{check.width}x{check.height}"
        print(f"  {out.name:<26} {dims:>11}  {size / 1024:7.1f} KB")

    # Shrink the orphaned headshot that shipped at 835 KB.
    legacy = ASSETS / "jayson.jpg"
    if legacy.exists() and legacy.stat().st_size > 200_000:
        with Image.open(legacy) as im:
            im = im.convert("RGB")
            if im.width > 700:
                im = im.resize((700, round(im.height * 700 / im.width)), Image.LANCZOS)
            im.save(legacy, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"  {legacy.name:<26} {'recompressed':>11}  {legacy.stat().st_size / 1024:7.1f} KB")

    # care/ is a self-contained mirror - keep its assets in step.
    for src in ASSETS.iterdir():
        if src.is_file():
            shutil.copy2(src, CARE_ASSETS / src.name)

    print(f"\n  total new imagery: {total / 1024:.1f} KB across {len(IMAGES)} files")
    print(f"  mirrored into {CARE_ASSETS.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
