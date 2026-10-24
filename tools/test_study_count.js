const P = 'D:/GoAI/App/resources/app/js/';
const { GoMemory } = require(P + 'memory-store.js');
const Study = require(P + 'study-games.js');

function fakeEntries(n) {
  const out = [];
  for (let k = 0; k < n; k++) out.push({ i: k, color: k % 2 ? 2 : 1, no: k + 1, patKey: k % 100, h: 'h' + k });
  return out;
}

const mem = new GoMemory();
mem._scheduleFlush = function () {};      // 不落盘

const lens = Study.GAMES.map(g => g.moves.length);
function onePass(round) {
  Study.GAMES.forEach((g, i) => {
    mem.studyGame(fakeEntries(lens[i]), g.winner, { pass: round });
  });
  console.log('第 ' + round + ' 遍 -> 遍数=' + mem.meta.studyPasses + ' 手数=' + mem.meta.studyMoves);
}

onePass(1);
onePass(2);
onePass(3);
console.log('预期: 1/810  2/1620  3/2430');
