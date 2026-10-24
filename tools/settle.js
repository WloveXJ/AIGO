const Engine = require('D:/GoAI/App/resources/app/js/go-engine.js');
const Study = require('D:/GoAI/App/resources/app/js/study-games.js');
const raw = require('./moves_raw.json');
const N = 19;
const g = new Engine.GoGame(N);
const out = [];
const changes = [];
raw.forEach((m, k) => {
  const no = k + 1;
  if (m >= 0 && g.board[m] === 0) {
    const r = g.play(m);
    if (r.ok) { out.push(m); return; }
  }
  // 就近找合法点
  const j0 = (m / N) | 0, i0 = m % N;
  const cands = [];
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const t = j * N + i;
    if (g.board[t] !== 0) continue;
    cands.push([Math.max(Math.abs(j - j0), Math.abs(i - i0)), t]);
  }
  cands.sort((a, b) => a[0] - b[0]);
  let done = false;
  for (const [d, t] of cands) {
    if (d > 5) break;
    const c = g.clone();
    if (c.play(t).ok) {
      g.play(t);
      out.push(t);
      changes.push({ no, from: Study.toText(m), to: Study.toText(t), d });
      done = true;
      break;
    }
  }
  if (!done) { g.pass(); out.push(-1); changes.push({ no, from: Study.toText(m), to: 'PASS' }); }
});
console.log('调整', changes.length, '手');
console.log(changes);
require('fs').writeFileSync('./moves_final.json', JSON.stringify(out));
