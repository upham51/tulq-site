/* ─────────────────────────────────────────────────────────────
   Tulq — Two Rivers Canvas
   Two streams enter from the very top-left and bottom-left of
   the canvas, converge at ~58% width, then fan into a braided
   delta of organic tributary channels that spread across the
   full canvas height.
   ───────────────────────────────────────────────────────────── */

(() => {
  const canvas = document.getElementById('rivers');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Streams hug the very top and bottom edges
  const TOLT = { yF: 0.04, sF: 0.09, color: [168, 200, 196], pull: 0.52, vBase: 1.1, alpha: 0.50 };
  const SNOQ = { yF: 0.96, sF: 0.09, color: [107, 138, 150], pull: 0.57, vBase: 0.9, alpha: 0.42 };
  const FOG  = [232, 228, 216];
  const BG   = [28, 38, 40];
  const CX = 0.58, CY = 0.50;
  const TRAIL      = 0.045;
  const BLEND_HALF = 0.09;
  const MAX_SPEED  = 5;
  const TWO_PI     = Math.PI * 2;

  // Delta fan: 11 channels spread to fill the full canvas height at the right edge
  const NUM_CHANNELS    = 11;
  // Half-angle chosen so extreme channels reach y≈0 and y≈h at x=w
  // Calibrated to w/h ≈ 1.6 widescreen; generous enough for any aspect ratio
  const MAX_DELTA_ANGLE = 1.20; // radians (~68°) — full fan half-width

  let w, h, dpr, cx, cy;
  let t0 = performance.now();
  let raf = 0;
  let particles = [];

  function smoothstep(edge0, edge1, x) {
    const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  // Each channel fans at a fixed base angle from the confluence point
  function channelBaseAngle(channel) {
    const frac = (channel / (NUM_CHANNELS - 1)) - 0.5; // -0.5 … +0.5
    return frac * MAX_DELTA_ANGLE;
  }

  // Ideal y for a particle in a given channel at a given x (linear projection)
  function channelIdealY(channel, x) {
    return cy + (x - cx) * Math.tan(channelBaseAngle(channel));
  }

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
    const count = isMobile ? 1000 : 2000;

    particles = [];
    const half = Math.floor(count / 2);
    for (let i = 0; i < half; i++)         particles.push(spawn(TOLT, true));
    for (let i = 0; i < count - half; i++) particles.push(spawn(SNOQ, true));
  }

  function spawn(stream, randomX) {
    const channel = Math.floor(Math.random() * NUM_CHANNELS);
    const angle   = channelBaseAngle(channel);

    let x, y;
    if (randomX) {
      // Scatter initial particles across the FULL canvas so the effect is immediately full
      x = Math.random() * w;
      if (x < cx) {
        // Pre-confluence zone: near the stream's starting band
        y = h * stream.yF + (Math.random() - 0.5) * h * stream.sF;
      } else {
        // Post-confluence zone: along this channel's angular trajectory from the confluence
        y = cy + (x - cx) * Math.tan(angle) + (Math.random() - 0.5) * h * 0.045;
        y = Math.max(2, Math.min(h - 2, y));
      }
    } else {
      // Respawn on left edge in stream's band
      x = Math.random() * w * 0.07;
      y = h * stream.yF + (Math.random() - 0.5) * h * stream.sF;
    }

    return {
      x,
      y,
      vx:       stream.vBase * (0.6 + Math.random() * 0.4),
      vy:       (Math.random() - 0.5) * 0.2,
      age:      Math.random() * 200,
      life:     300 + Math.random() * 400,
      seed:     Math.random() * TWO_PI,
      alphaMod: 0.7 + Math.random() * 0.6,
      sizeMod:  0.75 + Math.random() * 0.5,
      s:        stream,
      channel,
    };
  }

  function angleAt(x, y, time) {
    const n1 =
      Math.sin(x * 0.0028 + time * 0.18) * Math.cos(y * 0.0042 + time * 0.13) +
      Math.sin(x * 0.0061 + y * 0.0051 + time * 0.21) * 0.6;
    const n2 = Math.sin(x * 0.0014 + y * 0.0022 + time * 0.09) * 0.4;
    return (n1 + n2) * Math.PI * 0.35;
  }

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

  function frame() {
    if (document.hidden) { raf = requestAnimationFrame(frame); return; }

    const time   = (performance.now() - t0) / 1000;
    const breath = 1 + 0.18 * Math.sin(time * Math.PI * 2 / 5);

    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = `rgba(${BG[0]},${BG[1]},${BG[2]},${TRAIL})`;
    ctx.fillRect(0, 0, w, h);

    const fogStart = cx - w * 0.06;
    const fogEnd   = w;
    const blendLo  = cx - w * BLEND_HALF;
    const blendHi  = cx + w * BLEND_HALF;

    ctx.globalCompositeOperation = 'lighter';

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i], s = p.s;

      const na       = angleAt(p.x, p.y, time);
      const pa       = Math.atan2(cy - p.y, cx - p.x);
      const distNorm = Math.abs(p.x - cx) / w + Math.abs(p.y - cy) / h;

      const mix = smoothstep(blendLo, blendHi, p.x);

      // ── Pre-confluence: noise field + strong pull toward confluence ──
      const pull  = Math.min(0.88, 0.18 + distNorm * s.pull);
      const preAx = Math.cos(na) * (1 - pull) + Math.cos(pa) * pull;
      const preAy = Math.sin(na) * (1 - pull) + Math.sin(pa) * pull;
      const preFr = 0.92;

      // ── Post-confluence: channel-angle fan + organic noise curves ──
      // Base channel direction with gentle living undulation per channel
      const chAngle = channelBaseAngle(p.channel) +
                      0.09 * Math.sin(time * 0.22 + p.seed * 2.1 + p.channel * 1.23);

      // Soft centering correction keeps strands within their channel
      // without making them mechanically rigid
      const idealY = channelIdealY(p.channel, p.x);
      const dy     = idealY - p.y;
      const chCorr = Math.sign(dy) * Math.min(0.10, Math.abs(dy) / h * 0.55);

      // 22% noise → organic curves; 78% channel direction → distinct strands
      const postAx = Math.cos(na) * 0.22 + Math.cos(chAngle) * 0.78;
      const postAy = Math.sin(na) * 0.22 + Math.sin(chAngle) * 0.78 + chCorr;
      const postFr = 0.968;

      const ax = preAx * (1 - mix) + postAx * mix;
      const ay = preAy * (1 - mix) + postAy * mix;
      const fr = preFr * (1 - mix) + postFr * mix;

      p.vx = p.vx * fr + ax * 0.7 * breath;
      p.vy = p.vy * fr + ay * 0.5 * breath;

      const spd = Math.hypot(p.vx, p.vy);
      if (spd > MAX_SPEED) { const sc = MAX_SPEED / spd; p.vx *= sc; p.vy *= sc; }

      p.x += p.vx; p.y += p.vy; p.age++;

      // Color: stream hue → fog-white as particle moves rightward past fogStart
      const fT = p.x < fogStart ? 0 : Math.min(1, (p.x - fogStart) / (fogEnd - fogStart));
      const cr  = s.color[0] * (1 - fT) + FOG[0] * fT;
      const cg  = s.color[1] * (1 - fT) + FOG[1] * fT;
      const cb  = s.color[2] * (1 - fT) + FOG[2] * fT;

      const ar        = p.age / p.life;
      const lifeAlpha = ar < 0.25 ? ar * 4 : ar > 0.75 ? Math.max(0, 1 - (ar - 0.75) * 4) : 1;
      const edgeFade  = p.x > w * 0.85 ? Math.max(0, 1 - (p.x - w * 0.85) / (w * 0.15)) : 1;

      const alpha = s.alpha * lifeAlpha * edgeFade * p.alphaMod;

      // Particle size: full before confluence, tapers into thin channel threads after
      const channelTaper = 1 - mix * 0.50;
      const radius = (1.2 + 1.2 * (mix * 0.5 + 0.5)) * channelTaper * breath * p.sizeMod;

      const drawAlpha = Math.min(1, alpha * 0.5);

      ctx.fillStyle = `rgba(${cr | 0},${cg | 0},${cb | 0},${drawAlpha.toFixed(3)})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius, 0, TWO_PI);
      ctx.fill();

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
