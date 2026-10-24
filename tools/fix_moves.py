import json

ALPHA = 'ABCDEFGHIJKLMNOPQRS'
raw = json.load(open('raw_reads.json')) if False else None

exec(open('build_moves.py').read().split("def idx")[0].split("raw = {")[0])
# 重新载入原始读谱
src = open('build_moves.py', encoding='utf-8').read()
ns = {}
exec(src[src.index('raw = {'):src.index('}\n\ndef idx')+1], ns)
raw = ns['raw']

def idx(c):
    if c.endswith('x'): c = c[:-1]
    return (19 - int(c[1:])) * 19 + ALPHA.index(c[0])

cand = json.load(open('cand.json'))
sets = {}
for t, d in cand.items():
    sets[t] = {(int(k.split(',')[0]), int(k.split(',')[1])) for k, v in d['pts'].items() if v >= 2}
order = ['1-50','51-100','101-150','151-200','201-250']
new = {}
prev = set()
for t in order:
    new[t] = sets[t] - prev
    prev = sets[t]

def band(n):
    if n <= 50: return '1-50'
    if n <= 100: return '51-100'
    if n <= 150: return '101-150'
    if n <= 200: return '151-200'
    return '201-250'

SPURIOUS = {245, 246, 249}   # 谱外标注（应为提子记录），跳过落子
moves = [None]*251
board = [0]*361
fixed = []
for n in range(1, 251):
    if n in SPURIOUS:
        moves[n] = -1
        continue
    m = idx(raw[n])
    if board[m]:
        # 就近修正
        j, i = divmod(m, 19)
        best, bd = None, 99
        pool = new[band(n)] | {(x, y) for (x, y) in [(jj, ii) for jj in range(19) for ii in range(19)]}
        for (tj, ti) in sorted(new[band(n)]):
            t = tj*19+ti
            if board[t]: continue
            d = max(abs(tj-j), abs(ti-i))
            if d < bd: bd, best = d, t
        if best is None or bd > 3:
            moves[n] = -1
            fixed.append((n, raw[n], 'SKIP'))
            continue
        fixed.append((n, raw[n], '->%s%d (d=%d)' % (ALPHA[best % 19], 19 - best // 19, bd)))
        m = best
    moves[n] = m
    board[m] = 1 if n % 2 else 2

print('修正', len(fixed), '处:')
for f in fixed: print('  ', f)
print('重复:', len([m for m in moves[1:] if m >= 0]) - len(set(m for m in moves[1:] if m >= 0)))
json.dump(moves[1:], open('moves.json','w'))
print('moves 前20:', moves[1:21])
