# -*- coding: utf-8 -*-
import io, re
L = io.open('天神下凡设定集_归纳整理版_v2.101.md', 'r', encoding='utf-8', newline='').read().split('\r\n')

# 严格：只取明确带"前传"字样的行号引用
strict = set()
loose = set()
for i, l in enumerate(L):
    for m in re.finditer(r'L(\d{3,4})', l):
        n = int(m.group(1))
        if not (635 <= n <= 851):
            continue
        loose.add(n)
        # 看该行号前60字符内是否有"前传"，且非"后传"
        pre = l[max(0, m.start()-60):m.start()]
        post = l[m.end():m.end()+10]
        if '前传' in pre and '后传' not in pre:
            strict.add(n)
print('严格前传引用行号(%d):' % len(strict), sorted(strict))
print('宽松混合引用行号(%d):' % len(loose), sorted(loose))
print('仅宽松(可能后传误入):', sorted(loose - strict))

print()
print('=== 关键金句/设定点 精确字面(含变体) ===')
PATS = {
 '我看到我征服': r'我看到.{0,2}我征服',
 '从来只有一枪': r'从来只有.{0,2}枪',
 '请宽恕我的迟到': r'宽恕.{0,4}迟到',
 '一夫当关': r'一夫当关',
 '钓鱼计': r'落网之鱼|放.{0,4}活口|遗落.{0,4}鱼',
 '血债血还': r'血债血还|以牙还牙',
 '懦夫': r'懦夫',
 '曼陀罂粟': r'曼陀|罂粟花.{0,4}黑暗',
 '碍眼小玩意': r'碍眼.{0,6}玩意',
 '双刃剑': r'双刃|双刃剑',
 '我老了不中用': r'老了.{0,4}不中用|不中用',
 '浩瀚大海枯井': r'浩瀚.{0,6}大海|枯井',
 '最优雅绅士': r'最优雅.{0,4}绅士',
 '工匠半年': r'工匠.{0,8}半年',
 '会很苦': r'会.{0,2}苦呢',
 '合格吧': r'合格吧|能给个合格',
 '骨骼肌黄金分割': r'骨骼肌.{0,40}黄金分割|黄金分割',
 '帝国第七骑士': r'帝国第七骑士',
 '五六年': r'五六年',
}
for name, pat in PATS.items():
    h = [i+1 for i, l in enumerate(L) if re.search(pat, l)]
    print('%-16s %s' % (name, ('0' if not h else '%d first=%d' % (len(h), h[0]))))
