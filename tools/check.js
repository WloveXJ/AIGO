const path = 'D:/GoAI/App/resources/app/js/';
const Engine = require(path + 'go-engine.js');
const Study = require(path + 'study-games.js');
const moves = require('./moves.json');
const g = new Engine.GoGame(19);
let bad = [];
moves.forEach((m, k) => {
  const n = k + 1;
  if (m < 0) { return; }
  const color = n % 2 === 1 ? 'B' : 'W';
  const before = g.board ? g.board.slice() : null;
  const r = g.play(m);
  if (!r.ok) bad.push({ n, m, color, at: Study.toText(m), reason: r.reason || 'illegal' });
});
console.log('非法手数:', bad.length);
console.log(bad.slice(0, 20));
