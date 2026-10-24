import json

ALPHA = 'ABCDEFGHIJKLMNOPQRS'
raw = {}
# 第一谱（与自动识别逐点吻合，50/50）
g1 = "P16 D16 R4 D3 D5 P4 C3 C2 C4 E2 B9 D7 C8 Q6 P3 O3 Q3 O4 S6 E5 J6 J4 L6 L4 F17 C14 D18 H17 C17 E17 E18 F16 G16 G17 F18 G15 N17 R16 R14 Q17 P17 R18 Q14 P18 O18 H16 J9 O9 R7 L9".split()
for i, c in enumerate(g1, 1): raw[i] = c

g2 = "G7 K5 L11 O11 N10 O10 M8 N11 O8 M10 N13 P8 P7 N8 O7 N7 L8 P19 C12 D10 C10 D4 C6 O13 N14 Q5 R5 Q4 R3 K16 Q10 Q11 R11 R12 Q12 P11 R10 Q13 P13 P12 P14 L5 P2 O2 J5 J4 K18 D12 M9 N9".split()
for i, c in enumerate(g2, 51): raw[i] = c

g3 = "L10 C13 B12 G11 H12 H11 I12 G12 B2 B1 A2 Q9 R9 I11 J12 I8 H5 G4 I9 H8 G8 H9 G9 J8 K8 J10 K14 K17 L18 J7 E8 M12 L12 C16 L6 M6 B16 B15 B17 J18 H14 G14 N1 M1 O1 M2 E11 D11 E10 D12".split()
for i, c in enumerate(g3, 101): raw[i] = c

g4 = "I15 L16 E2 E1 K9 H10 R13 Q12 B13 B3 B4 D6 D5 L17 M18 F7 D7 G18 S12 I16 J19 I18 O6 M16 R19 O16 O17 Q16 O19 Q18 O15 R15 Q8 B14 C11 P9 E6 F6 E4 F5 K5 M5 J11 I10 K10 H15 J15 H13 I14 F19".split()
for i, c in enumerate(g4, 151): raw[i] = c

g5 = "D17 E16 I13 G13 J16 J17 E3 D2 S17 A16 B18 S18 E19 L11 E11 I19 K19 G19 M13 R15 Q15 F12 D9 H4 F10 F8 F9 S14 A17 A13 A12 S15 S13 L14 L15 M15 M14 K15 L13 K7 D6 A15 A14 L16".split()
for i, c in enumerate(g5, 201): raw[i] = c
# 245/246/249 原谱只在图外标注（提子记录），位置不可靠，交给引擎就近补
raw[245] = 'L14'; raw[246] = 'A13'; raw[247] = 'F2'; raw[248] = 'F3'; raw[249] = 'A14'; raw[250] = 'C19'

print('读谱条目', len(raw), '缺号', [n for n in range(1, 251) if n not in raw])
moves = []
for n in range(1, 251):
    c = raw[n]
    moves.append((19 - int(c[1:])) * 19 + ALPHA.index(c[0]))
json.dump(moves, open('moves_raw.json', 'w'))
print('样例', moves[:8], moves[-5:])
