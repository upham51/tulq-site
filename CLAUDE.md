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

## Keys & credentials

- **Web3Forms access key**: `e35bd9a3-dae5-489d-930c-8ce8971006f3`
  - Used in `index.html` for the contact form submission
  - Free tier, submissions go to the owner's email registered at web3forms.com
