const P = 'D:/GoAI/App/resources/app/js/';
const Engine = require(P + 'go-engine.js');
const Study = require(P + 'study-games.js');
const ALPHA = 'ABCDEFGHIJKLMNOPQRS';

function toText(m) {
  if (m < 0) return '弃手';
  const r = Math.floor(m / 19), c = m % 19;
  return ALPHA[c] + (19 - r);
}

let total = 0, totalBad = 0;
Study.GAMES.forEach(function (gm) {
  const g = new Engine.GoGame(19);
  let bad = [];
  gm.moves.forEach(function (m, k) {
    total++;
    if (m < 0) { g.pass(); return; }
    const r = g.play(m);
    if (!r.ok) bad.push({ n: k + 1, at: toText(m), reason: r.reason || 'illegal' });
  });
  totalBad += bad.length;
  const stones = g.board ? g.board.filter(function (v) { return v !== 0; }).length : 0;
  const last = gm.moves.length ? gm.moves[gm.moves.length - 1] : -1;
  console.log(
    [gm.id, gm.title, '手数=' + gm.moves.length, '非法=' + bad.length,
     '终局子数=' + stones, '末手=' + toText(last)].join('  ')
  );
  if (bad.length) console.log('   ', JSON.stringify(bad.slice(0, 10)));
});
console.log('---');
console.log('总手数=' + total, '总非法=' + totalBad, '局数=' + Study.GAMES.length);

const t0 = Date.now();
const book = Study.buildBook();
const cons = (book.black && book.black.length) || 0;
const prof = Study.buildProfile ? Study.buildProfile() : null;
console.log('buildBook 用时=' + (Date.now() - t0) + 'ms');
console.log('book keys=' + Object.keys(book).join(','));
if (prof) console.log('profile keys=' + Object.keys(prof).join(','));
