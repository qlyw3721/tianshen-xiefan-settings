# -*- coding: utf-8 -*-
"""v2.88 修正二：v2.33/v2.83 宿块正文与 v2.88 块顺序对调"""
import io

P = '天神下凡设定集_归纳整理版_v2.88.md'
lines = io.open(P, encoding='utf-8').read().split('\n')

def swap(v288_head, host_body_first, tag):
    a = None
    for i, l in enumerate(lines):
        if l.startswith(v288_head):
            a = i
            break
    assert a is not None, (tag, 'v288 head')
    # host_body_first 在 v2.88 块之后出现
    b = None
    for i in range(a + 1, len(lines)):
        if host_body_first in lines[i]:
            b = i
            break
    assert b is not None, (tag, 'host body')
    # v2.88 块 = lines[a:b]，宿块正文 = lines[b:next_head-空行]
    c = None
    for i in range(b + 1, len(lines)):
        if lines[i].startswith('#### ') or lines[i].startswith('### '):
            c = i
            break
    assert c is not None, (tag, 'next')
    # 宿块正文到 c（不含 c），去掉尾部多余空行
    host = lines[b:c]
    while host and host[-1].strip() == '':
        host.pop()
    v288 = lines[a:b]
    # 重排：宿块正文 + 空行 + v288块 + 空行（c 前原有空行保留）
    seg = host + [''] + v288 + ['']
    del lines[a:c]
    lines[a:a] = seg
    print(tag, 'fixed: v288 %d lines after host %d lines' % (len(v288), len(host)))

swap('#### v2.88 补注｜院长谱系补全', '> **补入缘由**：用户 2026-11-20 交付「人物：**圣徒阿乐翰**', 'yuanzhang')
swap('#### v2.88 补注｜摩尼黑神学院登记', '> **用户裁定**：针对 v2.82 交付所留「波克斯／纽芬兰二校', 'munihe')

raw = '\r\n'.join(lines)
assert raw.count('\n') == raw.count('\r\n'), 'naked LF'
io.open(P, 'w', encoding='utf-8', newline='').write(raw)
print('OK lines=%d bytes=%d' % (len(lines), len(raw.encode('utf-8'))))
