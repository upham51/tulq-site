#!/usr/bin/env python3
"""
Homepage-styled landing pages.

pagekit.py renders *article* pages: a narrow column on pages.css, good for
resource posts and segment pages. This module renders the other shape, the
one the homepage uses: full-bleed sections alternating cream and basalt,
each with a Pexels scene photograph behind it, on styles.css.

Both modules read the same `Site` config out of pagekit, so nav, footer,
mission, and legal lines stay in one place. The markup here is copied from
care/index.html deliberately: every class below already exists in
styles.css, so a landing page inherits the homepage's type, colour, seams,
and reveal animations rather than growing a parallel design system.

The section vocabulary, in the order a page normally uses it:

    hero()            basalt, full-bleed, scene photo, H1 + sub + facts
    band()            generic cream|dark section, wraps any inner HTML
    serve_cards()     numbered card grid          (.serve-grid)
    pillars()         three-up pillar grid        (.pillars)
    steps()           numbered process flow       (.steps)
    numbers()         count-up statistics         (.numbers)
    routes()          cross-link grid             (.serve-routes)
    split()           two-column prose comparison (.lp-split)
    compare_table()   responsive comparison table (.lp-table)
    ledger()          requirement list with owner badges (.lp-ledger)
    note()            inset caution/aside         (.lp-note)
    faq()             accordion with cited sources (.faq-list)
    contact_close()   the closing band, with both seams

Anything prefixed .lp- is new and lives in the LANDING PAGES block at the
bottom of care/styles.css. Everything else is the homepage's own.

House style is enforced here as much as it can be: see check_copy().
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html import escape

from pagekit import Site, _strip_tags

# Scene photographs, reused from the homepage. Each tuple is
# (file, scene-photo modifier class) so a page picks a look, not a path.
SCENES = {
    "pines": ("scene-pines.webp", "scene-photo--pines"),
    "totem": ("scene-serve.webp", "scene-photo--totem"),
    "bio": ("scene-bio.webp", "scene-photo--bio"),
    "why": ("scene-why.webp", "scene-photo--why"),
    "cave": ("scene-cave-wall.webp", "scene-photo--cave"),
    "contact": ("scene-contact.webp", "scene-photo--contact"),
    "story": ("scene-story.webp", "scene-photo--story"),
    "petroglyph": ("scene-petroglyph.webp", "scene-photo--petroglyph"),
    "premise": ("scene-premise.webp", "scene-photo--petroglyph"),
}

ARROW_SVG = (
    '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
    '<path d="M3 7h8m0 0L7.5 3.5M11 7l-3.5 3.5" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


# ── Page model ────────────────────────────────────────────────────────

@dataclass
class LandingPage:
    site: Site
    slug: str
    title: str
    description: str
    h1: str                       # may contain <em>
    hero_sub: str
    hero_facts: tuple[str, ...] = ()
    hero_eyebrow: str = ""
    hero_scene: str = "pines"
    hero_ctas: str = ""           # HTML; defaults to Contact + a scroll link
    sections: list[str] = field(default_factory=list)
    schema: list[dict] = field(default_factory=list)
    reviewed: bool = False
    published: str = "2026-08-16"
    priority: str = "0.9"
    index_in_sitemap: bool = True
    extra_head: str = ""          # raw head HTML, e.g. a <link> to a tool stylesheet
    extra_css: str = ""           # CSS, wrapped in <style>, for one-off page needs
    extra_js: str = ""            # inline JS, or raw <script src> markup if it starts with "<"

    @property
    def url(self) -> str:
        slug = self.slug
        if slug.endswith("/index"):
            slug = slug[: -len("index")]
        return f"{self.site.base}/{slug}"

    @property
    def out_path(self):
        return self.site.out_dir / f"{self.slug}.html"

    @property
    def depth(self) -> int:
        return self.slug.count("/")

    @property
    def asset_prefix(self) -> str:
        return "../" * self.depth


# ── Small helpers ─────────────────────────────────────────────────────

def _scene(name: str, eager: bool = False) -> str:
    if not name:
        return ""
    fname, cls = SCENES[name]
    loading = "eager" if eager else "lazy"
    return (
        f'  <div class="scene-photo {cls}" aria-hidden="true">\n'
        f'    <img src="{{p}}assets/{fname}" alt="" loading="{loading}" decoding="async">\n'
        f"  </div>"
    )


def _head(eyebrow: str, h2: str, deck: str, dark: bool, centred: bool = False) -> str:
    tone = "eyebrow-dark" if dark else "eyebrow-light"
    style = ' style="text-align:center;margin-left:auto;margin-right:auto;"' if centred else ""
    deck_html = f"\n      <p>{deck}</p>" if deck else ""
    eye = ""
    if eyebrow:
        eye = (
            f'\n      <span class="eyebrow {tone}">'
            f'<span class="dot" aria-hidden="true"></span>{eyebrow}</span>'
        )
    return f"""    <div class="section-head rise"{style}>{eye}
      <h2>{h2}</h2>{deck_html}
    </div>"""


# ── Section builders ──────────────────────────────────────────────────

def band(inner: str, *, dark: bool = False, scene: str = "", anchor: str = "",
         label: str = "", eyebrow: str = "", h2: str = "", deck: str = "",
         centred_head: bool = False, extra_class: str = "") -> str:
    """A full-bleed section in the homepage's cream/basalt rhythm."""
    tone = "section-dark" if dark else "section-cream"
    ident = f' id="{anchor}"' if anchor else ""
    lab = f' data-screen-label="{label}"' if label else ""
    cls = f"section {tone}" + (f" {extra_class}" if extra_class else "")
    head = _head(eyebrow, h2, deck, dark, centred_head) if h2 else ""
    parts = [f'<section class="{cls}"{ident}{lab}>']
    if scene:
        parts.append(_scene(scene))
    parts.append('  <div class="container">')
    if head:
        parts.append(head)
    parts.append(inner)
    parts.append("  </div>")
    parts.append("</section>")
    return "\n".join(parts)


def hero(page: LandingPage) -> str:
    fname, _ = SCENES[page.hero_scene]
    facts = ""
    if page.hero_facts:
        spans = "".join(f"<span>{f}</span>" for f in page.hero_facts)
        facts = f'\n      <p class="hero-facts">{spans}</p>'
    eyebrow = ""
    if page.hero_eyebrow:
        eyebrow = (
            f'\n      <span class="eyebrow eyebrow-dark hero-eyebrow">'
            f'<span class="dot" aria-hidden="true"></span>{page.hero_eyebrow}</span>'
        )
    ctas = page.hero_ctas or (
        '<a class="btn btn-primary" href="/contact" data-magnetic>'
        f"Talk to us{ARROW_SVG}</a>"
        '<a class="btn btn-ghost" href="#how">How it works</a>'
    )
    return f"""<header class="hero hero--page" id="top" data-screen-label="01 Hero">
  <div class="hero-photos" aria-hidden="true">
    <img class="hero-photo hero-photo--forest" src="{{p}}assets/{fname}" alt="" loading="eager" decoding="async">
  </div>
  <div class="hero-glow" id="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <div class="hero-copy rise">{eyebrow}
      <h1>{page.h1}</h1>
      <h2 class="hero-sub">{page.hero_sub}</h2>{facts}
      <div class="hero-ctas">{ctas}</div>
    </div>
  </div>
  <div class="hero-scroll" aria-hidden="true">
    <span>Keep going</span>
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
      <path d="M6 2v8m0 0L2.5 6.5M6 10l3.5-3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</header>"""


def crumbs(trail: list[tuple[str, str]]) -> str:
    """Breadcrumb strip. Sits on the cream band directly under the hero."""
    items = ['  <a href="/">Home</a>']
    for i, (label, href) in enumerate(trail):
        items.append('  <span class="sep" aria-hidden="true">/</span>')
        if i == len(trail) - 1:
            items.append(f'  <span aria-current="page">{label}</span>')
        else:
            items.append(f'  <a href="{href}">{label}</a>')
    return (
        '<nav class="lp-crumbs" aria-label="Breadcrumb">\n  <div class="container">\n'
        + "\n".join("  " + i for i in items)
        + "\n  </div>\n</nav>"
    )


def serve_cards(cards: list[dict]) -> str:
    """cards: {title, body, tag, href?, link_label?}

    The grid draws its rules as 1px gaps showing the container background,
    so a column count that exceeds the card count renders as a blank panel
    rather than as whitespace. The count modifier keeps them in step.
    """
    out = []
    for i, c in enumerate(cards, start=1):
        link = ""
        if c.get("href"):
            label = c.get("link_label", "Learn more")
            link = f'\n        <a class="serve-card-link" href="{c["href"]}">{label} &rarr;</a>'
        out.append(f"""      <div class="serve-card rise">
        <div class="serve-num">{i:02d}</div>
        <h4>{c["title"]}</h4>
        <p>{c["body"]}</p>
        <div class="serve-card-tag">{c["tag"]}</div>{link}
      </div>""")
    mod = f" serve-grid--{len(cards)}" if len(cards) in (2, 3) else ""
    return f'    <div class="serve-grid{mod}">\n' + "\n".join(out) + "\n    </div>"


def pillars(items: list[dict]) -> str:
    """items: {title, body, source}"""
    out = []
    for i, p in enumerate(items, start=1):
        out.append(f"""      <article class="pillar rise">
        <div class="pillar-num">Pillar {i:02d}</div>
        <h3>{p["title"]}</h3>
        <p>{p["body"]}</p>
        <div class="pillar-source">{p["source"]}</div>
      </article>""")
    return '    <div class="pillars">\n' + "\n".join(out) + "\n    </div>"


def steps(items: list[dict]) -> str:
    """items: {title, body}"""
    out = []
    for i, s in enumerate(items, start=1):
        out.append(f"""      <div class="step rise">
        <div class="step-num">{i:02d}</div>
        <h3>{s["title"]}</h3>
        <p>{s["body"]}</p>
      </div>""")
    return '    <div class="steps">\n' + "\n".join(out) + "\n    </div>"


def numbers(items: list[dict], source: str = "", anchor: str = "numbers") -> str:
    """items: {tag, value, label, count?, suffix?, prefix?, sup?}"""
    out = []
    for n in items:
        attrs = ""
        for key in ("count", "suffix", "prefix", "sup"):
            if n.get(key):
                attrs += f' data-{key}="{n[key]}"'
        out.append(f"""      <div class="number">
        <div class="number-tag">{n["tag"]}</div>
        <div class="number-value"{attrs}>{n["value"]}</div>
        <div class="number-label">{n["label"]}</div>
      </div>""")
    src = f'\n    <div class="numbers-source">{source}</div>' if source else ""
    return (
        f'    <div class="numbers rise" id="{anchor}">\n'
        + "\n".join(out)
        + f"\n    </div>{src}"
    )


def routes(heading: str, deck: str, items: list[dict]) -> str:
    """items: {tag, title, desc, href}"""
    out = []
    for r in items:
        out.append(f"""        <a class="serve-route" href="{r["href"]}">
          <span class="serve-route-tag">{r["tag"]}</span>
          <span class="serve-route-title">{r["title"]}</span>
          <span class="serve-route-desc">{r["desc"]}</span>
        </a>""")
    return f"""    <div class="serve-routes rise">
      <div class="serve-routes-head">
        <h3>{heading}</h3>
        <p>{deck}</p>
      </div>
      <div class="serve-routes-grid">
{chr(10).join(out)}
      </div>
    </div>"""


def split(left: dict, right: dict, *, highlight_right: bool = True) -> str:
    """Two facing prose columns. Each side: {label, body} where body is HTML."""
    hl = " lp-col--lit" if highlight_right else ""
    return f"""    <div class="lp-split rise">
      <div class="lp-col">
        <div class="lp-col-label">{left["label"]}</div>
{left["body"]}
      </div>
      <div class="lp-col{hl}">
        <div class="lp-col-label">{right["label"]}</div>
{right["body"]}
      </div>
    </div>"""


def compare_table(caption: str, cols: tuple[str, str], rows: list[tuple[str, str, str]],
                  foot: str = "") -> str:
    """A two-option comparison. rows: (row label, col A cell, col B cell).

    Cells collapse to stacked cards under 700px using the data-l attribute,
    so the column header is never lost on a phone.
    """
    body = []
    for label, a, b in rows:
        body.append(f"""        <tr>
          <td class="lp-table-key">{label}</td>
          <td data-l="{escape(_strip_tags(cols[0]), quote=True)}">{a}</td>
          <td data-l="{escape(_strip_tags(cols[1]), quote=True)}">{b}</td>
        </tr>""")
    tail = f'\n      <p class="lp-table-foot">{foot}</p>' if foot else ""
    return f"""    <div class="lp-table-wrap rise">
      <table class="lp-table">
        <caption class="lp-table-caption">{caption}</caption>
        <thead>
          <tr><th scope="col"></th><th scope="col">{cols[0]}</th><th scope="col">{cols[1]}</th></tr>
        </thead>
        <tbody>
{chr(10).join(body)}
        </tbody>
      </table>{tail}
    </div>"""


def ledger(groups: list[dict]) -> str:
    """Requirement lists with a who-owns-it badge on each row.

    groups: {title, note?, wide?, items: [(text, owner)]} where owner is
    "tulq", "you", or "" for shared. A wide group spans both columns and
    lays its own rows out two-up, which is what the long recurring-monthly
    group wants rather than a squeezed single column.
    """
    out = []
    n = 0
    for g in groups:
        rows = []
        for text, owner in g["items"]:
            n += 1
            badge = ""
            if owner == "tulq":
                badge = '<span class="lp-own lp-own--t">TULQ</span>'
            elif owner == "you":
                badge = '<span class="lp-own lp-own--y">Your practice</span>'
            rows.append(
                f'          <li><span class="lp-ledger-n">{n:02d}</span>'
                f'<span class="lp-ledger-t">{text}</span>{badge}</li>'
            )
        note_html = f'\n        <p class="lp-ledger-note">{g["note"]}</p>' if g.get("note") else ""
        wide = " lp-ledger-group--wide" if g.get("wide") else ""
        out.append(f"""      <div class="lp-ledger-group{wide} rise">
        <div class="lp-ledger-head">{g["title"]}</div>{note_html}
        <ul class="lp-ledger-list">
{chr(10).join(rows)}
        </ul>
      </div>""")
    return '    <div class="lp-ledger">\n' + "\n".join(out) + "\n    </div>"


def note(body: str, kind: str = "caution") -> str:
    mark = "!" if kind == "caution" else "i"
    return f"""    <div class="lp-note lp-note--{kind} rise">
      <span class="lp-note-mark" aria-hidden="true">{mark}</span>
      <div>{body}</div>
    </div>"""


def prose(html: str, wide: bool = False) -> str:
    cls = "lp-prose lp-prose--wide" if wide else "lp-prose"
    return f'    <div class="{cls} rise">\n{html}\n    </div>'


def faq(qa: list[tuple[str, str]]) -> str:
    """qa: (question, answer HTML). An answer may end with an <a class="faq-source">."""
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
    return '    <div class="faq-list rise">\n' + "\n".join(items) + "\n    </div>"


def source_link(label: str, url: str) -> str:
    return (f'          <a class="faq-source" href="{url}" target="_blank" '
            f'rel="noopener">Source: {label}</a>')


def sources(items: list[tuple[str, str]], disclaimer: str = "") -> str:
    rows = "\n".join(
        f'        <li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>'
        for label, url in items
    )
    tail = f'\n      <p class="lp-sources-note">{disclaimer}</p>' if disclaimer else ""
    return f"""    <div class="lp-sources rise">
      <div class="lp-sources-head">Sources</div>
      <ul>
{rows}
      </ul>{tail}
    </div>"""


def section_links(items: list[tuple[str, str]]) -> str:
    rows = "\n".join(f'      <a href="{href}">{label}</a>' for label, href in items)
    return f'    <div class="section-links rise">\n{rows}\n    </div>'


def contact_close(title: str, deck: str, *, cap_title: str, cap_body: str,
                  eyebrow: str = "Next step") -> str:
    """The closing band. Carries both seams, so it must be the last section.

    The two seams ramp cream to basalt to ink across ~200px each. See the
    house-style note in CLAUDE.md: the cream seam has to reach alpha 0 and
    be front-loaded, or it reads as a grey fog bank over the photograph.
    """
    return f"""<section class="contact section-dark contact-dark" id="contact" data-screen-label="Contact">
{_scene("contact")}
  <div class="sec-seam sec-seam--from-cream" aria-hidden="true"></div>
  <div class="sec-seam sec-seam--to-ink" aria-hidden="true"></div>
  <div class="container">
    <div class="contact-head rise">
      <span class="eyebrow eyebrow-dark" style="justify-content:center; display:inline-flex;">
        <span class="dot" aria-hidden="true"></span>
        {eyebrow}
      </span>
      <h2>{title}</h2>
      <p>{deck}</p>
    </div>
    <div class="contact-split">
      <div class="contact-reach">
        <div class="contact-reach-person rise">
          <div class="contact-reach-role">Founder · CEO · President</div>
          <div class="contact-reach-name">Michael Chavez Ross</div>
          <a class="contact-reach-email" href="mailto:michael@tulq.health">michael@tulq.health</a>
        </div>
        <div class="contact-reach-person rise">
          <div class="contact-reach-role">Clinical Director · RN, BSN</div>
          <div class="contact-reach-name">Jayson Forrest Minagawa</div>
          <a class="contact-reach-email" href="mailto:jayson@tulq.health">jayson@tulq.health</a>
        </div>
      </div>
      <div class="cap rise">
        <div class="cap-body">
          <div class="cap-eye">{cap_title}</div>
          <h4>{cap_body}</h4>
          <p>Ask and we will send it the same day, with the reimbursement figures run against your own locality rather than a national average.</p>
        </div>
        <a class="btn btn-amber" href="/contact" data-magnetic>
          Get in touch
          <span class="orb" aria-hidden="true">{ARROW_SVG}</span>
        </a>
      </div>
    </div>
  </div>
</section>"""


# ── Nav / footer, rendered in the homepage's markup from the Site config ──

def _nav(page: LandingPage) -> str:
    p = page.asset_prefix
    rows = []
    for label, href in page.site.nav:
        target = href.strip("/")
        slug = page.slug.rstrip("/").removesuffix("/index")
        current = ""
        if slug == target or (href.endswith("/") and slug.startswith(target + "/")):
            current = ' aria-current="page"'
        rows.append(f'      <a href="{href}"{current}>{label}</a>')
    return f"""<div class="nav-wrap" id="nav" data-mode="dark">
  <nav class="nav" aria-label="Primary">
    <a href="/" class="brand" aria-label="TULQ home">
      <img class="brand-logo" src="{p}assets/logo.webp" alt="" width="32" height="32" fetchpriority="high" decoding="async" />
      <span>TULQ</span>
    </a>
    <div class="nav-links">
{chr(10).join(rows)}
    </div>
    <a class="nav-cta" href="/contact" data-magnetic>
      <span class="dot-live" aria-hidden="true"></span>
      <span>Contact us</span>
    </a>
  </nav>
</div>"""


def _footer(page: LandingPage) -> str:
    p = page.asset_prefix
    cols = []
    for head, links in page.site.footer_cols:
        items = "\n".join(f'          <a href="{href}">{label}</a>' for label, href in links)
        cols.append(f"""        <div class="site-footer-col">
          <div class="site-footer-col-head">{head}</div>
{items}
        </div>""")
    legal = "\n".join(f"        <span>{item}</span>" for item in page.site.legal)
    return f"""<footer class="site-footer">
  <div class="site-footer-river" aria-hidden="true">
    <svg viewBox="0 0 1180 44" preserveAspectRatio="none">
      <path class="path-tolt" d="M 0,14 C 200,14 380,30 590,22 C 800,14 980,30 1180,22"/>
      <path class="path-snoq" d="M 0,30 C 200,30 380,14 590,22 C 800,30 980,14 1180,22"/>
    </svg>
  </div>
  <div class="site-footer-inner">
    <div class="site-footer-top">
      <div class="site-footer-brand">
        <img class="site-footer-logo" src="{p}assets/logo.webp" alt="TULQ" width="68" height="68" loading="lazy" decoding="async" />
        <p class="site-footer-brand-name">TULQ</p>
        <p class="site-footer-tagline">tultx&#695; · where two currents meet</p>
        <p class="site-footer-mission">{page.site.mission}</p>
      </div>
      <nav class="site-footer-nav" aria-label="Footer navigation">
{chr(10).join(cols)}
      </nav>
    </div>
    <div class="site-footer-bottom">
      <div class="site-footer-legal">
{legal}
      </div>
      <span class="site-footer-mark">tultx&#695;</span>
    </div>
  </div>
</footer>"""


# ── Schema ────────────────────────────────────────────────────────────

def _reviewer(site: Site) -> dict:
    return {
        "@type": "Person",
        "name": "Jayson Forrest Minagawa",
        "honorificSuffix": "RN, BSN",
        "jobTitle": "Clinical Director",
        "worksFor": {"@id": site.org_id},
    }


def service_node(page: LandingPage, name: str, service_type: str, description: str,
                 audience: str = "", offers: list[dict] | None = None) -> dict:
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
    if offers:
        node["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": f"{name} options",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": o["name"],
                                                   "description": o["description"]}}
                for o in offers
            ],
        }
    return node


def faq_node(page: LandingPage, qa: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{page.url}#faq",
        "url": f"{page.url}#faq",
        "inLanguage": "en-US",
        "isPartOf": {"@id": page.site.website_id},
        "mainEntity": [
            {"@type": "Question", "name": _strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": _strip_tags(a)}}
            for q, a in qa
        ],
    }


def breadcrumb_node(page: LandingPage, trail: list[tuple[str, str]]) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Home",
              "item": f"{page.site.base}/"}]
    for i, (label, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": _strip_tags(label),
                      "item": f"{page.site.base}{href}"})
    return {"@type": "BreadcrumbList", "@id": f"{page.url}#breadcrumb",
            "itemListElement": items}


def _webpage_node(page: LandingPage) -> dict:
    node = {
        "@type": "WebPage",
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
    if page.reviewed:
        node["reviewedBy"] = _reviewer(page.site)
        node["dateModified"] = page.published
    return node


def build_schema(page: LandingPage) -> str:
    graph = [_webpage_node(page)] + page.schema
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      indent=2, ensure_ascii=False)


# ── House-style guard ─────────────────────────────────────────────────

class CopyError(ValueError):
    pass


def check_copy(page: LandingPage, html: str) -> None:
    """Fail the build rather than ship a house-style regression.

    CLAUDE.md makes two of these hard rules, and both have shipped by
    accident before, so they are checked here rather than trusted to review.
    """
    if "—" in html or "&mdash;" in html:
        raise CopyError(f"{page.slug}: em dash in visible copy (CLAUDE.md house style)")
    plain = _strip_tags(page.title)
    if len(plain) > 60:
        raise CopyError(f"{page.slug}: title is {len(plain)} chars, limit is 60 -> {plain!r}")
    desc = _strip_tags(page.description)
    if not (120 <= len(desc) <= 165):
        raise CopyError(
            f"{page.slug}: meta description is {len(desc)} chars, needs 120-165"
        )


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
<meta property="og:type" content="website" />
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

<link rel="stylesheet" href="{p}styles.css" />
{extra_head}{extra_css}
<script type="application/ld+json">
{schema}
</script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-progress" id="scroll-progress" aria-hidden="true"></div>

{nav}

<main id="main">
{body}
</main>

{footer}

<script src="{p}landing.js"></script>
{extra_js}
</body>
</html>
"""


def render(page: LandingPage) -> str:
    p = page.asset_prefix
    body = "\n\n".join([hero(page)] + page.sections).replace("{p}", p)
    extra_head = f"{page.extra_head.replace('{p}', p)}\n" if page.extra_head else ""
    extra_css = f"<style>\n{page.extra_css}\n</style>\n" if page.extra_css else ""
    # A tool page may want a <script src> rather than an inline block; anything
    # starting with a tag is passed through as authored.
    extra_js = ""
    if page.extra_js:
        raw = page.extra_js.strip()
        extra_js = raw if raw.startswith("<") else f"<script>\n{page.extra_js}\n</script>"
        extra_js = extra_js.replace("{p}", p)
    html = TEMPLATE.format(
        title=page.title,
        description=escape(_strip_tags(page.description), quote=True),
        url=page.url,
        base=page.site.base,
        domain=page.site.domain,
        p=p,
        schema=build_schema(page),
        nav=_nav(page),
        body=body,
        footer=_footer(page),
        extra_head=extra_head,
        extra_css=extra_css,
        extra_js=extra_js,
    )
    check_copy(page, _visible(html))
    return html


def _visible(html: str) -> str:
    """Strip script/style so the em-dash guard only reads visible copy."""
    return re.sub(r"<(script|style)\b.*?</\1>", "", html, flags=re.S | re.I)


def write(page: LandingPage):
    out = page.out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(page), encoding="utf-8")
    return out
