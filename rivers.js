/* ─────────────────────────────────────────────────────────────
   Tulq — Two Rivers Canvas
   Canvas 2D flow-field with two particle populations converging
   at ~60% width, then branching into a braided delta of thin
   tributary channels that fan across the full canvas height.
   Motion paced to a 5-second resting-breath cycle.
   ───────────────────────────────────────────────────────────── */

(() => {
  const canvas = document.getElementById('rivers');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const TOLT = { yF: 0.30, sF: 0.13, color: [168, 200, 196], pull: 0.35, vBase: 1.1, alpha: 0.46 };
  const SNOQ = { yF: 0.72, sF: 0.16, color: [107, 138, 150], pull: 0.45, vBase: 0.9, alpha: 0.36 };
  const FOG  = [232, 228, 216];
  const BG   = [28, 38, 40];
  const CX = 0.62, CY = 0.50;
  const TRAIL = 0.045;
  const BLEND_HALF = 0.12;
  const MAX_SPEED  = 5;
  const TWO_PI     = Math.PI * 2;

  // Braided delta parameters
  const NUM_CHANNELS    = 11;    // number of distinct tributary channels
  const CHANNEL_SPREAD  = 0.80;  // channels fan across this fraction of canvas height

  let w, h, dpr, cx, cy;
  let t0 = performance.now();
  let raf = 0;
  let particles = [];

  function smoothstep(edge0, edge1, x) {
    const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  // Return the target y for a given channel index at a moment in time
  function channelTargetY(channel, time, seed) {
    const frac = (channel / (NUM_CHANNELS - 1)) - 0.5; // -0.5 … +0.5
    const baseY = cy + frac * h * CHANNEL_SPREAD;
    // Each channel undulates gently and independently
    const undulation = h * 0.022 * Math.sin(time * 0.28 + seed * 2.1 + channel * 1.37);
    return baseY + undulation;
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
    const count = isMobile ? 900 : 1800;

    particles = [];
    const half = Math.floor(count / 2);
    for (let i = 0; i < half; i++)         particles.push(spawn(TOLT, true));
    for (let i = 0; i < count - half; i++) particles.push(spawn(SNOQ, true));
  }

  function spawn(stream, randomX) {
    // Each particle is assigned a permanent channel for post-confluence routing
    const channel = Math.floor(Math.random() * NUM_CHANNELS);

    let x, y;
    if (randomX) {
      // Spread initial particles across the FULL canvas so it looks beautiful from frame 0
      x = Math.random() * w;
      if (x < cx) {
        // Pre-confluence zone: near the stream band
        y = h * stream.yF + (Math.random() - 0.5) * h * stream.sF;
      } else {
        // Post-confluence zone: place particle near its channel's resting position
        const frac = (channel / (NUM_CHANNELS - 1)) - 0.5;
        const baseY = cy + frac * h * CHANNEL_SPREAD;
        y = baseY + (Math.random() - 0.5) * h * 0.03;
      }
    } else {
      x = Math.random() * w * 0.08;
      y = h * stream.yF + (Math.random() - 0.5) * h * stream.sF;
    }

    return {
      x,
      y,
      vx:       stream.vBase * (0.6 + Math.random() * 0.4),
      vy:       (Math.random() - 0.5) * 0.2,
      age:      Math.random() * 200,
      life:     320 + Math.random() * 420,
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
    gt.addColorStop(0.62, 'rgba(232,228,216,0.45)');
    gt.addColorStop(1,    'rgba(232,228,216,0)');
    ctx.fillStyle = gt;
    ctx.fillRect(0, h * 0.24, w, h * 0.12);

    const gs = ctx.createLinearGradient(0, 0, w, 0);
    gs.addColorStop(0,    'rgba(107,138,150,0)');
    gs.addColorStop(0.35, 'rgba(107,138,150,0.28)');
    gs.addColorStop(0.62, 'rgba(232,228,216,0.45)');
    gs.addColorStop(1,    'rgba(232,228,216,0)');
    ctx.fillStyle = gs;
    ctx.fillRect(0, h * 0.66, w, h * 0.12);

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

      // Pre-confluence: flow field + pull toward confluence
      const pull  = Math.min(0.8, 0.18 + distNorm * s.pull);
      const preAx = Math.cos(na) * (1 - pull) + Math.cos(pa) * pull;
      const preAy = Math.sin(na) * (1 - pull) + Math.sin(pa) * pull;
      const preFr = 0.92;

      // Post-confluence: branch into assigned tributary channel
      // Strong pull toward the channel's y, gentle noise keeps strands organic
      const targetY  = channelTargetY(p.channel, time, p.seed);
      const dy       = targetY - p.y;
      // Proportional pull — enough to stay in channel without oscillating
      const chPull   = Math.sign(dy) * Math.min(0.6, Math.abs(dy) / h * 1.8);
      const postAx   = Math.cos(na) * 0.06 + 0.94; // strongly rightward
      const postAy   = Math.sin(na) * 0.06 + chPull;
      const postFr   = 0.97;

      const ax = preAx * (1 - mix) + postAx * mix;
      const ay = preAy * (1 - mix) + postAy * mix;
      const fr = preFr * (1 - mix) + postFr * mix;

      p.vx = p.vx * fr + ax * 0.7 * breath;
      p.vy = p.vy * fr + ay * 0.5 * breath;

      const spd = Math.hypot(p.vx, p.vy);
      if (spd > MAX_SPEED) { const sc = MAX_SPEED / spd; p.vx *= sc; p.vy *= sc; }

      p.x += p.vx; p.y += p.vy; p.age++;

      // Color: stream hue → FOG as particle moves past fogStart
      const fT = p.x < fogStart ? 0 : Math.min(1, (p.x - fogStart) / (fogEnd - fogStart));
      const cr  = s.color[0] * (1 - fT) + FOG[0] * fT;
      const cg  = s.color[1] * (1 - fT) + FOG[1] * fT;
      const cb  = s.color[2] * (1 - fT) + FOG[2] * fT;

      const ar        = p.age / p.life;
      const lifeAlpha = ar < 0.25 ? ar * 4 : ar > 0.75 ? Math.max(0, 1 - (ar - 0.75) * 4) : 1;
      const edgeFade  = p.x > w * 0.85 ? Math.max(0, 1 - (p.x - w * 0.85) / (w * 0.15)) : 1;

      const alpha = s.alpha * lifeAlpha * edgeFade * p.alphaMod;

      // Post-confluence: shrink particles so channels look like thin thread-like rivers
      // Pre-confluence: normal breathing size
      const baseSz      = 1.2 + 1.2 * (mix * 0.5 + 0.5);
      const channelTaper = mix > 0 ? 1 - mix * 0.55 : 1; // shrink as channels separate
      const radius      = baseSz * channelTaper * breath * p.sizeMod;

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
