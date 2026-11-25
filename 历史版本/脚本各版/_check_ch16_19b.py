# -*- coding: utf-8 -*-
import io, re
L = io.open('天神下凡设定集_归纳整理版_v2.101.md', 'r', encoding='utf-8', newline='').read().split('\r\n')

def s(p):
    return [i+1 for i, l in enumerate(L) if re.search(p, l)]

print('=== 钓鱼计/放走活口 变体 ===')
for p in ['钓鱼','放.{0,6}活口','留.{0,4}活口','跟踪','追剿','钓','一两个.{0,8}活']:
    h = s(p); print('%-18s %s' % (p, ('0' if not h else '%d first=%d' % (len(h), h[0]))))

print()
print('=== 一夫当关/万夫莫开 变体 ===')
for p in ['一夫当关','万夫莫开','一枪.{0,4}关','当关']:
    h = s(p); print('%-18s %s' % (p, ('0' if not h else str(h[:5]))))

print()
print('=== 亡灵系诅咒/只有一枪/迟到 变体 ===')
for p in ['亡灵.{0,6}诅咒','只有一枪','一枪','宽恕.{0,6}迟到','请宽恕','迟.{0,2}到','曼陀','罂粟','碍眼','小玩意','双刃']:
    h = s(p); print('%-18s %s' % (p, ('0' if not h else '%d first=%d' % (len(h), h[0]))))

print()
print('=== 老丕平年岁/忠诚/儿子背 变体 ===')
for p in ['伺候.{0,4}忠诚','词典.{0,8}忠诚','老.{0,2}不中用','老了','多背','背.{0,6}几次','我的儿子','未来的儿子','等着你背','还等']:
    h = s(p); print('%-18s %s' % (p, ('0' if not h else '%d first=%d' % (len(h), h[0]))))

print()
print('=== 最优雅绅士/浩瀚枯井/工匠/会很苦 变体 ===')
for p in ['最优雅','优雅.{0,4}绅士','浩瀚','大海','枯井','深不见底','工匠.{0,8}半年','半年','很苦','会.{0,2}苦','合格']:
    h = s(p); print('%-18s %s' % (p, ('0' if not h else '%d first=%d' % (len(h), h[0]))))

print()
print('=== 原文行号引用覆盖：L690-851 ===')
# 查设定集里是否有"前传 Lxxx"形式引用了本批次行号
refs = []
for i, l in enumerate(L):
    for m in re.finditer(r'(?:前传\s*)?L(\d{3,4})', l):
        n = int(m.group(1))
        if 690 <= n <= 851:
            refs.append((n, i+1))
from collections import Counter
byline = sorted(set(n for n, _ in refs))
print('被引用的原文行号(%d个):' % len(byline), byline)
