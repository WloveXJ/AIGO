const P = 'D:/GoAI/App/resources/app/js/';
const Engine = require(P + 'go-engine.js');
const Study = require(P + 'study-games.js');

const t0 = Date.now();
const bBook = Study.buildBook(Engine, Study.GAMES, 1);
const t1 = Date.now();
const wBook = Study.buildBook(Engine, Study.GAMES, 2);
const t2 = Date.now();
const bProf = Study.buildProfile(Study.GAMES, 1);
const wProf = Study.buildProfile(Study.GAMES, 2);

const cnt = (bk) => Object.keys(bk).reduce((a, k) => a + Object.keys(bk[k]).length, 0);
console.log('黑方手册 局面=' + Object.keys(bBook).length + ' 条目=' + cnt(bBook) + ' 用时=' + (t1 - t0) + 'ms');
console.log('白方手册 局面=' + Object.keys(wBook).length + ' 条目=' + cnt(wBook) + ' 用时=' + (t2 - t1) + 'ms');
console.log('吴棋 手数=' + bProf.moves + ' 均手距=' + bProf.avgDist.toFixed(2) + ' 角=' + bProf.openerCorner.toFixed(2) + ' 边=' + bProf.openerSide.toFixed(2));
console.log('邓棋 手数=' + wProf.moves + ' 均手距=' + wProf.avgDist.toFixed(2) + ' 角=' + wProf.openerCorner.toFixed(2) + ' 边=' + wProf.openerSide.toFixed(2));

// 研习签名（与 trainer.worker.js 一致）
const sig = Study.GAMES.length + ':' + Study.GAMES.reduce((a, g) => a + g.moves.length, 0);
console.log('研习签名 studySig = ' + sig);

// 抽样：第 5 局前 12 手
console.log('对局五前 12 手: ' + Study.GAMES[4].moves.slice(0, 12).map(Study.toText).join(' '));
console.log('对局五末 6 手: ' + Study.GAMES[4].moves.slice(-6).map(Study.toText).join(' '));
