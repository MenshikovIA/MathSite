const {
  PI,
  sin,
  cos,
  min,
  abs } =
Math;

const size = min(innerHeight, innerWidth);
const canvases = Array.from(document.querySelectorAll('canvas'));
const ctxes = [];
canvases.forEach(canvas => {
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctxes.push(ctx);
});
const [base, cover] = ctxes;

if (innerWidth < innerHeight) {
  base.setTransform(0, 1, 1, 0, 0, size / 2);
  cover.setTransform(0, 1, 1, 0, 0, size / 2);
} else {
  base.translate(size / 2, 0);
  cover.translate(size / 2, 0);
}

const d = 64;
class Hyperboloid {
  constructor() {
    this.theta = PI / 1.5;
    this.trail = false;
    this.r = PI;
    this.d = d;

    this.draw = this.draw.bind(this);
    this.draw();
  }
  clear() {
    ctxes.forEach(ctx => {
      ctx.save();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, size, size);
      ctx.restore();
    });
  }
  replay() {
    this.clear();
    this.r = PI;
    this.d = d;
  }
  draw() {
    if (!this.trail) {
      this.clear();
    }

    let i = 0;
    do {
      const color = `hsl(${i * 360},100%,50%)`;
      base.strokeStyle = color;
      cover.strokeStyle = color;
      base.beginPath();
      cover.beginPath();

      const alpha = i * 2 * PI;
      const ca = size / 2 * cos(alpha + this.r);
      const sa = size / 2 * sin(alpha + this.r);
      const cb = size / 2 * cos(alpha + this.r + this.theta);
      const sb = size / 2 * sin(alpha + this.r + this.theta);
      if (sa >= 0 && sb >= 0) {
        cover.moveTo(ca, 0);
        cover.lineTo(cb, size);
      } else if (sa <= 0 && sb <= 0) {
        base.moveTo(ca, 0);
        base.lineTo(cb, size);
      } else {
        let k = abs(sa / (sa - sb));
        let x = ca + k * (cb - ca);
        let y = k * size;
        if (sa > 0) {
          cover.moveTo(ca, 0);
          cover.lineTo(x, y);
          base.moveTo(x, y);
          base.lineTo(cb, size);
        } else {
          base.moveTo(ca, 0);
          base.lineTo(x, y);
          cover.moveTo(x, y);
          cover.lineTo(cb, size);
        }
      }
      base.stroke();
      cover.stroke();

      i += d / this.d;
    } while (i < 1);

    this.r -= PI / 768;
    this.r %= 2 * PI;
    if (this.d < d * 32) {
      this.d += 1;
    }
    requestAnimationFrame(this.draw);
  }}


onload = function () {
  const _ = new Hyperboloid();
  const gui = new dat.GUI();
  document.getElementById('controller').appendChild(gui.domElement);

  gui.add(_, 'theta', 0, PI).step(0.01);
  gui.add(_, 'trail');
  gui.add(_, 'replay');
};