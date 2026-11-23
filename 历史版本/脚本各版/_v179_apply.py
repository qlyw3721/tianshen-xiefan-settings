# -*- coding: utf-8 -*-
"""执行 v1.79 裁定回填：六条裁定（用户 2026-11-16）落盘。
用法：python _v179_apply.py
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _v179_blocks as K

SRC = '天神下凡设定集_归纳整理版_v1.78.md'
DST = '天神下凡设定集_归纳整理版_v1.79.md'

raw = open(SRC, 'rb').read().decode('utf-8')
assert '\r\n' in raw
text = raw.replace('\r\n', '\n')

def rep1(old, new, tag):
    global text
    n = text.count(old)
    if n != 1:
        raise SystemExit('[%s] 锚点命中 %d 次：%s' % (tag, n, old[:70]))
    text = text.replace(old, new, 1)
    print('OK  ', tag)

def ins(anchor, block, tag):
    global text
    n = text.count(anchor)
    if n != 1:
        raise SystemExit('[%s] 插入锚点命中 %d 次：%s' % (tag, n, anchor[:70]))
    text = text.replace(anchor, block + anchor, 1)
    print('OK  ', tag, '（插入 %d 字符）' % len(block))

# ---------- 1. 五块插入 ----------
rep1(K.T13_ANCHOR, K.T13_ANCHOR + '\n' + K.T13_ROWS, '1. §1.3 主表补 7 行')

ins(K.B63_ANCHOR, K.B63, '2. §6.3 九大龙脉总表')
ins(K.B82_ANCHOR, K.B82, '3. §8.2 龙种—龙脉对照')
ins(K.B53_ANCHOR, K.B53, '4. §5.3 龙骑士定案')
ins(K.B52_ANCHOR, K.B52, '5. §5.2 三封印正名')

# ---------- 2. 替换项 ----------
rep1(K.OLD_MS, K.NEW_MS, '6. §1.2.5 玛索郡→西北')
rep1(K.OLD_SK, K.NEW_SK, '7. §1.10 方位骨架')
rep1(K.OLD_ASCII, K.NEW_ASCII, '8. ASCII 轮廓图 奥格斯歌/玛索亚')
rep1(K.OLD_KY, K.NEW_KY, '9. §1.9 库亚平原地图注')
rep1(K.OLD_T151, K.NEW_T151, '10. §1.5.1 标题状态')
ins(K.T151_ADD_ANCHOR, K.T151_ADD, '11. §1.5.1 裁定回填注')

for i in sorted(K.OLD_P3):
    rep1(K.OLD_P3[i], K.NEW_P3[i], '12.%d §11.1 P3 第 %d 项' % (i, i))
rep1(K.OLD_V176_1, K.NEW_V176_1, '13. §11.1 v1.76 第 1 项')

# ---------- 3. 顶部时间戳 ----------
lines = text.split('\n')
assert lines[2].startswith('> 更新时间戳'), lines[2][:40]
STAMP = ('> 更新时间戳：2026-11-16（GMT+8）｜**v1.79**｜**第十八轮：用户六条裁定回填（九大龙脉＋龙族分支归属／三封印正名／龙骑士独立／地图与总纲处理／两处方位更正）**：'
 '① **龙脉定为 9 条**（原文 **L1459**「9条龙脉」）：**原初四脉**（圣梅根／摩纳哥／许珀波瑞／厄瑞波斯）＝《摩西神律》签约禁锢之脉，**后得五脉**（德莱叶／乔纳森／涣歌／缪斯祖脉／科尔基斯）＝神律发布后新发现、不受禁锢；「四条」为签约层之数，一字不改、两数各管一层，互不冲突；'
 '② **龙族分支各居一脉**（用户插话追加）：提坦龙→圣梅根、冰霜三龙→摩纳哥、极夜霜龙→许珀波瑞、暮影龙→厄瑞波斯、安格尔火龙→德莱叶、圣荣格芬兰红龙→乔纳森、德莱赛水龙→涣歌、娲龙→缪斯祖脉、卡洛琳幼龙→科尔基斯；**原文内证闭环**：卡培拉可离脉（L6494 例外一）、丹东离脉遭追剿而陨落（L4378／L3810），恰证「禁锢只对未被豁免者生效」；'
 '③ **三封印正名以前传为准**（之环／之心／十三黑色羽翼），后传三写降为别名，**「13 圣徒」保留待裁**（不并、不废、不解释）；'
 '④ **龙骑士独立于骑士命名体系之外、是骑士中的特殊存在**：不进阶位序列、不设号段，与阶位两套并行（L1811／L1852／L1853 三处内证按此重解）；'
 '⑤ **玛索郡更正为西北**（L1520／L1012）、**奥格斯歌城为东南**（L1384／L1474），§1.2.5／§1.10／ASCII 轮廓图／地图 v1.1 全部同步；'
 '⑥ **地图 SVG 回灌**（集中增标一批，升 v1.1）、**总纲文件名与正文一致**改《八百万字完本总纲》；⑦ §11.1 收口 6 项（P3 第 1／3／7／9／13／15 项＋v1.76 第 1 项）、余项续挂；'
 '⑧ 本批**不新增 >841 故事年份、不写续写正文、不排产**；前后传 txt sha 未变；**未上传资料库**（承 §0.6 第十五款）。')
lines[2] = STAMP
text = '\n'.join(lines)
print('OK   14. 顶部时间戳')

# ---------- 4. 修订记录追加 ----------
OLD_TAIL = '**未上传资料库**，在线节点维持 v1.77（承 §0.6 第十五款）。'
NEW_TAIL = (OLD_TAIL + ' → **v1.79（2026-11-16 第十八轮·用户六条裁定）**：① 龙脉扩为 **9 条**（原初四＋后得五，「四条」为签约层之数不改）；'
 '② 新立「**龙族分支各居一脉**」对应表（9 支，含 2 支原创龙种）；③ 三封印**正名以前传为准**、「13 圣徒」保留待裁；'
 '④ **龙骑士独立于骑士命名体系**（不进阶位序列）；⑤ 玛索郡→**西北**、奥格斯歌城→**东南**；⑥ 地图 SVG 增标升 **v1.1**、总纲改《八百万字完本总纲》；'
 '⑦ §11.1 收口 6 项。')
rep1(OLD_TAIL, NEW_TAIL, '15. 修订记录追加')

# ---------- 5. 写回 CRLF ----------
out = text.replace('\n', '\r\n')
open(DST, 'wb').write(out.encode('utf-8'))
print('写出：', DST, len(out.encode('utf-8')), 'bytes')
