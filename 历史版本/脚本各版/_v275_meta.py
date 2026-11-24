# -*- coding: utf-8 -*-
import io, os, shutil

# ---------- 说明集 ----------
S = '天神下凡设定集版本更新说明集.md'
L = io.open(S, encoding='utf-8').read().split('\n')
old6 = [l for l in L if l.startswith('> **现行版本**：')]
assert len(old6) == 1, ('现行版本行', len(old6))
L[L.index(old6[0])] = (
    '> **现行版本**：**v2.75**｜2026-11-24（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.75.md`'
    '｜**本版一事**：**神学院—修道院建制通则**（用户裁定三层：神学院可由多个修道院组成【原文·前传 L2473】'
    '／修道院隶属于神学院／足够强大的修道院其名可代表整个神学院，后两层【用户裁定】本机零命中）。'
    '（v2.74 十项设定戳、v2.73 五问戳依次下移。）'
)
assert L[10] == '## 一、版本戳（最新在上 · v2.74 → v1.0）', L[10][:80]
L[10] = '## 一、版本戳（最新在上 · v2.75 → v1.0）'
stamp = (
    '> 更新时间戳：2026-11-24（GMT+8）｜**v2.75**｜**第一百一十四轮：神学院—修道院建制通则**'
    '——用户裁定三条：① 神学院可由多个修道院组成（**原文·前传 L2473**「由地点不同的 24 个修道院组成，'
    '各院距离不远、皆建于山顶」，§1.4 v1.84／v2.55 块已载，本轮依「已有则忽略」抽为通则）；'
    '② 修道院**隶属于**神学院（【用户裁定·建制通则】，本机「隶属于／修道院隶属于」0 命中，不写行号）；'
    '③ 某一修道院**足够强大**时其名可代表整个神学院（同上，用户裁定）。'
    '新增 §1.5.13 五：三层关系表＋与 §1.4 v1.90「脉代奥拉神学院＝主修道院两称」防误判⑥的咬合'
    '（给出「何以两称」机制，院长仍只一位）＋四条防误判（可代表≠都代表／院名代表≠实体合并、'
    '两榜不混／不得反推读卡尼／不划量化门槛）；**奥丁修道院、石崖修道院以院名入帝国十大神学院榜**由此得解。'
    '原 §1.5.13 五、六顺延为六、七；§1.4 防误判⑥补交叉。'
    '顺带修正主稿头部版本戳 **v2.73→v2.75**（v2.74 轮漏改）。'
    'md **21,665 行／3,405,125 B／裸 LF 0**；四件套全绿。'
)
assert L[12].startswith('> 更新时间戳：') and 'v2.74' in L[12], L[12][:80]
L.insert(12, stamp)
io.open(S, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('说明集 OK', len(L), 'lines')

# ---------- 台账 ----------
T = '设定集_裁定台账.md'
M = io.open(T, encoding='utf-8').read().split('\n')


def loc(s, tag):
    idx = [i for i, l in enumerate(M) if l == s]
    assert len(idx) == 1, (tag, len(idx), idx[:5])
    return idx[0]


ci = loc('| **当前版本** |', '当前版本') if any(l == '| **当前版本** |' for l in M) else None
ci = [i for i, l in enumerate(M) if l.startswith('| **当前版本** |')]
pi = [i for i, l in enumerate(M) if l.startswith('| **上一版** |')]
ppi = [i for i, l in enumerate(M) if l.startswith('| **上上版** |')]
assert len(ci) == len(pi) == len(ppi) == 1, (len(ci), len(pi), len(ppi))
old_cur, old_prev, old_preprev = M[ci[0]], M[pi[0]], M[ppi[0]]

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
M[ci[0]] = new_cur
M.insert(ci[0] + 1, new_detail)
pi = [i for i, l in enumerate(M) if l.startswith('| **上一版** |')]
ppi = [i for i, l in enumerate(M) if l.startswith('| **上上版** |')]
M[pi[0]] = old_cur.replace('**当前版本**', '**上一版**', 1)
M[ppi[0]] = old_prev.replace('**上一版**', '**上上版**', 1)
# 旧「上上版」降为「历史版」
hi = [i for i, l in enumerate(M) if l.startswith('| **上上版** |')]
M[hi[0]] = old_preprev.replace('**上上版**', '**历史版**', 1)

txt = '\r\n'.join(M)
io.open(T, 'w', encoding='utf-8', newline='').write(txt)
mirror = 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md'
if os.path.exists(os.path.dirname(mirror)):
    io.open(mirror, 'w', encoding='utf-8', newline='').write(txt)
    print('台账镜像 OK')
print('台账 OK', len(M), 'lines')

# ---------- 脚本版本号 ----------
Q = '_md2docx.py'
s = io.open(Q, encoding='utf-8').read()
assert s.count('v2.74') == 3, s.count('v2.74')
io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace('v2.74', 'v2.75'))
print('脚本版本号 OK')

# ---------- 先复制旧版入历史，再改名升版 ----------
hist = '历史版本/设定集各版/'
md_old = '天神下凡设定集_归纳整理版_v2.74.md'
md_new = '天神下凡设定集_归纳整理版_v2.75.md'
doc_old = '天神下凡设定集_归纳整理版_v2.74.docx'
assert not os.path.exists(hist + md_old), '历史版本已有 v2.74.md，勿覆盖'
assert not os.path.exists(hist + doc_old), '历史版本已有 v2.74.docx，勿覆盖'
shutil.copy2(md_old, hist + md_old)
shutil.move(doc_old, hist + doc_old)
os.rename(md_old, md_new)
print('升版 OK：', md_new)
