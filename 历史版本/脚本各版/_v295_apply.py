# -*- coding: utf-8 -*-
import io
P = '天神下凡设定集_归纳整理版_v2.94.md'
OUT = '天神下凡设定集_归纳整理版_v2.95.md'
BLOCK = '_v295_block.md'

raw = io.open(P, 'rb').read().decode('utf-8')
lines = raw.split('\r\n')

def rep(old, new, tag):
    idx = [i for i, l in enumerate(lines) if old in l]
    assert len(idx) == 1, (tag, len(idx))
    i = idx[0]
    lines[i] = lines[i].replace(old, new, 1)
    print('rep ok:', tag, 'line', i+1)

# 1. 头部版本戳 v2.94 -> v2.95（只前 2 行）
head_idx = [i for i, l in enumerate(lines[:12]) if 'v2.94' in l]
assert len(head_idx) == 2, head_idx
for i in head_idx:
    lines[i] = lines[i].replace('v2.94', 'v2.95', 1)
print('head stamp ok', [i+1 for i in head_idx])

# 2. 插块：v2.94 块末尾「6. **历史块不回改**」行后、v2.02 标题前
anchor = '#### v2.02 补注｜莱茵哈泰深化人物志："胖子"'
idx = [i for i, l in enumerate(lines) if l.startswith(anchor)]
assert len(idx) == 1, ('v2.02 anchor', len(idx))
i = idx[0]
assert lines[i-1].strip() == '', repr(lines[i-1][:50])
# 读块（Write 工具纯 LF），规范化为 CRLF 分段
braw = io.open(BLOCK, 'rb').read().decode('utf-8')
braw = braw.replace('\r\n', '\n')
block_lines = braw.split('\n')
# 插在 i 位置（v2.02 标题之前），块末已自带 --- 与空行
lines[i:i] = block_lines
print('block inserted at', i+1, 'lines', len(block_lines))

# 3. §14.3 大事件表：在「约 820–821 父母双亡」行后插 830 两行
anchor2 = '| 约 **820–821** | **父母双亡／罗桐柴尔德家族覆灭**'
idx = [i for i, l in enumerate(lines) if anchor2 in l]
assert len(idx) == 1, ('event anchor', len(idx))
j = idx[0]
new_rows = [
    '| **830** | **主角建立秩序（COSMO）**：以皇帝亲口任命的首脑身份正式成形，机构人员不足 10 人 | 甲 | 【用户裁定】第1章 L31/L48/L124；§3.16 v2.95 块四；与后传层「约 820 建立秩序」两存，旧行留档不回改 | 约 22 岁 |',
    '| **830** | **主角父母被绞死／罗桐柴尔德家族覆灭**：公爵以叛国罪上绞架、爱葛莉丝殉情，主角亲手告发并被剥夺爵位 | 甲／戊 | 【用户裁定】第1章 L37/L115/L122；与后传层「约 820–821 父母双亡」两存，代数 12／14 代冲突见 v2.95 块二 | 约 22 岁 |',
]
lines[j+1:j+1] = new_rows
print('event rows inserted after', j+1)

# 写回（CRLF）
io.open(OUT, 'w', encoding='utf-8', newline='').write('\r\n'.join(lines))
b = io.open(OUT, 'rb').read()
print('裸LF', b.count(b'\n') - b.count(b'\r\n'), '总行', b.count(b'\r\n'))
