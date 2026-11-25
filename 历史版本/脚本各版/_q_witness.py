# -*- coding: utf-8 -*-
import io
F = '天神下凡设定集_归纳整理版_v2.98.md'
L = io.open(F, 'r', encoding='utf-8', newline='').read().split('\r\n')

def show(kw, limit=6, width=280):
    hits = [i for i, l in enumerate(L) if kw in l]
    print('### %s : %d hits' % (kw, len(hits)))
    for i in hits[:limit]:
        print('%d| %s' % (i + 1, L[i][:width]))
    print()

for kw in ['Q1', 'Q2', 'Q3', 'Q4', '拿不准（交用户裁定', '交用户裁定',
           '朱庇特', '朱批特', '朱毗特', '其实是个女孩', '女孩.*谣言',
           '六岁', '七岁', '三年', '五年', '异写', '商业化前统一']:
    show(kw)
