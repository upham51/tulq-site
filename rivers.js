/* ─────────────────────────────────────────────────────────────
   Tulq — Two Rivers Canvas  (leveled-up)
   Two streams always originate from the LEFT edge: Tolt hugs
   the top, Snoqualmie the bottom.  They converge at ~56% width,
   then braid into organic delta channels that fan rightward.

   Root-cause fix: initial seeding is confined to the
   pre-confluence zone (x = 0..cx) so no water ever "appears"
   in the middle-right — every particle must flow in from left.

   Level-up: line-segment filaments, gaussian cross-section,
   shimmer glints, confluence turbulence, channel braiding noise.
   ───────────────────────────────────────────────────────────── */

(() => {
  const canvas = document.getElementById('rivers');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Stream definitions ── */
  const TOLT = { yF: 0.04, sF: 0.08, color: [168, 200, 196], pull: 0.54, vBase: 1.2, alpha: 0.52 };
  const SNOQ = { yF: 0.96, sF: 0.08, color: [107, 138, 150], pull: 0.58, vBase: 1.0, alpha: 0.46 };
  const FOG  = [232, 228, 216];
  const BG   = [28, 38, 40];

  /* ── Layout constants ── */
  const CX = 0.56, CY = 0.50;        // confluence fraction
  const BLEND_HALF = 0.08;           // transition zone half-width
  const TRAIL      = 0.04;           // trail fade per frame (lower = longer trails)
  const MAX_SPEED  = 5.5;
  const TWO_PI     = Math.PI * 2;

  /* ── Delta fan: 15 channels, gaussian-weighted toward center ── */
  const NUM_CHANNELS    = 15;
  const MAX_DELTA_ANGLE = 1.10;      // radians – tighter than before, less rectangular

  let w, h, dpr, cx, cy;
  let t0 = performance.now();
  let raf = 0;
  let particles = [];

  /* ── Helpers ── */
  function smoothstep(a, b, x) {
    const t = Math.max(0, Math.min(1, (x - a) / (b - a)));
    return t * t * (3 - 2 * t);
  }

  function channelBaseAngle(ch) {
    return (ch / (NUM_CHANNELS - 1) - 0.5) * MAX_DELTA_ANGLE;
  }

  function channelIdealY(ch, x) {
    return cy + (x - cx) * Math.tan(channelBaseAngle(ch));
  }

  /* Layered simplex-like noise → organic angle field */
  function angleAt(x, y, time) {
    const n1 =
      Math.sin(x * 0.0026 + time * 0.17) * Math.cos(y * 0.0041 + time * 0.13) +
      Math.sin(x * 0.0058 + y * 0.0049 + time * 0.22) * 0.55;
    const n2 = Math.sin(x * 0.0013 + y * 0.0023 + time * 0.09) * 0.38;
    const n3 = Math.cos(x * 0.0035 - y * 0.0017 + time * 0.14) * 0.22;
    return (n1 + n2 + n3) * Math.PI * 0.36;
  }

  /* Gaussian channel pick: center channels denser than edge channels */
  function gaussianChannel() {
    const u1 = Math.random(), u2 = Math.random();
    const z = Math.sqrt(-2 * Math.log(Math.max(1e-10, u1))) * Math.cos(TWO_PI * u2);
    const ch = Math.round(z * 2.6 + (NUM_CHANNELS - 1) / 2);
    return Math.max(0, Math.min(NUM_CHANNELS - 1, ch));
  }

  /* ── Setup / resize ── */
  function setup() {
    w = canvas.parentElement.clientWidth;
    h = canvas.parentElement.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width  = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width  = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    ctx.fillStyle = `rgb(${BG.join(',')})`;
    ctx.fillRect(0, 0, w, h);

    cx = w * CX;
    cy = h * CY;

    const isMobile = w < 760;
    const count = isMobile ? 1400 : 2600;

    particles = [];
    const half = Math.floor(count / 2);
    for (let i = 0; i < half; i++)         particles.push(spawn(TOLT, true));
    for (let i = 0; i < count - half; i++) particles.push(spawn(SNOQ, true));
  }

  /* ── Spawn ──
     ROOT-CAUSE FIX: initial particles are seeded ONLY in the
     pre-confluence zone (x ∈ [0, cx]).  Age is set proportional
     to x so particles already mid-journey look correct.
     Respawned particles always enter from the left edge band.  */
  function spawn(stream, initial) {
    const channel = gaussianChannel();
    let x, y, age;

    if (initial) {
      /* Pre-confluence zone only – never right of confluence */
      x   = Math.random() * cx * 0.97;
      y   = h * stream.yF + (Math.random() - 0.5) * h * stream.sF * 1.3;
      /* Age proportional to x so they look mid-journey, not newborn */
      const life = 350 + Math.random() * 450;
      age = (x / cx) * life * 0.60;
    } else {
      /* Respawn: always enter from left edge in stream's entry band */
      x   = Math.random() * w * 0.06;
      y   = h * stream.yF + (Math.random() - 0.5) * h * stream.sF * 1.4;
      age = 0;
    }

    return {
      x, y,
      px: x, py: y,              // previous position for filament rendering
      vx: stream.vBase * (0.55 + Math.random() * 0.55),
      vy: (Math.random() - 0.5) * 0.28,
      age,
      life: 350 + Math.random() * 450,
      seed: Math.random() * TWO_PI,
      alphaMod: 0.55 + Math.random() * 0.90,
      sizeMod:  0.70 + Math.random() * 0.65,
      shimmer:  Math.random() < 0.09,  // 9% are shimmer/glint particles
      s: stream,
      channel,
    };
  }

  /* ── Reduced-motion static fallback ── */
  function staticFallback() {
    ctx.fillStyle = `rgb(${BG.join(',')})`;
    ctx.fillRect(0, 0, w, h);
    const gt = ctx.createLinearGradient(0, 0, w, 0);
    gt.addColorStop(0,    'rgba(168,200,196,0)');
    gt.addColorStop(0.35, 'rgba(168,200,196,0.35)');
    gt.addColorStop(0.58, 'rgba(232,228,216,0.45)');
    gt.addColorStop(1,    'rgba(232,228,216,0)');
    ctx.fillStyle = gt;
    ctx.fillRect(0, h * 0.0, w, h * 0.10);
    const gs = ctx.createLinearGradient(0, 0, w, 0);
    gs.addColorStop(0,    'rgba(107,138,150,0)');
    gs.addColorStop(0.35, 'rgba(107,138,150,0.28)');
    gs.addColorStop(0.58, 'rgba(232,228,216,0.45)');
    gs.addColorStop(1,    'rgba(232,228,216,0)');
    ctx.fillStyle = gs;
    ctx.fillRect(0, h * 0.90, w, h * 0.10);
    const bloom = ctx.createRadialGradient(cx, cy, 0, cx, cy, w * 0.18);
    bloom.addColorStop(0,   'rgba(232,228,216,0.5)');
    bloom.addColorStop(0.5, 'rgba(232,228,216,0.15)');
    bloom.addColorStop(1,   'rgba(232,228,216,0)');
    ctx.fillStyle = bloom;
    ctx.beginPath();
    ctx.arc(cx, cy, w * 0.18, 0, TWO_PI);
    ctx.fill();
  }

  /* ── Animation frame ── */
  function frame() {
    if (document.hidden) { raf = requestAnimationFrame(frame); return; }

    const time   = (performance.now() - t0) / 1000;
    /* gentle breathing rhythm — surface undulation */
    const breath = 1 + 0.13 * Math.sin(time * TWO_PI / 5.4);

    /* Trail: semi-transparent BG overlay creates motion blur */
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = `rgba(${BG[0]},${BG[1]},${BG[2]},${TRAIL})`;
    ctx.fillRect(0, 0, w, h);

    const fogStart = cx - w * 0.05;
    const fogEnd   = w * 1.08;
    const blendLo  = cx - w * BLEND_HALF;
    const blendHi  = cx + w * BLEND_HALF;

    ctx.globalCompositeOperation = 'lighter';
    ctx.lineCap = 'round';        // set once, reused for all strokes

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      const s = p.s;

      /* Cache previous position for filament segment */
      p.px = p.x;
      p.py = p.y;

      /* ── Physics ── */
      const na = angleAt(p.x, p.y, time);
      const pa = Math.atan2(cy - p.y, cx - p.x);
      const distNorm = Math.abs(p.x - cx) / w + Math.abs(p.y - cy) / h;

      const mix = smoothstep(blendLo, blendHi, p.x);

      /* Pre-confluence: noise field + strong directional pull to confluence */
      const pull  = Math.min(0.91, 0.15 + distNorm * s.pull);
      const preAx = Math.cos(na) * (1 - pull) + Math.cos(pa) * pull;
      const preAy = Math.sin(na) * (1 - pull) + Math.sin(pa) * pull;
      const preFr = 0.915;

      /* Post-confluence: channel angle + organic noise curves */
      /* Channels gently breathe/undulate for a living-river feel */
      const chAngle = channelBaseAngle(p.channel) +
                      0.085 * Math.sin(time * 0.21 + p.seed * 2.2 + p.channel * 1.28) +
                      0.040 * Math.cos(time * 0.13 + p.seed * 3.1);

      /* Soft centering: keeps strands in their channel lane */
      const idealY = channelIdealY(p.channel, p.x);
      const offY   = idealY - p.y;
      const chCorr = Math.sign(offY) * Math.min(0.11, Math.abs(offY) / h * 0.58);

      /* Confluence turbulence: extra chaos in the mixing bowl */
      const dConfl    = Math.hypot(p.x - cx, p.y - cy) / w;
      const turbFrac  = dConfl < 0.09 ? (1 - dConfl / 0.09) * 0.38 : 0;

      const postAx = Math.cos(na) * (0.19 + turbFrac) + Math.cos(chAngle) * (0.81 - turbFrac);
      const postAy = Math.sin(na) * (0.19 + turbFrac) + Math.sin(chAngle) * (0.81 - turbFrac) + chCorr;
      const postFr = 0.971;

      const ax = preAx * (1 - mix) + postAx * mix;
      const ay = preAy * (1 - mix) + postAy * mix;
      const fr = preFr  * (1 - mix) + postFr  * mix;

      p.vx = p.vx * fr + ax * 0.70 * breath;
      p.vy = p.vy * fr + ay * 0.50 * breath;

      const spd = Math.hypot(p.vx, p.vy);
      if (spd > MAX_SPEED) { const sc = MAX_SPEED / spd; p.vx *= sc; p.vy *= sc; }

      p.x += p.vx;
      p.y += p.vy;
      p.age++;

      /* ── Color ── stream hue → fog-white as particle moves rightward */
      const fT = p.x < fogStart ? 0 : Math.min(1, (p.x - fogStart) / (fogEnd - fogStart));
      const cr  = s.color[0] * (1 - fT) + FOG[0] * fT;
      const cg  = s.color[1] * (1 - fT) + FOG[1] * fT;
      const cb  = s.color[2] * (1 - fT) + FOG[2] * fT;

      /* ── Alpha compositing ── */
      const ar        = p.age / p.life;
      const lifeAlpha = ar < 0.25 ? ar * 4 : ar > 0.75 ? Math.max(0, 1 - (ar - 0.75) * 4) : 1;
      const edgeFade  = p.x > w * 0.87 ? Math.max(0, 1 - (p.x - w * 0.87) / (w * 0.13)) : 1;

      /* Gaussian cross-section: bright at stream center, fades at edges
         → organic edges instead of a rectangular slab of particles        */
      const centerY       = p.x < cx
        ? h * s.yF
        : cy + (p.x - cx) * Math.tan(channelBaseAngle(p.channel));
      const crossDist     = Math.abs(p.y - centerY) / (h * s.sF * 2.8);
      const gaussFade     = Math.exp(-crossDist * crossDist * 2.2);

      let alpha = s.alpha * lifeAlpha * edgeFade * p.alphaMod * gaussFade;

      /* Shimmer / glint: sunlight catching the surface */
      if (p.shimmer) {
        const pulse = Math.sin(time * 8.6 + p.seed * 5.4);
        if (pulse > 0.82) alpha = Math.min(1.0, alpha * 3.8);
      }

      const drawAlpha = Math.min(1, alpha * 0.54);
      if (drawAlpha < 0.005) {
        if (p.x > w + 4 || p.x < -10 || p.y < -20 || p.y > h + 20 || p.age > p.life) {
          Object.assign(p, spawn(s, false));
        }
        continue;
      }

      /* ── Particle size ── */
      /* Tapers post-confluence: fat stream → thin braided threads */
      const channelTaper = 1 - mix * 0.48;
      const radius = (1.25 + 1.1 * (mix * 0.5 + 0.5)) * channelTaper * breath * p.sizeMod;

      const rStr = cr | 0, gStr = cg | 0, bStr = cb | 0;
      const aStr = drawAlpha.toFixed(3);

      /* ── Rendering ── line-segment filament where velocity is meaningful;
         arc otherwise.  Filaments create the flowing-thread water look.   */
      const fdx = p.x - p.px;
      const fdy = p.y - p.py;
      const fLen = Math.hypot(fdx, fdy);

      if (fLen > 0.8 && fLen < 9) {
        ctx.strokeStyle = `rgba(${rStr},${gStr},${bStr},${aStr})`;
        ctx.lineWidth   = radius * 1.85;
        ctx.beginPath();
        ctx.moveTo(p.px, p.py);
        ctx.lineTo(p.x,  p.y);
        ctx.stroke();
      } else {
        ctx.fillStyle = `rgba(${rStr},${gStr},${bStr},${aStr})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, radius, 0, TWO_PI);
        ctx.fill();
      }

      /* Respawn when particle exits canvas or expires */
      if (p.x > w + 4 || p.x < -10 || p.y < -20 || p.y > h + 20 || p.age > p.life) {
        Object.assign(p, spawn(s, false));
      }
    }

    ctx.globalCompositeOperation = 'source-over';
    raf = requestAnimationFrame(frame);
  }

  if (reduceMotion) {
    setup();
    staticFallback();
    return;
  }

  setup();
  raf = requestAnimationFrame(frame);

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(setup, 200);
  });
})();
