# -*- coding: utf-8 -*-
import io, ast

SRC = '天神下凡设定集_归纳整理版_V2.7.md'
DST = '天神下凡设定集_归纳整理版_V2.8.md'
BLK = '_v28_block.md'

raw = io.open(SRC, encoding='utf-8', newline='').read()
assert '\n' not in raw.replace('\r\n', ''), 'SRC 含裸 LF'
L = raw.split('\r\n')
print('SRC lines', len(L))

# 封面两处（V2.3 教训：封面必须核两处）
assert L[3].count('**V2.7**') == 1, L[3][:80]
L[3] = L[3].replace('**V2.7**', '**V2.8**')
assert L[5] == '**版本**：V2.7（2026-11-26）', L[5]
L[5] = '**版本**：V2.8（2026-11-26）'

# 锚点唯一
anchors = [i for i, l in enumerate(L) if l == '## 4. 使徒牌与帕雅战棋']
assert len(anchors) == 1, anchors
i = anchors[0]
print('anchor at', i + 1)

blk_raw = io.open(BLK, encoding='utf-8', newline='').read().replace('\r\n', '\n').strip('\n')
blines = blk_raw.split('\n')
for b in blines:
    assert '\r' not in b
print('block lines', len(blines))
assert not any(l == '## 4. 使徒牌与帕雅战棋' for l in blines)
# 块首必须为 V2.8 补注标题
assert blines[0].startswith('#### V2.8 补注'), blines[0][:40]

out = L[:i] + blines + [''] + L[i:]
io.open(DST, 'w', encoding='utf-8', newline='').write('\r\n'.join(out))
print('DST lines', len(out))

chk = io.open(DST, encoding='utf-8', newline='').read()
assert '\n' not in chk.replace('\r\n', ''), 'DST 出现裸 LF'
print('bare LF 0 OK')
print('V2.8 count', chk.count('V2.8'), '| V2.7 count', chk.count('V2.7'))
