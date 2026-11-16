# -*- coding: utf-8 -*-
"""世界地图 v1.0 → v1.1：v1.79 增标（九大龙脉／玛索郡西北／奥格斯歌东南／P3 新地点）。"""
import re, sys

SRC = '天神下凡_世界地图_v1.0.svg'
DST = '天神下凡_世界地图_v1.1.svg'

s = open(SRC, encoding='utf-8').read()
n0 = len(s)

def rep1(old, new, tag):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit('[%s] 命中 %d 次：%s' % (tag, c, old[:60]))
    s = s.replace(old, new, 1)
    print('OK  ', tag)

# ---------- 1. 画布加高 120（1620→1740） ----------
rep1('width="960" height="1620" viewBox="0 0 960 1620"',
     'width="960" height="1740" viewBox="0 0 960 1740"', '1 画布')
rep1('<rect x="0" y="0" width="960" height="1580" fill="#f3e9d2"/>',
     '<rect x="0" y="0" width="960" height="1700" fill="#f3e9d2"/>', '2 底色')
rep1('<rect x="16" y="16" width="928" height="1588" fill="none" stroke="#8a6d3b" stroke-width="3"/>',
     '<rect x="16" y="16" width="928" height="1708" fill="none" stroke="#8a6d3b" stroke-width="3"/>', '3 外框')
rep1('<rect x="24" y="24" width="912" height="1572" fill="none" stroke="#8a6d3b" stroke-width="1" opacity="0.6"/>',
     '<rect x="24" y="24" width="912" height="1692" fill="none" stroke="#8a6d3b" stroke-width="1" opacity="0.6"/>', '4 内框')

# ---------- 2. 副标题 ----------
rep1('v1.69 增标地名与场景 · 续补·原创绘制）</text>',
     'v1.69 增标地名与场景 · <tspan font-weight="bold">v1.79 增标九大龙脉／玛索郡更正西北／奥格斯歌城更正东南</tspan> · 续补·原创绘制）</text>', '5 副标题')

# ---------- 3. 神圣帝国区点位 ----------
rep1('<text x="766" y="552" text-anchor="middle">●奥格斯歌（东北经济之都）</text>',
     '<text x="770" y="646" text-anchor="middle">●奥格斯歌（东南经济之都·东南隅）</text>', '6 奥格斯歌→东南')
rep1('<text x="820" y="592" text-anchor="end">◆ 德古拉之牙（奥格斯歌城最高建筑）</text>',
     '<text x="816" y="664" text-anchor="end">◆ 德古拉之牙（占星楼）</text>', '7 德古拉之牙')
rep1('<text x="820" y="610" text-anchor="end" font-size="10" fill="#8a2f2a">◆ 瑕多丽庄园（奥格斯歌城近郊 · 血鳞石 · 采邑）【续补·原创定位】</text>',
     '<text x="816" y="700" text-anchor="end" font-size="10" fill="#8a2f2a">◆ 瑕多丽庄园（血鳞石 · 采邑）</text>', '8 瑕多丽')
rep1('<text x="820" y="628" text-anchor="end" font-size="10" fill="#5a7d5a">◆ 塞缪耳森林（帝国东南玛敦郡 · 异教徒根据地）【续补·原创定位】</text>',
     '<text x="880" y="628" text-anchor="end" font-size="10" fill="#5a7d5a">◆ 塞缪耳森林（玛敦郡 · 异教徒）</text>', '9 塞缪耳')
rep1('<text x="820" y="574" text-anchor="end">◆ 玛索亚（下午茶）</text>',
     '<text x="592" y="560" text-anchor="end" font-size="10">◆ 玛索亚＝玛索郡（西北 · 下午茶）</text>', '10 玛索亚→西北')

# ---------- 4. 新增玛索郡建筑（P3 入库） ----------
NEW_SITE = '''    <text x="592" y="578" text-anchor="end" font-size="10" fill="#8a2f2a">◆ 白象城堡（玛索郡西北角 · 军事堡垒式 · 俯瞰黑天鹅湖）【P3】</text>
    <text x="575" y="612" text-anchor="end" font-size="10" fill="#5a7d5a">◆ 贝福德山脉·玛索平原·佛伦萨森林</text>
'''
anchor_af = '    <text x="880" y="560" text-anchor="end">◆ 诗呢哥城堡／黑天鹅湖（秩序总部 · 脉点）</text>'
rep1(anchor_af, anchor_af + '\n' + NEW_SITE.rstrip('\n'), '11 白象城堡等')

# ---------- 5. 九大龙脉 ◇ 点位 ----------
LONGMAI = '''  <!-- ===================== v1.79 九大龙脉（◇） ===================== -->
  <g font-size="10.5" fill="#6b3a8a">
    <text x="706" y="200">◇ 缪斯祖脉（娲龙）</text>
    <text x="418" y="290">◇ 许珀波瑞（极夜霜龙）</text>
    <text x="824" y="530">◇ 摩纳哥（冰霜三龙）</text>
    <text x="486" y="542">◇ 乔纳森（红龙）</text>
    <text x="842" y="690">◇ 科尔基斯（幼龙）</text>
    <text x="392" y="728">◇ 圣梅根（提坦龙·最大）</text>
    <text x="528" y="688" text-anchor="end">◇ 德莱叶（火龙）</text>
    <text x="130" y="788">◇ 厄瑞波斯（暮影龙）</text>
    <text x="98" y="910" text-anchor="middle">◇ 涣歌（德莱赛水龙）</text>
  </g>

'''
anchor_legend = '  <!-- ===================== 图例与注记 ===================== -->'
rep1(anchor_legend, LONGMAI + anchor_legend, '12 九大龙脉')

# ---------- 6. 底部 v1.79 索引区 ----------
IDX = '''  <!-- ===================== v1.79 增标索引（与设定集 §1.10 七对应） ===================== -->
  <text x="60" y="1622" font-size="11.5" font-weight="bold" fill="#6b3a8a">◇ 九大龙脉（v1.79 用户裁定 · 设定集 §6.3）：原初四＝圣梅根（中部·最大）· 摩纳哥（玛雅山脉）· 许珀波瑞（卡妙极北）· 厄瑞波斯（奥古迦西陲）｜后得五＝德莱叶（帝国西南）· 乔纳森（帝都西南）· 涣歌（龙脊海沟）· 缪斯祖脉（缪斯北地）· 科尔基斯（高加索）。</text>
  <text x="60" y="1646" font-size="11.5" fill="#6b3a8a">◇＝龙脉；原初四为《摩西神律》签约「禁锢之脉」（龙不可离），后得五为神律发布后新发现（不受禁锢）。「四条」为签约层之数、与「九条」世界数并存不冲突（§6.3 v1.79 裁定补注）。</text>
  <text x="60" y="1670" font-size="11" fill="#8a2f2a">◆ v1.79 增补（P3 入库）：白象城堡（玛索郡西北角·贝福德山脉顶点）· 贝福德山脉 · 玛索平原 · 佛伦萨森林；城内街区（洛丽塔三街／梵妮事务厅／小玛丽断头台）依 §0.6 第十三款第 6 条不作硬定位、不入图。</text>
  <text x="60" y="1694" font-size="11" fill="#8a2f2a">方位订正（用户 2026-11-16 裁定）：玛索郡 东北→<tspan font-weight="bold">西北</tspan>（后传 L1520／L1012）｜奥格斯歌城 东北→<tspan font-weight="bold">东南</tspan>（前传 L1384／L1474）；神圣帝国本体仍在史诗大陆东北，奥歌为其东南隅。前后传 txt 一字不改。</text>
'''
# 插在最后一个 </svg> 前
i = s.rindex('</svg>')
s = s[:i] + IDX + s[i:]
print('OK   13 v1.79 索引区')


# ---------- 7. 帝都南疆注记瘦身（为东南集群让位） ----------
for old, new in [
 ('<text x="560" y="648" font-size="10">◆ 黄昏盆地（帝国南疆 · 翡翠河战役）</text>',
  '<text x="560" y="648" font-size="10">◆ 黄昏盆地（帝国南疆）</text>'),
 ('<text x="560" y="666" font-size="10">◆ 翡翠河（盆地内渡口【续补·原创定位】）</text>',
  '<text x="560" y="666" font-size="10">◆ 翡翠河（渡口）</text>'),
 ('<text x="560" y="684" font-size="10">◆ 罗伽费因格竞技场（帝都朱庇特城）</text>',
  '<text x="560" y="684" font-size="10">◆ 罗伽费因格竞技场（帝都）</text>'),
 ('<text x="560" y="702" font-size="10">◆ 帝国学院（帝都朱庇特城 · 第三骑士掌院）</text>',
  '<text x="560" y="702" font-size="10">◆ 帝国学院（帝都）</text>'),
]:
    if s.count(old) != 1:
        raise SystemExit('瘦身锚点未命中：' + old[:60])
    s = s.replace(old, new, 1)
s = s.replace('y="720" font-size="10" fill="#3f6e80"', 'y="716" font-size="10" fill="#3f6e80"', 1)
print('OK   14 南疆注记瘦身＋茴香微调')


# ---------- 8. 既有重叠微调 ----------
for old, new in [
 ('<text x="880" y="560" text-anchor="end">◆ 诗呢哥城堡／黑天鹅湖（秩序总部 · 脉点）</text>',
  '<text x="880" y="546" text-anchor="end">◆ 诗呢哥城堡／黑天鹅湖（秩序总部 · 脉点）</text>'),
 ('<text x="880" y="596" text-anchor="end">◆ 审判之庭（朱庇特城 · 圣约翰大教堂对面）</text>',
  '<text x="880" y="592" text-anchor="end">◆ 审判之庭（朱庇特城 · 圣约翰大教堂对面）</text>'),
 ('<text x="618" y="500" text-anchor="middle">●莱辛葛郡（北境牧区）</text>',
  '<text x="596" y="506" text-anchor="middle">●莱辛葛郡（北境牧区）</text>'),
]:
    if s.count(old) != 1:
        raise SystemExit('微调锚点未命中：' + old[:60])
    s = s.replace(old, new, 1)
print('OK   15 既有重叠微调')


# ---------- 9. 波坎儿右对齐 ----------
_old = '<text x="575" y="592" text-anchor="start">◆ 波坎儿（帝都近郊 · 奶茶 · 红酒）</text>'
if s.count(_old) == 1:
    s = s.replace(_old, '<text x="560" y="592" text-anchor="end">◆ 波坎儿（帝都近郊 · 奶茶 · 红酒）</text>', 1)
    print('OK   16 波坎儿右对齐')

open(DST, 'w', encoding='utf-8', newline='').write(s)
print('写出：', DST, n0, '→', len(s), 'bytes')
