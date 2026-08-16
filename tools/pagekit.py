#!/usr/bin/env python3
"""
Shared shell for TULQ's generated content pages.

The repo is deliberately plain static HTML with no build step, and that
doesn't change: this emits finished .html files that are committed to git
and served directly. The generator exists so that three dozen pages share
one nav, one footer, and one schema shape instead of drifting apart.

Two sites are generated from the same kit:

  tulq.health     tribal / IHS track   (repo root)
  tulqhealth.com  mainstream track     (care/)

Run tools/build-pages.py to regenerate everything.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ── Site configuration ────────────────────────────────────────────────

@dataclass(frozen=True)
class Site:
    key: str
    domain: str
    out_dir: Path
    mission: str
    nav: tuple[tuple[str, str], ...]
    footer_cols: tuple[tuple[str, tuple[tuple[str, str], ...]], ...]
    legal: tuple[str, ...]

    @property
    def base(self) -> str:
        return f"https://{self.domain}"

    @property
    def org_id(self) -> str:
        return f"{self.base}/#organization"

    @property
    def website_id(self) -> str:
        return f"{self.base}/#website"


TRIBAL = Site(
    key="tribal",
    domain="tulq.health",
    out_dir=ROOT,
    mission=(
        "A 24/7 culturally competent nurse advice line for Indian Health Service "
        "beneficiaries. A confluence of cultural care."
    ),
    # Destinations only. The nav used to carry one entry per homepage
    # section, which put seven items in the bar and told a reader nothing.
    # Everything else routes from the homepage cards and the footer.
    nav=(
        ("IHS Areas", "/areas/"),
        ("Resources", "/resources/"),
        ("Our story", "/story"),
    ),
    footer_cols=(
        ("Who we serve", (
            ("Tribal health &amp; IHS", "/for/tribal-health-ihs"),
            ("IHS Areas", "/areas/"),
            ("Contracting officers", "/for/contracting-officers"),
            ("Buy Indian Act", "/buy-indian-act"),
        )),
        ("Company", (
            ("The line", "/#how"),
            ("Leadership", "/#leadership"),
            ("Our story", "/story"),
            ("Resources", "/resources/"),
            ("Privacy Policy", "/privacy"),
        )),
        ("Reach us", (
            ("hello@tulq.health", "mailto:hello@tulq.health"),
            ("support@tulq.health", "mailto:support@tulq.health"),
            ("Contact the team", "/contact"),
        )),
    ),
    legal=(
        "© 2026 TULQ LLC",
        "Indian Health Service · Nurse Advice Line",
        "Buy Indian Act Qualified · 25 U.S.C. § 47",
    ),
)

CARE = Site(
    key="care",
    domain="tulqhealth.com",
    out_dir=ROOT / "care",
    mission=(
        "Licensed registered nurses who run your after-hours triage line, your "
        "Medicare care management program, and your annual wellness visits."
    ),
    # Three service lines, three money pages, one hub. The Aug 2026 keyword
    # research is explicit that these need separate URLs: the buyers differ,
    # the SERPs differ, and the keyword sets barely overlap. See the module
    # docstring in content_care_services.py.
    #
    # Under the triage service sit four buyer-segment pages, no two competing
    # for the same query. /nurse-triage-for-hospice and
    # /nurse-triage-for-rural-health-clinics began hand-written in PR #88.
    #
    # Destinations only — see the note on TRIBAL.nav. Adding Services meant
    # something had to leave the bar to keep it at three; "Our story" went,
    # since it already sits in the footer's Company column and is the least
    # commercial of the four.
    nav=(
        ("Services", "/services/"),
        ("Compare", "/compare/"),
        ("Resources", "/resources/"),
    ),
    footer_cols=(
        ("Services", (
            ("After-hours nurse triage", "/services/after-hours-nurse-triage"),
            ("Care management", "/services/care-management"),
            ("Annual wellness visits", "/services/medicare-annual-wellness-visits"),
            ("AWV revenue calculator", "/tools/awv-revenue-calculator"),
            ("AWV worksheet", "/tools/annual-wellness-visit-worksheet"),
        )),
        ("Who we serve", (
            ("Hospice", "/nurse-triage-for-hospice"),
            ("Home health", "/for/home-health"),
            ("FQHC &amp; health centers", "/for/health-centers"),
            ("Rural health clinics", "/nurse-triage-for-rural-health-clinics"),
            ("Compare providers", "/compare/"),
        )),
        ("Company", (
            ("All services", "/services/"),
            ("Leadership", "/#leadership"),
            ("Our story", "/story"),
            ("Resources", "/resources/"),
            ("Privacy Policy", "/privacy"),
        )),
        ("Reach us", (
            ("hello@tulq.health", "mailto:hello@tulq.health"),
            ("support@tulq.health", "mailto:support@tulq.health"),
            ("Contact the team", "/contact"),
        )),
    ),
    legal=(
        "© 2026 TULQ LLC",
        "Nurse Triage · Care Management · Wellness Visits",
        "Licensed RNs · Schmitt-Thompson Protocols",
    ),
)


# ── Page model ────────────────────────────────────────────────────────

@dataclass
class Page:
    site: Site
    slug: str                 # "for/tribal-health-ihs" -> /for/tribal-health-ihs
    title: str                # <title>, keyword-led, <= ~60 chars
    description: str          # meta description with a CTA
    eyebrow: str
    h1: str                   # may contain <em>
    deck: str
    body: str = ""            # main HTML between deck and CTA
    crumbs: list[tuple[str, str]] = field(default_factory=list)
    schema: list[dict] = field(default_factory=list)
    page_type: str = "WebPage"
    reviewed: bool = False    # stamp the RN clinical review byline
    published: str = "2026-08-06"
    cta_title: str = ""
    cta_body: str = ""
    wide: bool = False
    index_in_sitemap: bool = True
    priority: str = "0.7"

    @property
    def url(self) -> str:
        """Canonical URL. Index pages canonicalize to the directory, not /index."""
        slug = self.slug
        if slug.endswith("/index"):
            slug = slug[: -len("index")]
        elif slug == "index":
            slug = ""
        return f"{self.site.base}/{slug}"

    @property
    def out_path(self) -> Path:
        return self.site.out_dir / f"{self.slug}.html"

    @property
    def depth(self) -> int:
        return self.slug.count("/")

    @property
    def asset_prefix(self) -> str:
        """Relative hop back to the site root, so care/ stays self-contained."""
        return "../" * self.depth


# ── Fragments ─────────────────────────────────────────────────────────

def _is_current(page: Page, href: str) -> bool:
    """Highlight the nav entry whose section this page lives in."""
    target = href.strip("/")
    slug = page.slug.rstrip("/")
    if slug == target:
        return True
    # Section indexes (/areas/, /resources/) own their children.
    return href.endswith("/") and slug.startswith(target + "/")


def _nav(page: Page) -> str:
    site = page.site
    p = page.asset_prefix
    rows = []
    for label, href in site.nav:
        current = ' aria-current="page"' if _is_current(page, href) else ""
        rows.append(f'      <a href="{href}"{current}>{label}</a>')
    links = "\n".join(rows)
    return f"""<div class="nav-wrap">
  <nav class="nav" aria-label="Primary">
    <a href="/" class="brand" aria-label="TULQ home">
      <img class="brand-logo" src="{p}assets/logo.webp" alt="" width="32" height="32" fetchpriority="high" decoding="async" />
      <span>TULQ</span>
    </a>
    <div class="nav-links">
{links}
    </div>
    <a class="nav-cta" href="/contact">
      <span class="dot" aria-hidden="true"></span>
      Contact us
    </a>
  </nav>
</div>"""


def _crumbs(page: Page) -> str:
    if not page.crumbs:
        return ""
    parts = ['<nav class="crumbs" aria-label="Breadcrumb">', '  <a href="/">Home</a>']
    for i, (label, href) in enumerate(page.crumbs):
        parts.append('  <span class="sep" aria-hidden="true">/</span>')
        if i == len(page.crumbs) - 1:
            parts.append(f'  <span aria-current="page">{label}</span>')
        else:
            parts.append(f'  <a href="{href}">{label}</a>')
    parts.append("</nav>")
    return "\n".join(parts)


def _byline(page: Page) -> str:
    if not page.reviewed:
        return ""
    return f"""<div class="byline">
  <span class="byline-tag">Clinically reviewed</span>
  <span>Reviewed by <strong>Jayson Forrest Minagawa, RN, BSN</strong>, Clinical Director</span>
  <span>Updated {page.published}</span>
</div>"""


def _cta(page: Page) -> str:
    title = page.cta_title or "Talk to the people who built the line."
    body = page.cta_body or (
        "TULQ is launching in 2026. If you are scoping coverage, responding to a "
        "solicitation, or just want to know what this would look like for your "
        "organization, we would like to hear from you."
    )
    return f"""<section class="cta">
  <h2>{title}</h2>
  <p>{body}</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="/contact">Contact the team</a>
    <a class="btn btn-ghost" href="/#how">See how the line works</a>
  </div>
</section>"""


def _footer(page: Page) -> str:
    site = page.site
    p = page.asset_prefix
    cols = []
    for head, links in site.footer_cols:
        items = "\n".join(f'          <a href="{href}">{label}</a>' for label, href in links)
        cols.append(f"""        <div class="site-foot-col">
          <div class="site-foot-col-head">{head}</div>
{items}
        </div>""")
    legal = "\n".join(f"        <span>{item}</span>" for item in site.legal)
    return f"""<footer class="site-foot">
  <div class="site-foot-inner">
    <div class="site-foot-top">
      <div class="site-foot-brand">
        <img class="site-foot-logo" src="{p}assets/logo.webp" alt="TULQ" width="54" height="54" loading="lazy" decoding="async" />
        <p class="site-foot-name">TULQ</p>
        <p class="site-foot-tag">tultx&#695; · where the waters meet</p>
        <p class="site-foot-mission">{site.mission}</p>
      </div>
      <nav class="site-foot-nav" aria-label="Footer">
{chr(10).join(cols)}
      </nav>
    </div>
    <div class="site-foot-bottom">
      <div class="site-foot-legal">
{legal}
      </div>
      <span class="site-foot-mark">tultx&#695;</span>
    </div>
  </div>
</footer>"""


# ── Schema ────────────────────────────────────────────────────────────

def _breadcrumb_node(page: Page) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{page.site.base}/"}]
    for i, (label, href) in enumerate(page.crumbs, start=2):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": _strip_tags(label),
            "item": f"{page.site.base}{href}" if href.startswith("/") else href,
        })
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page.url}#breadcrumb",
        "itemListElement": items,
    }


def _webpage_node(page: Page) -> dict:
    # Article pages get a proper Article node of their own (see article_node),
    # linked back here via mainEntityOfPage. The page node stays a WebPage so
    # we don't emit two competing Article entities for the same URL.
    node_type = "WebPage" if page.page_type in ("Article", "BlogPosting") else page.page_type
    node = {
        "@type": node_type,
        "@id": f"{page.url}#webpage",
        "url": page.url,
        "name": _strip_tags(page.title),
        "description": _strip_tags(page.description),
        "inLanguage": "en-US",
        "isPartOf": {"@id": page.site.website_id},
        "about": {"@id": page.site.org_id},
        "publisher": {"@id": page.site.org_id},
        "primaryImageOfPage": f"{page.site.base}/assets/og-cover.jpg",
    }
    if page.crumbs:
        node["breadcrumb"] = {"@id": f"{page.url}#breadcrumb"}
    if page.reviewed:
        node["reviewedBy"] = {
            "@type": "Person",
            "name": "Jayson Forrest Minagawa",
            "honorificSuffix": "RN, BSN",
            "jobTitle": "Clinical Director",
            "worksFor": {"@id": page.site.org_id},
        }
        node["dateModified"] = page.published
    return node


def build_schema(page: Page) -> str:
    graph = [_webpage_node(page)]
    if page.crumbs:
        graph.append(_breadcrumb_node(page))
    graph.extend(page.schema)
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, indent=2, ensure_ascii=False)


def faq_node(page: Page, qa: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{page.url}#faq",
        "url": f"{page.url}#faq",
        "inLanguage": "en-US",
        "isPartOf": {"@id": page.site.website_id},
        "mainEntity": [
            {
                "@type": "Question",
                "name": _strip_tags(q),
                "acceptedAnswer": {"@type": "Answer", "text": _strip_tags(a)},
            }
            for q, a in qa
        ],
    }


def article_node(page: Page) -> dict:
    node = {
        "@type": "Article",
        "@id": f"{page.url}#article",
        "headline": _strip_tags(page.title),
        "description": _strip_tags(page.description),
        "inLanguage": "en-US",
        "isPartOf": {"@id": page.site.website_id},
        "mainEntityOfPage": {"@id": f"{page.url}#webpage"},
        "publisher": {"@id": page.site.org_id},
        "author": {"@id": page.site.org_id},
        "image": f"{page.site.base}/assets/og-cover.jpg",
        "datePublished": page.published,
        "dateModified": page.published,
    }
    if page.reviewed:
        node["reviewedBy"] = {
            "@type": "Person",
            "name": "Jayson Forrest Minagawa",
            "honorificSuffix": "RN, BSN",
            "jobTitle": "Clinical Director",
            "worksFor": {"@id": page.site.org_id},
        }
    return node


def service_node(page: Page, name: str, service_type: str, description: str,
                 audience: str = "") -> dict:
    node = {
        "@type": "Service",
        "@id": f"{page.url}#service",
        "name": name,
        "serviceType": service_type,
        "description": description,
        "provider": {"@id": page.site.org_id},
        "areaServed": {"@type": "Country", "name": "United States"},
    }
    if audience:
        node["audience"] = {"@type": "Audience", "audienceType": audience}
    return node


# ── HTML helpers used by the content modules ──────────────────────────

def faq_block(qa: list[tuple[str, str]], heading: str = "Questions people ask") -> str:
    items = []
    for q, a in qa:
        items.append(f"""      <details class="faq-item">
        <summary>
          <span class="faq-q">{q}</span>
          <span class="faq-sign" aria-hidden="true"></span>
        </summary>
        <div class="faq-answer">
{a}
        </div>
      </details>""")
    return f"""<h2 id="faq">{heading}</h2>
    <div class="faq-list">
{chr(10).join(items)}
    </div>"""


def card_grid(cards: list[tuple[str, str, str, str]]) -> str:
    """cards: (tag, title, blurb, href)"""
    out = []
    for tag, title, blurb, href in cards:
        tag_html = f'<div class="card-tag">{tag}</div>' if tag else ""
        out.append(f"""      <a class="card" href="{href}">
        {tag_html}
        <h3>{title}</h3>
        <p>{blurb}</p>
        <span class="card-more">Read &rarr;</span>
      </a>""")
    return f'<div class="card-grid">\n{chr(10).join(out)}\n    </div>'


def sources_block(items, disclaimer: str = "") -> str:
    """Render the Sources list.

    An item is either a bare string, or a (label, url) pair. Pairs become
    real outbound links to the document being cited, which is the whole
    point of listing a source: a reader who wants to check the claim
    should be one click from the primary text, not left to search for it.
    Only cite a URL that has actually been checked to resolve.
    """
    rows = []
    for item in items:
        if isinstance(item, (tuple, list)):
            label, url = item
            rows.append(
                f'    <li><a class="source-link" href="{url}" '
                f'target="_blank" rel="noopener">{label}</a></li>'
            )
        else:
            rows.append(f"    <li>{item}</li>")
    lis = "\n".join(rows)
    extra = f'\n  <p class="disclaimer">{disclaimer}</p>' if disclaimer else ""
    return f"""<section class="sources">
  <h2>Sources</h2>
  <ul>
{lis}
  </ul>{extra}
</section>"""


def _strip_tags(text: str) -> str:
    import re
    clean = re.sub(r"<[^>]+>", "", text)
    return (clean.replace("&amp;", "&").replace("&nbsp;", " ")
                 .replace("&rarr;", "->").replace("&#695;", "ʷ")
                 .replace("&mdash;", "—").replace("&sect;", "§").strip())


# ── Render ────────────────────────────────────────────────────────────

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="{url}" />

<meta property="og:site_name" content="TULQ" />
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="{og_type}" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{base}/assets/og-cover.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta property="twitter:domain" content="{domain}" />
<meta property="twitter:url" content="{url}" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{base}/assets/og-cover.jpg" />

<meta name="theme-color" content="#1c2628" />
<link rel="icon" type="image/webp" href="{p}assets/logo.webp" />
<link rel="apple-touch-icon" href="{p}assets/logo.webp" />

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<link rel="stylesheet" href="{p}pages.css" />

<script type="application/ld+json">
{schema}
</script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main class="{wrap_class}" id="main">
{crumbs}
  <span class="eyebrow">{eyebrow}</span>
  <h1 class="display">{h1}</h1>
  <p class="deck">{deck}</p>
{byline}
  <div class="prose">
{body}
  </div>

{cta}
</main>

{footer}

</body>
</html>
"""


def render(page: Page) -> str:
    og_type = "article" if page.page_type in ("Article", "BlogPosting") else "website"
    html = TEMPLATE.format(
        title=page.title,
        description=escape(_strip_tags(page.description), quote=True),
        url=page.url,
        base=page.site.base,
        domain=page.site.domain,
        og_type=og_type,
        p=page.asset_prefix,
        schema=build_schema(page),
        nav=_nav(page),
        crumbs=_crumbs(page),
        eyebrow=page.eyebrow,
        h1=page.h1,
        deck=page.deck,
        byline=_byline(page),
        body=page.body,
        cta=_cta(page),
        footer=_footer(page),
        wrap_class="wide-wrap" if page.wide else "article-wrap",
    )
    return html


def write(page: Page) -> Path:
    out = page.out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(page), encoding="utf-8")
    return out
