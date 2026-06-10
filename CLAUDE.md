# TULQ Site

## Brand / Logo

- **The official TULQ logo is the metallic "T" mark** (gunmetal Coast Salish
  formline "T" with a green malachite arm, copper basket-weave, and garnet
  pavé, "TULQ" engraved at the base). Use this mark for ALL logo/icon/brand
  needs from now on. Do not reintroduce the old gradient-"t" placeholder.
- **File location**: `assets/logo.png` (and a mirror copy at
  `care/assets/logo.png` for the self-contained `care/` subsite). Transparent
  background PNG. Referenced relatively as `assets/logo.png` from every page.
- **Where it's wired in** (all reference `assets/logo.png`):
  - Favicon + apple-touch-icon on all 8 pages.
  - Nav brand lockup — `.brand-logo` `<img>` next to the "TULQ" wordmark.
  - Footer brand — `.site-footer-logo` `<img>` above the wordmark (index +
    privacy, root and care).
- **Performance**: the logo only ever displays small (~38px nav, ~68px
  footer), so ship a SMALL, tightly-cropped PNG (256–512px square is plenty).
  `tools/optimize-logo.sh` trims/quantizes the master and mirrors it into both
  `assets/` dirs (optionally emitting WebP/AVIF). Keep `width`/`height` on every
  `<img>` to avoid layout shift; nav logo is `fetchpriority="high"`, footer is
  `loading="lazy"`.
- `assets/favicon.svg` is the retired placeholder mark (kept in the repo but no
  longer linked).

## Keys & credentials

- **Web3Forms access key**: `e35bd9a3-dae5-489d-930c-8ce8971006f3`
  - Used in `index.html` for the contact form submission
  - Free tier, submissions go to the owner's email registered at web3forms.com
