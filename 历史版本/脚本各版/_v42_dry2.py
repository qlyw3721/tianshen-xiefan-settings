# -*- coding: utf-8 -*-
import re
SRC = '天神下凡设定集_归纳整理版_V4.1.md'
lines = open(SRC, 'rb').read().decode('utf-8').split('\r\n')

PROT = re.compile(r'「[^」]*」|『[^』]*』|“[^”]*”')
# 显式保护：跨行原文块，含专名但引号不配对
WHITE = {10149, 10150, 10151, 10152, 10153, 10154, 10155}

def rn(t):
    return t.replace('庞培', '庞贝').replace('克拉苏', '克拉夫')

def fix(s):
    if s.count('「') != s.count('」') or s.count('『') != s.count('』'):
        return None
    out = []; last = 0
    for m in PROT.finditer(s):
        out.append(rn(s[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(rn(s[last:]))
    return ''.join(out)

rep = []; skip = []
for i, l in enumerate(lines):
    n = i + 1
    if not any(k in l for k in ('庞培', '克拉夫', '克拉苏', '克罗夫')):
        continue
    if n in WHITE:
        skip.append((n, l, '白名单·跨行原文块')); continue
    r = fix(l)
    if r is None:
        skip.append((n, l, '引号不配对')); continue
    if r != l:
        rep.append((n, l, r))

print('=== 待改 %d 行／跳过 %d 行 ===' % (len(rep), len(skip)))
for n, a, b in rep:
    print('---L%d' % n)
    print('  前|%s' % a[:300])
    print('  后|%s' % b[:300])
print()
print('=== 跳过（需人工） ===')
for n, a, t in skip:
    print('---L%d [%s]' % (n, t))
    print('    |%s' % a[:300])
