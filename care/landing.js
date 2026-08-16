/* ══════════════════════════════════════════════════════════════════════
   landing.js — behaviour for the homepage-styled landing pages.

   This is the homepage's inline script minus the two things that are
   specific to index.html: the rivers Canvas 2D background, and the
   "Launching 2026" call-button ring. Everything else is shared, so it
   lives here rather than being pasted into each generated page.

   Served with Cache-Control: immutable, so the reference is hashed by
   tools/stamp-assets.py. Never hand-write a ?v= on it.
   ══════════════════════════════════════════════════════════════════════ */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Nav mode: dark over the hero, light once past it ──── */
  const nav  = document.getElementById('nav');
  const hero = document.getElementById('top');
  if (nav && hero) {
    const updateNav = () => {
      const heroBottom = hero.getBoundingClientRect().bottom;
      nav.setAttribute('data-mode', heroBottom < 80 ? 'light' : 'dark');
      nav.classList.toggle('scrolled', window.scrollY > 8);
    };
    updateNav();
    window.addEventListener('scroll', updateNav, { passive: true });
    window.addEventListener('resize', updateNav);
  }

  /* ── Scroll progress hairline ──────────────────────────── */
  const prog = document.getElementById('scroll-progress');
  if (prog) {
    const updateProgress = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const p = max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0;
      prog.style.setProperty('--p', p.toFixed(2) + '%');
    };
    updateProgress();
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
  }

  /* ── Staggered reveal on scroll (.rise → .is-in) ───────── */
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-reveal');
    const groups = new Map();
    document.querySelectorAll('.rise').forEach(el => {
      const key = el.parentElement;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(el);
    });
    groups.forEach(list => list.forEach((el, i) => {
      el.style.setProperty('--rd', (i * 90) + 'ms');
    }));

    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    document.querySelectorAll('.rise').forEach(el => io.observe(el));
  }

  /* ── Count-up on any .numbers block in view ────────────── */
  if (!reduce && 'IntersectionObserver' in window) {
    const fmt = (n, decimals) =>
      decimals > 0 ? n.toFixed(decimals) : Math.round(n).toString();
    const animate = (el) => {
      const target = parseFloat(el.dataset.count);
      if (isNaN(target)) return;
      const prefix = el.dataset.prefix || '';
      const suffix = el.dataset.suffix || '';
      const sup    = el.dataset.sup;
      const decimals = (el.dataset.count.split('.')[1] || '').length;
      const duration = 1400;
      const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / duration);
        const e = 1 - Math.pow(1 - t, 3);
        const supHTML = sup ? `<sup>${sup}</sup>` : '';
        el.innerHTML = `${prefix}${fmt(target * e, decimals)}${suffix}${supHTML}`;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    document.querySelectorAll('.numbers').forEach(block => {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            block.querySelectorAll('.number-value[data-count]').forEach(animate);
            obs.disconnect();
          }
        });
      }, { threshold: 0.3 });
      obs.observe(block);
    });
  }

  /* ── Subtle magnetic pull on primary buttons ───────────── */
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('[data-magnetic]').forEach(btn => {
      const strength = 10;
      btn.style.transition = btn.style.transition || 'transform .12s var(--ease-out-soft)';
      btn.addEventListener('pointermove', (ev) => {
        const r = btn.getBoundingClientRect();
        const nx = Math.max(-1, Math.min(1, (ev.clientX - (r.left + r.width / 2)) / (r.width / 2)));
        const ny = Math.max(-1, Math.min(1, (ev.clientY - (r.top + r.height / 2)) / (r.height / 2)));
        btn.style.transform =
          `translate(${(nx * strength).toFixed(2)}px, ${(ny * strength * 0.7).toFixed(2)}px)`;
      });
      btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
    });
  }

  /* ── Cursor-tracked glow in the hero ───────────────────── */
  const glow = document.getElementById('hero-glow');
  if (glow && hero && !reduce && window.matchMedia('(hover: hover)').matches) {
    hero.addEventListener('pointermove', (ev) => {
      const r = hero.getBoundingClientRect();
      glow.style.setProperty('--gx', (ev.clientX - r.left) + 'px');
      glow.style.setProperty('--gy', (ev.clientY - r.top)  + 'px');
      glow.style.setProperty('--gO', '1');
    });
    hero.addEventListener('pointerleave', () => glow.style.setProperty('--gO', '0'));
  }

  /* ── Smooth-scroll for in-page anchors ─────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (ev) => {
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      ev.preventDefault();
      const y = target.getBoundingClientRect().top + window.scrollY - 12;
      window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
      history.replaceState(null, '', id);
    });
  });
})();
