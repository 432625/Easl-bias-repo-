(() => {
  const cnv = document.getElementById('bg-bubbles');
  const ctx = cnv.getContext('2d', { alpha: true });


  const COLORS = ['#9bb3c8', '#a3b8c9', '#b2c3d4', '#94a8ba', '#8fa5bb'];


  const COUNT_SMALL  = 18;
  const COUNT_MEDIUM = 10;
  const COUNT_LARGE  = 6;
  const SPEED_BASE   = 0.02;
  const DRIFT        = 0.12;

  let W = 0, H = 0, bubbles = [], raf = null;

  class Bubble {
    constructor({ r, speedY }) {
      this.r = r;
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.speedY = speedY;
      this.phase = Math.random() * Math.PI * 2;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.alpha = 0.18 + Math.random() * 0.22; // softness
    }
    step(dt) {
      this.y -= this.speedY * dt;
      this.phase += DRIFT * dt * 0.001;
      this.x += Math.sin(this.phase) * 0.12 * this.r;
      if (this.y < -this.r - 2) {
        this.y = H + this.r;
        this.x = Math.random() * W;
      }
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color + Math.floor(this.alpha * 255).toString(16).padStart(2, '0');
      // above creates hex with alpha; for better support use rgba:
      ctx.fillStyle = hexToRgba(this.color, this.alpha);
      ctx.fill();
    }
  }

  function hexToRgba(hex, a) {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    const r = parseInt(m[1], 16), g = parseInt(m[2], 16), b = parseInt(m[3], 16);
    return `rgba(${r}, ${g}, ${b}, ${a})`;
  }

  function makeBubbles() {
    bubbles = [];

    for (let i = 0; i < COUNT_SMALL; i++)   bubbles.push(new Bubble({ r: 10 + Math.random() * 10, speedY: (0.015 + Math.random() * 0.03) * SPEED_BASE * H }));

    for (let i = 0; i < COUNT_MEDIUM; i++)  bubbles.push(new Bubble({ r: 20 + Math.random() * 16, speedY: (0.02  + Math.random() * 0.04) * SPEED_BASE * H }));

    for (let i = 0; i < COUNT_LARGE; i++)   bubbles.push(new Bubble({ r: 34 + Math.random() * 18, speedY: (0.025 + Math.random() * 0.045) * SPEED_BASE * H }));
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2); // cap DPR for perf
    W = cnv.clientWidth;
    H = cnv.clientHeight;
    cnv.width  = Math.floor(W * dpr);
    cnv.height = Math.floor(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    makeBubbles();
  }

  let last = performance.now();
  function loop(now) {
    const dt = now - last; last = now;
    ctx.clearRect(0, 0, W, H);
    for (const b of bubbles) { b.step(dt); b.draw(); }
    raf = requestAnimationFrame(loop);
  }


  resize();
  window.addEventListener('resize', resize, { passive: true });
  raf = requestAnimationFrame(loop);
})();
