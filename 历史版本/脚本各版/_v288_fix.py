# -*- coding: utf-8 -*-
"""v2.88 修正：移动两个误插块到宿块尾 + 删名言表多余空行"""
import io

P = '天神下凡设定集_归纳整理版_v2.88.md'
lines = io.open(P, encoding='utf-8').read().split('\n')

def move_block(head_prefix, next_head_prefix, tag):
    start = None
    for i, l in enumerate(lines):
        if l.startswith(head_prefix):
            start = i
            break
    assert start is not None, (tag, 'head')
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(next_head_prefix):
            end = i
            break
    assert end is not None, (tag, 'next')
    # 块范围 start..end-1（end-1 为空行则含入块尾）
    if lines[end - 1].strip() == '':
        block = lines[start:end - 1]
        del lines[start:end - 1]
    else:
        block = lines[start:end]
        del lines[start:end]
    # 删除后 next 块头位于 start；确保其前恰有一个空行
    # 块插入位置：next 块头前，先确保块前有空行
    if start > 0 and lines[start - 1].strip() == '':
        pos = start - 1  # 复用已有空行
        lines[pos:pos] = block + ['']
    else:
        lines[start:start] = [''] + block + ['']
    print(tag, 'moved: %d lines -> before L%d' % (len(block), start + 1))

# 1) 院长谱系块移到 v2.37 块头前（即 v2.33 块尾）
move_block('#### v2.88 补注｜院长谱系补全', '#### v2.37 补注｜铁拔翁树', 'yuanzhang')

# 2) 摩尼黑块移到 1.5.14 块头前（即 v2.83 块尾）
move_block('#### v2.88 补注｜摩尼黑神学院登记', '#### 1.5.14 厄休拉大地树眼', 'munihe')

# 3) 名言表：删除 #166 行后的多余空行（#167 前不应隔空行）
idx = [i for i, l in enumerate(lines) if l.startswith('| **167** |')]
assert len(idx) == 1
i = idx[0]
if lines[i - 1].strip() == '' and lines[i - 2].startswith('| **166** |'):
    del lines[i - 1]
    print('quote blank removed')

raw = '\r\n'.join(lines)
assert raw.count('\n') == raw.count('\r\n'), 'naked LF'
io.open(P, 'w', encoding='utf-8', newline='').write(raw)
print('OK lines=%d bytes=%d' % (len(lines), len(raw.encode('utf-8'))))
