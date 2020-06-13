function _defineProperty(obj, key, value) {if (key in obj) {Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true });} else {obj[key] = value;}return obj;}const width = innerWidth;
const height = innerHeight;
const canvases = Array.from(document.querySelectorAll('canvas'));
canvases.forEach(canvas => {
  canvas.width = width;
  canvas.height = height;
});
const ctxes = canvases.map(canvas => canvas.getContext('2d'));
ctxes.forEach(ctx => {
  ctx.translate(width / 2, height / 2);
  ctx.lineCap = 'round';
});
const {
  sin,
  cos,
  abs,
  PI } =
Math;
const [base, curve, cover] = ctxes;

class Choid {
  constructor() {_defineProperty(this, "setup",









    () => {
      delete this.lastP;
      base.clearRect(-width / 2, -height / 2, width, height);
      curve.clearRect(-width / 2, -height / 2, width, height);
      cover.clearRect(-width / 2, -height / 2, width, height);
      this._R = this.R;
      this._r = this.inner ? -this.r : this.r;
      this._arm = this.arm;

      this.c = this._R + this._r;
      this.delta = this.c && 4 / this.c;
      this.theta = 0;
      this.phi = 0;
      base.beginPath();
      base.arc(0, 0, this._R, 0, 2 * PI);
      base.strokeStyle = '#7f7f7f';
      base.stroke();
    });_defineProperty(this, "draw",
    () => {
      if (this.fade) {
        curve.fade();
      }
      const p = [
      this.c * cos(this.theta) + this._arm * cos(this.phi),
      this.c * sin(this.theta) + this._arm * sin(this.phi)];

      const color = this.color ?
      d3.interpolateRainbow(this.theta / PI / 2) :
      '#7f7f7f';

      cover.clearRect(-width / 2, -height / 2, width, height);
      cover.beginPath();
      cover.arc(this.c * cos(this.theta), this.c * sin(this.theta), abs(this._r), 0, 2 * PI);
      cover.strokeStyle = color;
      cover.stroke();
      if (this.lastP) {
        curve.beginPath();
        curve.moveTo(...this.lastP);
        curve.lineTo(...p);
        curve.strokeStyle = color;
        curve.stroke();

        cover.beginPath();
        cover.moveTo(this.c * cos(this.theta), this.c * sin(this.theta));
        cover.lineTo(...p);
        cover.strokeStyle = color;
        cover.stroke();
      }
      this.lastP = p;
      this.theta += this.delta;
      this.theta %= 2 * PI;
      this.phi += (1 + this._R / this._r) * this.delta;
      this.phi %= 2 * PI;
      requestAnimationFrame(this.draw);
    });this.R = 256;this.r = 180;this.arm = 149;this.inner = true;this.color = true;this.fade = false;this.setup();this.draw();}}


const c = new Choid();
const gui = new dat.GUI({ autoPlace: false });
document.getElementById('controller').appendChild(gui.domElement);
gui.add(c, 'R', 8, 256).onFinishChange(c.setup);
gui.add(c, 'r', 1, 256).onFinishChange(c.setup);
gui.add(c, 'arm', 0, 248).onFinishChange(c.setup);
gui.add(c, 'inner').onFinishChange(c.setup);
gui.add(c, 'color').onFinishChange(c.setup);
gui.add(c, 'fade');