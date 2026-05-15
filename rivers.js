/* ─────────────────────────────────────────────────────────────
   Tulq — Two Rivers Canvas
   Canvas 2D flow-field with two particle populations converging
   at ~60% width. After convergence both streams interpolate toward
   fog — a tone neither current contained alone.
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
  const TRAIL = 0.026;

  let w = canvas.parentElement.clientWidth;
  let h = canvas.parentElement.clientHeight;
  let dpr = Math.min(window.devicePixelRatio || 1, 1.5);
  let t0 = performance.now();
  let raf = 0;
  let particles = [];

  function setup() {
    w = canvas.parentElement.clientWidth;
    h = canvas.parentElement.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    ctx.fillStyle = `rgb(${BG.join(',')})`;
    ctx.fillRect(0, 0, w, h);

    const isMobile = w < 760;
    const count = isMobile ? 900 : 1800;

    particles = [];
    const half = Math.floor(count / 2);
    for (let i = 0; i < half; i++) particles.push(spawn(TOLT, true));
    for (let i = 0; i < count - half; i++) particles.push(spawn(SNOQ, true));
  }

  function spawn(stream, randomX) {
    return {
      x: randomX ? Math.random() * w * 0.5 : Math.random() * w * 0.08,
      y: h * stream.yF + (Math.random() - 0.5) * h * stream.sF,
      vx: stream.vBase * (0.6 + Math.random() * 0.4),
      vy: (Math.random() - 0.5) * 0.2,
      age: Math.random() * 200,
      life: 320 + Math.random() * 420,
      s: stream
    };
  }

  function angleAt(x, y, time) {
    const n =
      Math.sin(x * 0.0028 + time * 0.18) * Math.cos(y * 0.0042 + time * 0.13) +
      Math.sin(x * 0.0061 + y * 0.0051 + time * 0.21) * 0.6;
    return n * Math.PI * 0.55;
  }

  function staticFallback() {
    ctx.fillStyle = `rgb(${BG.join(',')})`;
    ctx.fillRect(0, 0, w, h);
    const grad = ctx.createLinearGradient(0, 0, w, 0);
    grad.addColorStop(0, 'rgba(168,200,196,0)');
    grad.addColorStop(0.4, 'rgba(168,200,196,0.45)');
    grad.addColorStop(0.62, 'rgba(232,228,216,0.55)');
    grad.addColorStop(0.85, 'rgba(107,138,150,0.4)');
    grad.addColorStop(1, 'rgba(107,138,150,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, h * 0.42, w, h * 0.16);

    const cx = w * CX, cy = h * CY;
    ctx.fillStyle = 'rgba(232,228,216,0.7)';
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  function frame() {
    if (document.hidden) { raf = requestAnimationFrame(frame); return; }

    const time = (performance.now() - t0) / 1000;
    const breath = 1 + 0.18 * Math.sin(time * Math.PI * 2 / 5);

    ctx.fillStyle = `rgba(${BG[0]},${BG[1]},${BG[2]},${TRAIL})`;
    ctx.fillRect(0, 0, w, h);

    const cx = w * CX, cy = h * CY;
    const fogStart = cx - w * 0.06;
    const fogEnd = w * 0.94;

    ctx.filter = 'blur(0.9px)';
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i], s = p.s;

      const distNorm = Math.abs(p.x - cx) / w + Math.abs(p.y - cy) / h;

      const na = angleAt(p.x, p.y, time);
      const pa = Math.atan2(cy - p.y, cx - p.x);
      const post = p.x > cx;
      let ax, ay, fr;
      if (post) {
        // Smooth merged river — mostly rightward, gentle vertical centering, minimal noise
        const noiseAx = Math.cos(na) * 0.14;
        const noiseAy = Math.sin(na) * 0.14;
        const centerY = (cy - p.y) / h * 0.55; // pulls toward mid-height
        ax = noiseAx + 0.86;
        ay = noiseAy + centerY;
        fr = 0.965;
      } else {
        // Pre-confluence: noise field + pull toward confluence point
        const pull = Math.min(0.8, 0.18 + distNorm * s.pull);
        const ep = pull;
        ax = Math.cos(na) * (1 - ep) + Math.cos(pa) * ep;
        ay = Math.sin(na) * (1 - ep) + Math.sin(pa) * ep;
        fr = 0.92;
      }
      p.vx = p.vx * fr + ax * 0.7 * breath;
      p.vy = p.vy * fr + ay * 0.5 * breath;

      p.x += p.vx; p.y += p.vy; p.age++;

      const fT = p.x < fogStart ? 0 : Math.min(1, (p.x - fogStart) / (fogEnd - fogStart));
      const r = s.color[0] * (1 - fT) + FOG[0] * fT;
      const g = s.color[1] * (1 - fT) + FOG[1] * fT;
      const b = s.color[2] * (1 - fT) + FOG[2] * fT;

      const ar = p.age / p.life;
      const aa = ar < 0.25 ? ar * 4 : ar > 0.75 ? Math.max(0, 1 - (ar - 0.75) * 4) : 1;

      ctx.fillStyle = `rgba(${r | 0},${g | 0},${b | 0},${(s.alpha * aa).toFixed(3)})`;
      const radius = post ? 1.8 : 1.3;
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
      ctx.fill();

      if (p.x > w + 4 || p.x < -10 || p.y < -20 || p.y > h + 20 || p.age > p.life) {
        Object.assign(p, spawn(s, false));
      }
    }
    ctx.filter = 'none';

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
    resizeTimer = setTimeout(() => { setup(); }, 200);
  });
})();
