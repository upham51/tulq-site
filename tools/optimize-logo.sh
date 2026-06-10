#!/usr/bin/env bash
#
# optimize-logo.sh — squeeze the TULQ logo for fast loading.
#
# The logo only ever displays small (~38px in the nav, ~68px in the footer),
# so we never need to ship the multi-megabyte master export. This script:
#   1. Trims transparent borders off the master so the mark fills the frame.
#   2. Produces a small, quantized PNG at assets/logo.png (and mirrors it into
#      care/assets/logo.png for the self-contained care/ subsite).
#   3. Optionally emits WebP + AVIF variants (5–15x smaller) if encoders exist.
#
# Usage:
#   1. Drop your full-resolution export at assets/logo-master.png
#      (falls back to assets/logo.png if no master is present).
#   2. From the repo root, run:  bash tools/optimize-logo.sh
#
# Requires ImageMagick (`magick` or `convert`). cwebp/avifenc are optional.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SRC="assets/logo-master.png"
[ -f "$SRC" ] || SRC="assets/logo.png"

if [ ! -f "$SRC" ]; then
  echo "✗ No source logo found. Add assets/logo-master.png (or assets/logo.png) first." >&2
  exit 1
fi

# Pick an ImageMagick entrypoint.
if command -v magick >/dev/null 2>&1; then IM="magick"
elif command -v convert >/dev/null 2>&1; then IM="convert"
else
  echo "✗ ImageMagick not found (need 'magick' or 'convert')." >&2
  exit 1
fi

# Longest edge for the shipped PNG. 512 is crisp on retina at our display sizes.
SIZE="${LOGO_SIZE:-512}"
OUT="assets/logo.png"

echo "→ Source: $SRC"
echo "→ Trimming transparent borders, resizing to ${SIZE}px, quantizing…"

# -trim removes the transparent margin; +repage resets the canvas; a tiny
# transparent border keeps the mark from touching the edges; -strip drops
# metadata. PNG8 (256-color) is dramatically smaller and visually lossless
# for a mark like this.
$IM "$SRC" \
  -trim +repage \
  -resize "${SIZE}x${SIZE}>" \
  -bordercolor none -border 4% \
  -strip \
  -define png:compression-level=9 \
  PNG32:"$OUT"

# Mirror into the care/ subsite so it stays self-contained.
mkdir -p care/assets
cp "$OUT" care/assets/logo.png
echo "✓ Wrote $OUT and care/assets/logo.png ($(du -h "$OUT" | cut -f1))"

# --- Optional next-gen formats -------------------------------------------
if command -v cwebp >/dev/null 2>&1; then
  cwebp -quiet -q 90 -alpha_q 100 "$OUT" -o assets/logo.webp
  cp assets/logo.webp care/assets/logo.webp
  echo "✓ Wrote assets/logo.webp ($(du -h assets/logo.webp | cut -f1))"
else
  echo "· cwebp not found — skipping WebP (install libwebp for a smaller variant)."
fi

if command -v avifenc >/dev/null 2>&1; then
  avifenc --min 20 --max 30 "$OUT" assets/logo.avif >/dev/null 2>&1 || true
  [ -f assets/logo.avif ] && cp assets/logo.avif care/assets/logo.avif \
    && echo "✓ Wrote assets/logo.avif ($(du -h assets/logo.avif | cut -f1))"
else
  echo "· avifenc not found — skipping AVIF."
fi

echo ""
echo "Done. If you generated .webp/.avif and want browsers to prefer them,"
echo "upgrade the nav/footer <img> tags to <picture> with avif → webp → png"
echo "sources (or just ask Claude to do it)."
