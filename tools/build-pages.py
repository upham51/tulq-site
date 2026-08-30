#!/usr/bin/env python3
"""
Generate every content page on both TULQ sites, then rewrite both sitemaps.

    python3 tools/build-pages.py

Output is plain static HTML committed to the repo and served directly by
Cloudflare Pages. The generator exists so three dozen pages share one nav,
one footer, and one schema shape - not to introduce a build step. Editing
a generated .html by hand works fine until someone reruns this; put lasting
changes in the tools/content_*.py modules.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_care  # noqa: E402
import content_care_awv  # noqa: E402
import content_care_resources  # noqa: E402
import content_care_services  # noqa: E402
import content_care_tools  # noqa: E402
import content_tribal  # noqa: E402
import content_tribal_areas  # noqa: E402
import content_tribal_resources  # noqa: E402
import landing  # noqa: E402
from pagekit import CARE, ROOT, TRIBAL, Page, write  # noqa: E402

TODAY = date.today().isoformat()

# Hand-authored pages that are not generated but still belong in the sitemaps.
# privacy is deliberately absent - it is noindex on both sites because the two
# copies are near-identical across domains.
#
# The two /nurse-triage-for-* segment pages started life hand-written in PR #88
# and are now generated too, so they no longer appear here.
STATIC = {
    TRIBAL.key: [
        ("/", "1.0", "weekly"),
        ("/story", "0.6", "monthly"),
        ("/contact", "0.7", "monthly"),
    ],
    CARE.key: [
        ("/", "1.0", "weekly"),
        ("/story", "0.6", "monthly"),
        ("/contact", "0.7", "monthly"),
    ],
}


def collect() -> list:
    """Every generated page on both sites.

    Two shapes live in this list. pagekit.Page renders the narrow article
    column on pages.css, which is right for resource posts and segment pages.
    landing.LandingPage renders the homepage's full-bleed cream and basalt
    sections on styles.css, which is what the service, hub, and tool pages
    use. They share enough of an interface (site, slug, priority,
    index_in_sitemap) that the sitemap treats them identically; only the
    writer differs, dispatched in main().
    """
    pages: list = []

    # tulq.health - tribal / IHS track
    pages.append(content_tribal.pillar_tribal_ihs())
    pages.append(content_tribal.pillar_buy_indian_act())
    pages.append(content_tribal.pillar_contracting_officers())
    pages.append(content_tribal_areas.areas_index())
    pages.extend(content_tribal_areas.area_pages())
    pages.append(content_tribal_resources.resources_index())
    pages.extend(content_tribal_resources.posts())
    pages.append(content_tribal_resources.compare_tribal())

    # tulqhealth.com - mainstream track
    # Services hub and the three money pages first: they are the top of the
    # internal-link model and everything below routes up into them.
    pages.extend(content_care_services.pages())
    pages.extend(content_care_awv.pages())
    pages.extend(content_care_tools.pages())
    pages.append(content_care.page_hospice())
    pages.append(content_care.pillar_home_health())
    pages.append(content_care.page_rhc_cah())
    pages.append(content_care.pillar_health_centers())
    pages.append(content_care_resources.resources_index())
    pages.extend(content_care_resources.posts())
    pages.append(content_care_resources.compare_index())
    pages.extend(content_care_resources.compare_pages())

    return pages


def canonical_path(page: Page) -> str:
    """Pretty URL: index pages become a trailing-slash directory."""
    slug = page.slug
    if slug.endswith("/index"):
        return "/" + slug[: -len("index")]
    return "/" + slug


def write_sitemap(site, pages: list[Page]) -> Path:
    entries: list[tuple[str, str, str]] = []
    for path, priority, freq in STATIC[site.key]:
        entries.append((path, priority, freq))
    for page in pages:
        if page.site.key != site.key or not page.index_in_sitemap:
            continue
        entries.append((canonical_path(page), page.priority, "monthly"))

    seen = set()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, freq in entries:
        if path in seen:
            continue
        seen.add(path)
        lines.append("  <url>")
        lines.append(f"    <loc>{site.base}{path}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    out = site.out_dir / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    pages = collect()

    slugs = [(p.site.key, p.slug) for p in pages]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        print(f"  !! duplicate slugs: {dupes}", file=sys.stderr)
        return 1

    by_site: dict[str, int] = {}
    for page in pages:
        out = landing.write(page) if isinstance(page, landing.LandingPage) else write(page)
        by_site[page.site.key] = by_site.get(page.site.key, 0) + 1
        print(f"  {out.relative_to(ROOT)}")

    print()
    for site in (TRIBAL, CARE):
        sm = write_sitemap(site, pages)
        n = sum(1 for p in pages if p.site.key == site.key and p.index_in_sitemap)
        print(f"  {sm.relative_to(ROOT)}  ({n + len(STATIC[site.key])} urls)")

    print(f"\n  {len(pages)} pages generated "
          f"({by_site.get('tribal', 0)} tribal, {by_site.get('care', 0)} mainstream)")

    # care/ is a self-contained mirror; it needs its own copy of pages.css.
    src = ROOT / "pages.css"
    dst = ROOT / "care" / "pages.css"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print("  mirrored pages.css into care/")

    # Stylesheets are served immutable for a year, so every reference has to
    # carry a content hash or CSS edits never reach a returning visitor.
    print()
    import subprocess
    rc = subprocess.call([sys.executable, str(Path(__file__).parent / "stamp-assets.py")])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
