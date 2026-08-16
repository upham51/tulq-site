#!/usr/bin/env python3
"""
Stamp every stylesheet reference with a hash of the file's contents.

Why this exists: _headers serves /*.css with

    Cache-Control: public, max-age=31536000, immutable

so a stylesheet URL is cached for a year by browsers and by Cloudflare's
edge. Editing styles.css without changing its URL therefore ships nothing -
returning visitors and the CDN keep serving the old bytes. That is exactly
what happened when the FAQ styles were added under an unchanged
"styles.css?v=9": the markup shipped, the CSS did not, and the accordion
rendered as bare <details> triangles in production.

Hand-maintained ?v=N numbers rely on somebody remembering. A content hash
does not, so this runs over every page and rewrites

    styles.css?v=<anything>   ->  styles.css?v=<hash of styles.css>
    pages.css                 ->  pages.css?v=<hash of pages.css>

_headers caches /*.js on the same immutable year, so scripts are stamped the
same way. rivers.js used to carry a hand-written "?v=2", which is exactly the
pattern that shipped the stale FAQ stylesheet; it is now hashed like the rest.

Run from the repo root (build-pages.py calls it automatically):

    python3 tools/stamp-assets.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = [ROOT, ROOT / "care"]
SHEETS = ("styles.css", "pages.css")
SCRIPTS = ("rivers.js", "landing.js", "awv-worksheet.js", "awv-worksheet.css")
ASSETS = SHEETS + SCRIPTS

# href="<prefix>styles.css" / src="<prefix>landing.js", optionally with ?v=...
_NAMES = "|".join(a.replace(".", r"\.") for a in ASSETS)
REF = re.compile(r'((?:href|src)=")((?:\.\./)*)(' + _NAMES + r')(\?v=[^"]*)?(")')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def main() -> int:
    # Hash per site directory - care/ has its own copies.
    hashes: dict[Path, dict[str, str]] = {}
    for site in SITES:
        hashes[site] = {}
        for sheet in ASSETS:
            f = site / sheet
            if f.exists():
                hashes[site][sheet] = digest(f)

    changed = 0
    scanned = 0
    for site in SITES:
        pages = sorted(site.glob("**/*.html"))
        for page in pages:
            # Root site must not claim care/'s pages.
            if site == ROOT and page.is_relative_to(ROOT / "care"):
                continue
            scanned += 1
            text = page.read_text(encoding="utf-8")

            def swap(m: re.Match) -> str:
                pre, prefix, sheet, _old, post = m.groups()
                h = hashes[site].get(sheet)
                if not h:
                    return m.group(0)
                return f"{pre}{prefix}{sheet}?v={h}{post}"

            new = REF.sub(swap, text)
            if new != text:
                page.write_text(new, encoding="utf-8")
                changed += 1

    for site in SITES:
        label = site.name or "root"
        for sheet, h in hashes[site].items():
            print(f"  {label:>5}/{sheet:<18} v={h}")
    print(f"\n  {changed} of {scanned} pages restamped")

    # Guard: nothing should still carry a hand-numbered version.
    stale = []
    for site in SITES:
        for page in sorted(site.glob("**/*.html")):
            if site == ROOT and page.is_relative_to(ROOT / "care"):
                continue
            for m in REF.finditer(page.read_text(encoding="utf-8")):
                ver = (m.group(4) or "")[3:]
                if ver != hashes[site].get(m.group(3), ver):
                    stale.append(f"{page.relative_to(ROOT)} -> {m.group(3)}?v={ver}")
    if stale:
        print("\n  !! stale references remain:", file=sys.stderr)
        for s in stale:
            print(f"     {s}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
