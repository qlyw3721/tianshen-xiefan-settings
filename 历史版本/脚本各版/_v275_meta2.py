# -*- coding: utf-8 -*-
import io, os, shutil

# 说明集已由上一脚本更新，本脚本只处理台账 / 脚本版本号 / 升版
T = '设定集_裁定台账.md'
M = io.open(T, encoding='utf-8').read().split('\n')

ci = [i for i, l in enumerate(M) if l.startswith('| **当前版本** |')]
pi = [i for i, l in enumerate(M) if l.startswith('| **上一版** |')]
ppi = [i for i, l in enumerate(M) if l.startswith('| **上上版** |')]
assert len(ci) == 1 and len(pi) >= 1 and len(ppi) >= 1, (len(ci), len(pi), len(ppi))
# 滚动位置＝首条；其余为历史留档，一律不动
ci0, pi0, ppi0 = ci[0], pi[0], ppi[0]
old_cur, old_prev, old_preprev = M[ci0], M[pi0], M[ppi0]
assert 'v2.74' in old_cur and 'v2.73' in old_prev and 'v2.64' in old_preprev, (
    old_cur[:60], old_prev[:60], old_preprev[:60])

new_cur = (
    '| **当前版本** | 本机 **v2.75**（第一百一十四轮·**神学院—修道院建制通则**：用户裁定三层——'
    '① 神学院可由多个修道院组成（原文·前传 L2473，24 院，§1.4 已在库只抽为通则）；'
    '② 修道院隶属于神学院（【用户裁定】，本机零命中）；'
    '③ 足够强大的修道院其名可代表整个神学院（【用户裁定】）。'
    '新增 §1.5.13 五：三层关系表＋与 v1.90「神学院＝主修道院两称」咬合＋四条防误判'
    '（可代表≠都代表／院名代表≠实体合并·两榜不混／不得反推读卡尼／不划量化门槛）；'
    '解释奥丁修道院、石崖修道院以院名入帝国十大神学院榜。'
    '顺带修正主稿头部版本戳 v2.73→v2.75） | 2026-11-24 |'
)
new_detail = (
    '| **v2.75 建制通则落地** | 用户裁定三条：① 神学院由多个修道院组成（**原文·前传 L2473**，已在库不重建）；'
    '② 修道院**隶属于**神学院；③ 院足强则**院名代表整个神学院**（②③【用户裁定·建制通则】，零行号）。'
    '落点 §1.5.13 五（表格化三层关系＋4 条防误判）；咬合 §1.4 v1.90 防误判⑥（两称之机制，院长仍一位）；'
    '原五／六节顺延为六／七。 | 2026-11-24 |'
)
new_prev = old_cur.replace('**当前版本**', '**上一版**', 1)

M[ci0] = new_cur
M.insert(ci0 + 1, new_detail)
M.insert(ci0 + 2, new_prev)
# 两处插入后原 pi0 / ppi0 各后移 2 行
M[pi0 + 2] = old_prev.replace('**上一版**', '**上上版**', 1)
M[ppi0 + 2] = old_preprev.replace('**上上版**', '**历史版**', 1)

txt = '\r\n'.join(M)
io.open(T, 'w', encoding='utf-8', newline='').write(txt)
mirror = 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md'
if os.path.exists(os.path.dirname(mirror)):
    io.open(mirror, 'w', encoding='utf-8', newline='').write(txt)
    print('台账镜像 OK')
print('台账 OK', len(M), 'lines')

# 脚本版本号
Q = '_md2docx.py'
s = io.open(Q, encoding='utf-8').read()
assert s.count('v2.74') == 3, s.count('v2.74')
io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace('v2.74', 'v2.75'))
print('脚本版本号 OK')

# 先复制旧版入历史，再改名升版
hist = '历史版本/设定集各版/'
md_old = '天神下凡设定集_归纳整理版_v2.74.md'
md_new = '天神下凡设定集_归纳整理版_v2.75.md'
doc_old = '天神下凡设定集_归纳整理版_v2.74.docx'
assert not os.path.exists(hist + md_old), '历史已有 v2.74.md'
assert not os.path.exists(hist + doc_old), '历史已有 v2.74.docx'
shutil.copy2(md_old, hist + md_old)
shutil.move(doc_old, hist + doc_old)
os.rename(md_old, md_new)
print('升版 OK：', md_new)
