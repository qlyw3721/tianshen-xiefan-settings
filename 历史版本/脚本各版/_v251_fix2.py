# -*- coding: utf-8 -*-
"""v2.51 收尾修正：节号（口子一在 §7.2）＋防误判④ 结案标记"""
P = '天神下凡设定集_归纳整理版_v2.51.md'
s = open(P, 'rb').read().decode('utf-8').replace('\r\n', '\n')

def rep(old, new, tag, cnt=1):
    n = s.count(old)
    assert n == cnt, '[FAIL] %s count=%d' % (tag, n)
    return s.replace(old, new)

s = rep('③ §7.1「口子一」改写为「不是终极体，只到接近」', '③ §7.2「口子一」改写为「不是终极体，只到接近」', 'stamp-sec')
s = rep('④ §7.1 「口子一」改写为 **「新物种」不是终极体', '④ §7.2 「口子一」改写为 **「新物种」不是终极体', 'rev-sec')
s = rep('| §7.1 口子一／§7.1 时序闭合后边界／附录 A |', '| §7.2 口子一／§7.1 时序闭合后边界／附录 A |', 'reg-sec')
s = rep('④ 安东尼奥亲王与 §3.2 罗桐柴尔德老家主**安东尼奥**是**同名异人**（→ **T-14**）。',
        '④ 安东尼奥亲王与 §3.2 罗桐柴尔德老家主**安东尼奥**是**同名异人**（**T-14 已结案 · v2.51 用户裁**）。', 'fangwu4')
print('fix2 ok')
open(P, 'wb').write(s.replace('\n', '\r\n').encode('utf-8'))
