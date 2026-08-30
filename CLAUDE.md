# TULQ Site

## Domains

- **Root site** (`/`, IHS/tribal-facing): `tulq.health`
- **B2B / non-tribal site** (`care/` subsite): **`tulqhealth.com`** — this is
  the live, canonical domain as of 2026-07-25. The README's mention of
  `care.tulq.health` as the custom domain target predates this and should be
  treated as superseded wherever the two conflict.

## Brand / Logo

- **The official TULQ logo is the metallic "T" mark** (gunmetal Coast Salish
  formline "T" with a green malachite arm, copper basket-weave, and garnet
  pavé, "TULQ" engraved at the base). Use this mark for ALL logo/icon/brand
  needs from now on. Do not reintroduce the old gradient-"t" placeholder.
- **File location**: `assets/logo.webp` (and a mirror copy at
  `care/assets/logo.webp` for the self-contained `care/` subsite).
  Transparent-background WebP — small and fast. Referenced relatively as
  `assets/logo.webp` from every page.
- **Where it's wired in** (all reference `assets/logo.webp`):
  - Favicon (`type="image/webp"`) + apple-touch-icon on all 8 pages. Note:
    WebP favicons render in Chrome/Edge/Firefox but NOT Safari/iOS — to cover
    those, also drop a small `assets/logo.png` and add a PNG `rel="icon"` line.
  - Nav brand lockup — `.brand-logo` `<img>` next to the "TULQ" wordmark.
  - Footer brand — `.site-footer-logo` `<img>` above the wordmark (index +
    privacy, root and care).
- **Performance**: the logo only ever displays small (~38px nav, ~68px
  footer), so ship a SMALL, tightly-cropped image (256–512px square is plenty).
  WebP is already the fast format. Keep `width`/`height` on every `<img>` to
  avoid layout shift; nav logo is `fetchpriority="high"`, footer is
  `loading="lazy"`. `tools/optimize-logo.sh` can re-trim/shrink a master and
  emit variants.
- `assets/favicon.svg` is the retired placeholder mark (kept in the repo but no
  longer linked).

## House style

These are held to across both sites. A change that reintroduces any of them
is a regression, not a preference.

- **No em dashes in visible copy.** Use a comma, a colon, a semicolon, a
  period, or parentheses, whichever the sentence actually calls for. This is a
  hard rule: `grep -r '—\|&mdash;' --include=*.html .` must come back empty.
- **Nav is destinations only, never one link per homepage section.** Three
  links plus a Contact us CTA, on every page of a site:
  - tulq.health: IHS Areas, Resources, Our story
  - tulqhealth.com: Services, Compare, Resources

  "Our story" left the tulqhealth.com bar when Services arrived, to keep it at
  three. It is still in the footer's Company column.

  Generated pages get this from the `nav=` tuple on each `Site` in
  `tools/pagekit.py`; the eight hand-written pages carry the same markup
  inline. Change one, change both.
- **Every cited source is a link, and every link has been checked.** FAQ
  sources on the homepages are `<a class="faq-source">`; resource-page Sources
  lists take `(label, url)` pairs in `sources_block()`. Never write a URL you
  have not actually requested, and prefer the primary document (eCFR,
  uscode.house.gov, the CMS or IHS program page) over a summary of it. Note
  that `bphc.hrsa.gov` and `gao.gov` return 403 to a plain `curl`; both are
  live, so verify those in a real browser rather than assuming they are dead.
- **The homepage hero is one typeface in two styles, and nothing else.**
  Everything in `.hero` is `var(--serif)` roman; the single `<em>` inside the
  H1 is the only italic. No mono, no sans, no second italic, no eyebrow. The
  hero is four elements deep at most (H1, `.hero-sub`, `.hero-facts`,
  `.hero-ctas`) and must land whole above the fold at 1280x720 and 360x640.
  Facts go in `.hero-facts` as short `<span>`s, not in a prose paragraph.
  Adding a font, a paragraph, or a fifth element back is a regression.
- **The closing run of each homepage is one continuous fall into the footer.**
  `.sec-seam--from-cream` and `.sec-seam--to-ink` inside the contact section
  ramp cream to basalt to ink across ~200px each. Do not give the contact band
  a hard top or bottom edge. Two rules govern the cream seam, and it took three
  attempts to get both right at once:
  - It must reach **alpha 0** at its bottom. An opaque ramp ending on a flat
    colour cannot match a section whose real background is basalt plus two
    radial gradients plus a photograph, so it leaves a visible line.
  - Its alpha must be **front-loaded**. A linear ramp spends half its height
    near 50% cream, and a full-width band of that over a dark section is the
    grey fog bank the seam is meant to avoid.
- **Card footers sit on the card floor.** `.pillar-source` and
  `.serve-card-tag` are footers: `margin-top: auto`, with `min-height` on
  `.pillar-source` reserving the two lines its longest citation needs so the
  dashed rules stay level. If you add a `.serve-card-link` to one card in a
  row, add one to all of them, or the tags fall out of line.

## Content pages & the generator

Most pages on both sites are **generated**, not hand-written. The repo is still
plain static HTML with no build step at deploy time — the generator emits
finished `.html` that is committed to git and served directly.

- **Run it**: `python3 tools/build-pages.py` (needs nothing but stdlib). It
  writes all 37 content pages, rewrites both `sitemap.xml` files, and mirrors
  `pages.css` into `care/`.
- **Edit content in `tools/content_*.py`, not in the generated HTML.** Hand
  edits to a generated page survive until the next run, then vanish.
  - `content_tribal.py` — the three tulq.health pillars
  - `content_tribal_areas.py` — `/areas/` index + 12 IHS Area pages
  - `content_tribal_resources.py` — tribal `/resources/` + the tribal compare page
  - `content_care.py` — the two tulqhealth.com pillars
  - `content_care_resources.py` — mainstream `/resources/` + `/compare/`
  - `content_care_services.py` — the `/services/` hub + three money pages
  - `content_care_tools.py` — the two free tools under `/tools/`
  - `content_care_awv.py` — the `/awv` plain-English guide to how a
    nurse-run wellness visit gets paid
- `tools/pagekit.py` holds the shared shell: nav, footer, breadcrumbs, FAQ
  accordions, schema builders, and the two `Site` configs. Nav and footer links
  for generated pages live in the `Site` definitions there.
- **There are two page shapes, and picking the wrong one is the usual mistake.**
  - `pagekit.Page` renders the narrow article column on `pages.css`. Right for
    resource posts, segment pages, and comparisons.
  - `landing.LandingPage` renders the homepage look on `styles.css`: full-bleed
    sections alternating cream and basalt, each with a Pexels scene photo, plus
    the hero and the closing contact band with its two seams. Right for the
    hub, the three service pages, and the tools. Its section vocabulary is
    listed in the `tools/landing.py` docstring. Components it added are
    namespaced `.lp-*` and live in the LANDING PAGES block at the bottom of
    `care/styles.css`.

  `landing.render()` fails the build on a house-style regression: an em dash in
  visible copy, a `<title>` over 60 characters, or a meta description outside
  120 to 165. Fix the copy rather than the guard.
- **Hand-written pages** (not generated, edit directly): `index.html`,
  `story.html`, `contact.html`, `privacy.html` on both sites.
  - `contact.html` is **one panel on one screen** by design: a single card on a
    dark stage, sized off the viewport so it lands whole on a laptop without
    scrolling. It has one `<h1>` and no second heading. If you add a field,
    take the height back somewhere else rather than letting the page scroll.
- `pages.css` styles the generated pages; `styles.css` styles the hand-written
  ones. Both exist in the root and mirrored in `care/`.

### Editing CSS — read this before you touch a stylesheet

`_headers` serves `/*.css` with `max-age=31536000, immutable`. A stylesheet
URL is therefore cached for a **year**, by browsers and by Cloudflare's edge.
Changing `styles.css` without changing its URL ships nothing — visitors keep
the old bytes. This has bitten the site once already: the FAQ styles were
added under an unchanged `styles.css?v=9`, so the markup went live and the
CSS did not, and the accordion rendered as bare `<details>` triangles in
production for two days.

Every stylesheet reference now carries a **content hash**, applied by
`python3 tools/stamp-assets.py`. `build-pages.py` runs it automatically at
the end of every build. So:

- After editing `styles.css`, `pages.css`, or any of the stamped scripts
  (`rivers.js`, `landing.js`, `awv-worksheet.js`, `awv-worksheet.css`), run
  `tools/stamp-assets.py` (or just `tools/build-pages.py`, which calls it).
  `_headers` caches `/*.js` on the same immutable year as CSS, so scripts are
  content-hashed too.
- Never hand-write `?v=` numbers. The tool owns that query string and will
  overwrite them.
- The same trap applies to `/assets/*`, which is also immutable. If you
  change an image's *contents*, give it a new filename rather than relying
  on the cache to notice.

### Checks worth running after any change

- `python3 tools/check-links.py` — every site-absolute link and relative asset
  resolves to a file that exists. Remember `/` means the repo root on
  tulq.health and the `care/` directory on tulqhealth.com.
- `python3 tools/fetch-optimize-images.py` then `tools/rewrite-image-refs.py`
  if imagery ever needs re-pulling from source.

## SEO conventions

These came out of the Aug 2026 dual-track keyword research and should be held to:

- **Title tags**: `Primary Keyword | Benefit | TULQ`, **under 60 characters**,
  unique across both sites. Do not lead with the brand — at DR 0 it has no
  search volume.
- **Meta descriptions**: unique, **120–165 characters**, ending in a CTA.
- **The poetic H1s on the homepages stay.** Search intent is carried by an
  `<h2 class="hero-sub">` directly beneath, not by flattening the H1.
- **Schema**: one `@graph` per page. `MedicalOrganization` is the root entity
  (`@id` = `https://<domain>/#organization`); the two domains reference each
  other via `sameAs` so they read as one entity. Clinical pages carry
  `reviewedBy` pointing at Jayson Minagawa, RN, BSN — the highest-impact YMYL
  property, per the research.
- **Both `privacy.html` files are `noindex, follow`** and absent from the
  sitemaps. They are ~94% identical across the two domains; keeping one copy out
  of the index avoids a cross-domain duplicate on two DR-0 domains.
- **Factual claims cite public sources only** (IHS, CMS, KFF, HRSA, statute,
  CFR, SAM.gov) and carry a dated disclaimer. TULQ is pre-launch: no page claims
  call volumes, uptime, or client references. Say so plainly rather than
  implying otherwise — the comparison pages depend on that credibility.
- **Comparison pages name competitors factually**, describe them from their own
  public materials, and explicitly say when the reader should choose them
  instead. Do not remove those sections. There are now two competitive sets
  under `/compare/`, and they take different evaluation questions
  (`TRIAGE_QUESTIONS` and `CARE_QUESTIONS` in `content_care_resources.py`):
  - Triage: IntellaTriage, Conduit Health Partners, AccessNurse.
  - Care management: ChartSpan (full-service scale), Signallamp (the closest
    analogue to our model; now part of Tellihealth), ThoroughCare (software,
    not staffing, so the page resolves the category error first).

  The Signallamp page turns on flat fee against revenue share. Keep that
  argument factual: a revenue share is not unlawful, it is a different
  compliance posture, and the page says so.

### One buyer segment, one page (tulqhealth.com)

Two pages on the same domain chasing the same query split the signal and
usually rank neither. The four mainstream segment pages are deliberately
scoped so none of them overlap:

| Segment | Page | Authored |
|---|---|---|
| Hospice | `/nurse-triage-for-hospice` | Hand-written (PR #88) |
| Home health | `/for/home-health` | Generated |
| RHC + critical access hospitals | `/nurse-triage-for-rural-health-clinics` | Hand-written (PR #88) |
| FQHC / community health centers | `/for/health-centers` | Generated |

### Three service lines, three money pages, one hub

The same rule one level up. The Aug 2026 research is explicit that the three
service lines need separate URLs, because the buyers, the SERPs, and the
keyword sets barely overlap:

| Service line | Page | Primary keyword |
|---|---|---|
| Hub | `/services/` | nurse-led clinical services |
| After-hours triage | `/services/after-hours-nurse-triage` | after hours nurse triage service |
| Care management | `/services/care-management` | care management outsourcing for small practices |
| Annual wellness visits | `/services/medicare-annual-wellness-visits` | annual wellness visit outsourcing |

The homepage is no longer the triage money page: its `hero-sub` covers all
three lines and it routes to the hub. The four segment pages above are
practice-type modifiers **on the triage service** and sit under it. Do not let
`/services/after-hours-nurse-triage` start covering hospice or RHC specifics,
or it will cannibalise them; it targets the unmodified head term and links
down. Likewise `/services/care-management` links across to
`/resources/apcm-billing-fqhc-rhc` rather than re-arguing health-center billing.

Two free ungated tools feed the AWV and care management pages:
`/tools/awv-revenue-calculator` and `/tools/annual-wellness-visit-worksheet`.
They stay ungated on purpose: an email wall makes them uncrawlable and
unlinkable, which is the whole value at DR 0.

**The AWV line carries three pages and they must not converge.** The money
page sells and quotes rates; `/resources/who-can-perform-annual-wellness-visit`
answers the evaluative "who may perform versus who may bill" query; `/awv`
answers the trust question that follows the sales call, walking the whole
regulatory chain rule by rule and describing the workflow end to end. `/awv`
therefore does not quote per-visit reimbursement and does not argue completion
rates. `/avw`, the transposition people type, 301s to it in `care/_redirects`.

That chain rests on three sections of 42 CFR, and the third one moved
recently. Direct supervision (`410.32(b)(3)(ii)`, incorporated by
`410.26(a)(2)`) still means immediately available throughout, but since
1 January 2026 that presence **may be virtual, through real-time audio and
video excluding audio-only**, adopted permanently in the CY2026 Physician Fee
Schedule final rule. Pages written before that described it as office-suite
only; if an edit reintroduces "not reachable by phone" as the whole of the
definition, check the current eCFR text before restoring it. The
patient-facing audio-only telehealth allowance is a separate rule and does
carry a date, so keep the two apart.

`/resources/` is organised into the same three tracks, and the four triage
segment pages carry a cross-sell footer (`_also()` in `content_care.py`) that
routes to the other two lines. That block is deliberately a footer, not body
copy: those pages rank for triage queries and promoting it into the argument
would dilute them.

Note the RHC page covers **both** RHCs and CAHs, which is why `/for/health-centers`
stops at FQHCs and links across rather than covering CAHs itself. Each page
carries a callout pointing readers at the neighbouring segment.

Before broadening any of these, retire the page it would start competing with.
Adding a fifth page that overlaps an existing one is the failure mode to avoid.
- **No opacity entrance animations on `pages.css`.** A blank column while CSS
  loads is the wrong trade for the rural/low-bandwidth audience this content
  targets. The homepage keeps its motion; content pages do not.

## Keys & credentials

- **Web3Forms access key**: `e35bd9a3-dae5-489d-930c-8ce8971006f3`
  - Used in `index.html` for the contact form submission
  - Free tier, submissions go to the owner's email registered at web3forms.com
