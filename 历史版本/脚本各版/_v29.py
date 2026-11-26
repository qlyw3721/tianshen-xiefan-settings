# -*- coding: utf-8 -*-
import io, ast

SRC = '天神下凡设定集_归纳整理版_V2.8.md'
DST = '天神下凡设定集_归纳整理版_V2.9.md'
BLK = '_v29_block.md'

raw = io.open(SRC, encoding='utf-8', newline='').read()
assert '\n' not in raw.replace('\r\n', ''), 'SRC 含裸 LF'
L = raw.split('\r\n')
print('SRC lines', len(L))

# ---- 封面两处（V2.3 教训：封面必须核两处）----
assert L[3].count('**V2.8**') == 1, L[3][:80]
L[3] = L[3].replace('**V2.8**', '**V2.9**')
assert L[5] == '**版本**：V2.8（2026-11-26）', L[5]
L[5] = '**版本**：V2.9（2026-11-26）'

# ---- 行号纠错：名言 #132 L2727 → L2736（全稿仅一处）----
idx132 = [i for i, l in enumerate(L) if '**132**' in l and '太阳和月亮' in l]
assert len(idx132) == 1, ('#132 命中数', len(idx132))
i132 = idx132[0]
assert L[i132].count('L2727') == 1, L[i132][:160]
L[i132] = L[i132].replace('前传 **L2727**', '前传 **L2736**')
print('#132 行号已改 L2727→L2736 at line', i132 + 1)

# ---- 锚点唯一 ----
anchors = [i for i, l in enumerate(L) if l == '## 4. 使徒牌与帕雅战棋']
assert len(anchors) == 1, anchors
i = anchors[0]
print('anchor at', i + 1)

# ---- 插入块 ----
blk_raw = io.open(BLK, encoding='utf-8', newline='').read().replace('\r\n', '\n').strip('\n')
blines = blk_raw.split('\n')
for b in blines:
    assert '\r' not in b
print('block lines', len(blines))
assert not any(l == '## 4. 使徒牌与帕雅战棋' for l in blines)
assert blines[0].startswith('#### V2.9 补注'), blines[0][:40]

out = L[:i] + blines + [''] + L[i:]
io.open(DST, 'w', encoding='utf-8', newline='').write('\r\n'.join(out))
print('DST lines', len(out))

chk = io.open(DST, encoding='utf-8', newline='').read()
assert '\n' not in chk.replace('\r\n', ''), 'DST 出现裸 LF'
print('bare LF 0 OK')
print('V2.9 count', chk.count('V2.9'), '| V2.8 count', chk.count('V2.8'))
