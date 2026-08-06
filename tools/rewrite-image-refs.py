#!/usr/bin/env python3
"""
Point every remote image reference at the self-hosted copy in assets/.

Companion to tools/fetch-optimize-images.py - run that first, then this.
The YouTube poster (i.ytimg.com) is deliberately left remote: it is the
facade thumbnail for an embedded video and should track the video, not a
snapshot of it.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Match on a stable fragment of each source URL, so query-string variants
# (?w=900 vs ?w=1920) collapse onto the same local file.
REPLACEMENTS = [
    ("i.postimg.cc/ZqbBzDjd", "assets/hero-forest.webp"),
    ("i.postimg.cc/nLXxm4Lb", "assets/jayson-portrait.webp"),
    ("i.postimg.cc/VLkjXvXD", "assets/og-cover.jpg"),
    ("pexels-photo-31733436", "assets/scene-petroglyph.webp"),
    ("pexels-photo-5109343", "assets/scene-premise.webp"),
    ("photo-1740085837769", "assets/scene-bio.webp"),
    ("photo-1570998103225", "assets/scene-totem.webp"),
    ("photo-1737309150415", "assets/scene-why.webp"),
    ("pexels-photo-5107843", "assets/scene-pines.webp"),
    ("photo-1584345735668", "assets/scene-story.webp"),
    ("pexels-photo-7195308", "assets/scene-contact.webp"),
    ("pexels-photo-31499386", "assets/scene-serve.webp"),
]

# Any src="https://host/...<marker>...", up to the closing quote.
URL_RE = re.compile(r'https://(?:i\.postimg\.cc|images\.unsplash\.com|images\.pexels\.com)/[^"\']*')


def rewrite(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text

    def swap(match: re.Match) -> str:
        url = match.group(0)
        for marker, local in REPLACEMENTS:
            if marker in url:
                return local
        return url

    text = URL_RE.sub(swap, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return len(URL_RE.findall(original)) - len(URL_RE.findall(text))
    return 0


def main() -> int:
    targets = sorted(ROOT.glob("*.html")) + sorted((ROOT / "care").glob("*.html"))
    total = 0
    for path in targets:
        n = rewrite(path)
        if n:
            print(f"  {path.relative_to(ROOT)}: {n} remote references localised")
            total += n

    leftover = 0
    for path in targets:
        found = URL_RE.findall(path.read_text(encoding="utf-8"))
        for url in found:
            print(f"  !! still remote in {path.relative_to(ROOT)}: {url[:90]}", file=sys.stderr)
            leftover += 1

    print(f"\n  {total} references rewritten, {leftover} left remote")
    return 1 if leftover else 0


if __name__ == "__main__":
    raise SystemExit(main())
