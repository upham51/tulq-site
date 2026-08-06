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
- `tools/pagekit.py` holds the shared shell: nav, footer, breadcrumbs, FAQ
  accordions, schema builders, and the two `Site` configs. Nav and footer links
  for generated pages live in the `Site` definitions there.
- **Hand-written pages** (not generated, edit directly): `index.html`,
  `story.html`, `contact.html`, `privacy.html` on both sites.
- `pages.css` styles the generated pages; `styles.css` styles the hand-written
  ones. Both exist in the root and mirrored in `care/`.

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
  instead. Do not remove those sections.
- **No opacity entrance animations on `pages.css`.** A blank column while CSS
  loads is the wrong trade for the rural/low-bandwidth audience this content
  targets. The homepage keeps its motion; content pages do not.

## Keys & credentials

- **Web3Forms access key**: `e35bd9a3-dae5-489d-930c-8ce8971006f3`
  - Used in `index.html` for the contact form submission
  - Free tier, submissions go to the owner's email registered at web3forms.com
