# Tulq — landing site

Static landing site for **Tulq**, a Native-led 24/7 nurse advice line for IHS beneficiaries. Built with the Nursing Directory UI Kit aesthetic — warm cream, teal, amber accents, Instrument Serif headers.

## care.tulq.health — universal subdomain

The `care/` directory is a **self-contained mirror of this site with the IHS/tribal targeting removed** and the copy retargeted at the broader regulated B2B market (FQHCs/RHCs, hospice & home health, Critical Access Hospitals, and DPC/pediatric/OB practices). The UI, CSS, JS, and rivers visual are byte-identical to the root site; only the content differs. The TULQ name and its `tultxʷ` origin story are kept as a respectful etymology, but the site no longer targets Indian Country.

It is built to be deployed as its **own Cloudflare Pages project** bound to `care.tulq.health`:

1. **Workers & Pages → Create application → Pages → Connect to Git** → select this repo
2. Configure build:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `care`
   - **Root directory:** `/`
3. **Save and Deploy**, then in the project's **Custom domains** tab add `care.tulq.health` (one click if the zone is on Cloudflare DNS).

The existing root project (the tribal/IHS site) is untouched and keeps serving `tulq.health` / `tulq-site.pages.dev`.

## Structure

```
tulq-site/
├── index.html          ← landing page
├── story.html          ← deeper Our Story / Ollie Moses + Chemawa narrative
├── assets/
│   ├── favicon.svg
│   ├── michael.jpg     ← Michael's headshot (already in place)
│   └── jayson.jpg      ← drop your headshot here when ready
├── _headers            ← Cloudflare Pages security + cache headers
├── _redirects          ← /story → /story.html alias
├── .gitignore
└── README.md
```

## Founders pictured

- **Michael Chavez Ross** — Founder, CEO & President. Photo is in `assets/michael.jpg`.
- **Jayson Minagawa** — Clinical Director, RN. **Drop `jayson.jpg` into `/assets/`** (any square crop, 600×600 or larger works best). Until then, the leadership card shows a stylized `JM` monogram in the same aesthetic.

## Deploy to Cloudflare Pages — step by step

The site is plain static HTML, no build step required.

### 1. Create the GitHub repo

```bash
cd tulq-site
git init
git add .
git commit -m "Initial commit: Tulq landing"
git branch -M main
# Create a new repo on github.com/<your-org>/tulq-site (Private is fine)
git remote add origin git@github.com:<your-org>/tulq-site.git
git push -u origin main
```

### 2. Connect Cloudflare Pages

1. Go to **Cloudflare dashboard → Workers & Pages → Create application → Pages → Connect to Git**
2. Authorize GitHub if not already; select the `tulq-site` repo
3. Configure build:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
   - **Root directory:** `/`
4. Click **Save and Deploy**
5. After ~30 seconds you'll get a `https://tulq-site.pages.dev` URL — share that with the contracting officer

### 3. Custom domain (optional, when ready)

In the project's **Custom domains** tab, click **Set up a custom domain** and follow the DNS prompts. If the domain is on Cloudflare DNS already, this is one click.

### 4. Future updates

Just `git push` to `main`. Cloudflare Pages rebuilds and redeploys automatically (usually under 30 seconds).

## Editing content

Everything is in two flat HTML files with all styles inlined — no framework, no toolchain. Open `index.html` or `story.html` in any editor, change copy, push, done.

### Common edits

- **Update phone / email** — search for `206-420-9055` in `index.html`, or `upham51@gmail.com`
- **Update bios** — see the `<article class="leader">` blocks in `index.html`
- **Update the hero photo** — replace the URL inside `.hero-photo` (currently a Pexels-hosted image by Tessy Agbonome)
- **Update the "Who we serve" photo** — same pattern inside `.serve-photo`
- **Swap in real Jayson headshot** — drop `assets/jayson.jpg`. No code change required; the JM monogram is automatically replaced.

## Image credits

Hero and "Who we serve" imagery courtesy of [Tessy Agbonome on Pexels](https://www.pexels.com/photo/smiling-doctor-sitting-with-smartphone-19963174/), used under the Pexels free license. Replace with custom photography for production.

## Compliance & contracting notes

- Site does **not** transmit PHI; it is a marketing site only.
- Capability statement available on request — see contact section.
- Site footer includes the disclaimer that Tulq is not affiliated with the Snoqualmie Indian Tribe.

## License & ownership

© Tulq. All rights reserved.
