const P = 'D:/GoAI/App/resources/app/js/';
const Study = require(P + 'study-games.js');
const NAME = ['一', '二', '三', '四', '五'];
[1, 2].forEach(function (c) {
  const p = Study.buildProfile(Study.GAMES, c);
  const top = (arr, exclude) => {
    let best = -1, bv = -1;
    arr.forEach((v, i) => { if (i === exclude) return; if (v > bv) { bv = v; best = i; } });
    return [best, bv];
  };
  const L = top(p.line, 0), R = top(p.region, -1);
  console.log((c === 1 ? '吴棋(黑)' : '邓棋(白)') +
    ' 手数=' + p.moves +
    ' 常用线=' + L[0] + '(' + L[1].toFixed(2) + ')' +
    ' 主区域=' + R[0] + '(' + R[1].toFixed(2) + ')' +
    ' 角=' + (p.openerCorner * 100).toFixed(0) + '%' +
    ' 边=' + (p.openerSide * 100).toFixed(0) + '%' +
    ' 均手距=' + p.avgDist.toFixed(1));
  console.log('   line=', p.line.map(v => v.toFixed(2)).join(' '));
  console.log('   region=', p.region.map(v => v.toFixed(2)).join(' '));
});
console.log('各局手数: ' + Study.GAMES.map(g => g.title + '=' + g.moves.length).join('  '));
