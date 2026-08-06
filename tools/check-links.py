#!/usr/bin/env python3
"""
Verify every site-absolute internal link resolves to a file that exists.

Each site is its own Cloudflare Pages project, so "/" means the repo root
for tulq.health and the care/ directory for tulqhealth.com. A link that is
correct on one site can be a 404 on the other, which is exactly the kind of
mistake this catches.

Cross-domain absolute links (https://tulq.health/... from care/, and vice
versa) are reported separately rather than resolved.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HREF = re.compile(r'href="([^"]+)"')


def resolve(base: Path, href: str) -> Path | None:
    """Map a site-absolute href to the file Cloudflare Pages would serve."""
    path = href.split("#")[0].split("?")[0]
    if not path or path == "/":
        return base / "index.html"
    path = path.strip("/")
    for candidate in (base / f"{path}.html", base / path / "index.html", base / path):
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    sites = [("tulq.health", ROOT, sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("*/*.html"))),
             ("tulqhealth.com", ROOT / "care", sorted((ROOT / "care").glob("**/*.html")))]

    broken: list[str] = []
    cross: set[str] = set()
    checked = 0

    for name, base, files in sites:
        for f in files:
            if base == ROOT and f.is_relative_to(ROOT / "care"):
                continue
            html = f.read_text(encoding="utf-8")
            for href in HREF.findall(html):
                if href.startswith(("mailto:", "tel:", "#")):
                    continue
                if href.startswith("http"):
                    if "tulq.health" in href or "tulqhealth.com" in href:
                        cross.add(f"{f.relative_to(ROOT)} -> {href}")
                    continue
                if not href.startswith("/"):
                    continue  # relative asset paths, checked separately below
                checked += 1
                if resolve(base, href) is None:
                    broken.append(f"  {name}: {f.relative_to(ROOT)} -> {href}")

    # Relative asset references (assets/…, pages.css, styles.css)
    asset_broken: list[str] = []
    for name, base, files in sites:
        for f in files:
            if base == ROOT and f.is_relative_to(ROOT / "care"):
                continue
            for href in re.findall(r'(?:href|src)="((?!http|mailto:|tel:|#|/)[^"]+)"', f.read_text(encoding="utf-8")):
                target = (f.parent / href.split("?")[0]).resolve()
                if not target.exists():
                    asset_broken.append(f"  {name}: {f.relative_to(ROOT)} -> {href}")

    print(f"  {checked} internal links checked")
    if broken:
        print(f"\n  {len(broken)} BROKEN internal links:")
        print("\n".join(sorted(set(broken))))
    if asset_broken:
        print(f"\n  {len(asset_broken)} BROKEN asset references:")
        print("\n".join(sorted(set(asset_broken))))
    if cross:
        print(f"\n  {len(cross)} cross-domain links (not resolved, expected):")
        for c in sorted(cross):
            print(f"    {c}")
    if not broken and not asset_broken:
        print("  all internal links and assets resolve")
    return 1 if (broken or asset_broken) else 0


if __name__ == "__main__":
    raise SystemExit(main())
