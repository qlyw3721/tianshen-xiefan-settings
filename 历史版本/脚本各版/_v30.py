# -*- coding: utf-8 -*-
import io

SRC = '天神下凡设定集_归纳整理版_V2.9.md'
DST = '天神下凡设定集_归纳整理版_V3.0.md'
BLK = '_v30_block.md'

raw = io.open(SRC, encoding='utf-8', newline='').read()
assert '\n' not in raw.replace('\r\n', ''), 'SRC 含裸 LF'
L = raw.split('\r\n')
print('SRC lines', len(L))

# ---- 封面两处（V2.3 教训：封面必须核两处）----
# L[3] 只改加粗的版本戳，口径说明里的「V2.9 → V3.0」示例不动
assert L[3].count('**V2.9**') == 1, L[3][:120]
L[3] = L[3].replace('**V2.9**', '**V3.0**')
assert L[5] == '**版本**：V2.9（2026-11-26）', L[5]
L[5] = '**版本**：V3.0（2026-11-26）'
print('封面两处已改 V2.9→V3.0')

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
assert blines[0].startswith('#### V3.0 补注'), blines[0][:40]

out = L[:i] + blines + [''] + L[i:]
io.open(DST, 'w', encoding='utf-8', newline='').write('\r\n'.join(out))
print('DST lines', len(out))

chk = io.open(DST, encoding='utf-8', newline='').read()
assert '\n' not in chk.replace('\r\n', ''), 'DST 出现裸 LF'
print('bare LF 0 OK')
print('V3.0 count', chk.count('V3.0'), '| V2.9 count', chk.count('V2.9'))
