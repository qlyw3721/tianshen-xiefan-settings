# -*- coding: utf-8 -*-
"""v2.51 结构自查：标题前空行 / 表格列数 / 连续空行"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = sys.argv[1] if len(sys.argv) > 1 else '天神下凡设定集_归纳整理版_v2.51.md'
s = open(P, 'rb').read().decode('utf-8').replace('\r\n', '\n')
L = s.split('\n')

# 1) 标题前空行
bad_h = []
for i, l in enumerate(L):
    if re.match(r'^#{1,6} ', l) and i > 0 and L[i-1].strip() != '':
        bad_h.append((i+1, l[:60]))
print('标题前缺空行:', len(bad_h))
for x in bad_h: print('  ', x)

# 2) 表格列数
def cells(row):
    r = row.strip()
    if r.startswith('|'): r = r[1:]
    if r.endswith('|'): r = r[:-1]
    return len(r.split('|'))

bad_t = []
i = 0
while i < len(L):
    if L[i].strip().startswith('|'):
        j = i
        while j < len(L) and L[j].strip().startswith('|'):
            j += 1
        blk = list(range(i, j))
        cnt = {}
        for k in blk:
            c = cells(L[k])
            cnt.setdefault(c, []).append(k+1)
        if len(cnt) > 1:
            for c, rows in cnt.items():
                bad_t.append((c, rows[:6], L[blk[0]][:50]))
        i = j
    else:
        i += 1
print('表格列数不一致块:', len(bad_t))
for x in bad_t: print('  cols=%d rows=%s head=%s' % x)

# 3) 连续 4+ 空行
cnt4 = 0
run = 0
for l in L:
    if l.strip() == '':
        run += 1
        if run == 3:
            cnt4 += 1
    else:
        run = 0
print('3+连续空行(即4行):', cnt4)
