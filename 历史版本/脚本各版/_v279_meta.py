# -*- coding: utf-8 -*-
import io, os, shutil

MD = '天神下凡设定集_归纳整理版_v2.78.md'

# ---------- 1. 主稿头部戳 ----------
L = io.open(MD, encoding='utf-8').read().split('\n')
assert 'v2.78' in L[3] and 'v2.78' in L[5], (L[3][:80], L[5][:80])
L[3] = L[3].replace('**v2.78**', '**v2.79**')
L[5] = L[5].replace('v2.78', 'v2.79')
io.open(MD, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('主稿头部戳 OK：v2.79')

# ---------- 2. 说明集 ----------
S = '天神下凡设定集版本更新说明集.md'
L = io.open(S, encoding='utf-8').read().split('\n')
old = [l for l in L if l.startswith('> **现行版本**：')]
assert len(old) == 1
L[L.index(old[0])] = (
    '> **现行版本**：**v2.79**｜2026-11-24（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.79.md`'
    '｜**本版一事**：**镜厅近景＋临摹段**（用户交付 · 原文补充，本机零命中不写行号）'
    '——名言 #156–#161、两种文风解构（极限拉扯／所爱者受伤的愤怒表达）、'
    '卜列颠明六大教团补五、两廷互派布道、魔法难题三术语、婆罗白头鹰、约克送鹰折服。'
    '（v2.78 戳依次下移。）'
)
assert L[10] == '## 一、版本戳（最新在上 · v2.78 → v1.0）', L[10][:80]
L[10] = '## 一、版本戳（最新在上 · v2.79 → v1.0）'
stamp = (
    '> 更新时间戳：2026-11-24（GMT+8）｜**v2.79**｜**第一百一十八轮：镜厅近景与临摹段**'
    '——用户交付一大段后续原文＋十四项标注，本机 epub／两 txt **零命中**'
    '（「黑暗使徒」「六大教团」「马费伦敦」「婆罗白头鹰」「从女人背后」皆 0），'
    '全标【用户交付·原文补充】、**不写行号**。'
    '① **名言 #156–#161**：伊甸裁决／奥古斯丁「婚姻基石」（面具型）／苏卡娜「痛苦的舞蹈」／'
    '主角「从女人背后到众生之上」（志向伏笔）／命运女神／小牛肉（叙述者语·与 §3.14 九闭环）。'
    '② **两种文风解构**（§1.7 v2.79 甲乙）：男女极限拉扯六法表、「不写怒写志向」五法表，'
    '【文风解构·非强制规则】。'
    '③ **六大教团补五**（§7.1 v2.79）：用户点名补齐，五席皆【原创·可驳】、'
    '西幻命名不搬现实名；卜列颠明为「入世＋暗线」那一席。'
    '④ **两廷互派布道＋黑暗使徒对位**（§7.1 v2.79）：与 v2.61 防误判⑤互证，'
    '「头等大敌不妨碍彼此布道」；切割者＝出场那一使徒。'
    '⑤ **镜厅数字核对**（§1.4 v2.79）：13／13／17 与 v2.55 相合，段作「13 扇」不改表。'
    '⑥ **魔法难题三术语＋檀伽玛星相**（§5.2 v2.79）：四色／哥尼斯堡 13 迷宫，'
    '名近≠同物、不援现实解法。'
    '⑦ **第七条准则**（§3.1.1）：志向挂在准则④上，不写加冕称帝。'
    '⑧ **婆罗白头鹰**（§8.5 v2.79）＋**约克送鹰折服**（§3.14 十一）。'
    'md 21,956 行／3,461,545 B／裸 LF 0；四件套全绿。'
)
assert L[12].startswith('> 更新时间戳：') and 'v2.78' in L[12]
L.insert(12, stamp)
io.open(S, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('说明集 OK', len(L))

# ---------- 3. 台账 ----------
T = '设定集_裁定台账.md'
M = io.open(T, encoding='utf-8').read().split('\n')
ci = [i for i, l in enumerate(M) if l.startswith('| **当前版本** |')]
pi = [i for i, l in enumerate(M) if l.startswith('| **上一版** |')]
ppi = [i for i, l in enumerate(M) if l.startswith('| **上上版** |')]
assert len(ci) == 1 and pi and ppi
ci0, pi0, ppi0 = ci[0], pi[0], ppi[0]
old_cur, old_prev, old_preprev = M[ci0], M[pi0], M[ppi0]
assert 'v2.78' in old_cur and 'v2.77' in old_prev and 'v2.76' in old_preprev, (old_cur[:80], old_prev[:80], old_preprev[:80])

new_cur = (
    '| **当前版本** | 本机 **v2.79**（第一百一十八轮·**镜厅近景与临摹段**：用户交付整段，'
    '本机 epub／两 txt 零命中→全标【用户交付·原文补充】不写行号。'
    '① 名言 #156–#161（含主角志向伏笔「从女人背后到众生之上」）；'
    '② 两种文风解构（极限拉扯六法／所爱者受伤的愤怒五法）；'
    '③ 六大教团补五【原创·可驳】；④ 两廷互派布道＋黑暗使徒对位；'
    '⑤ 镜厅 13／13／17 数字核对；⑥ 魔法难题三术语＋檀伽玛星相；'
    '⑦ §3.1.1 第七条准则；⑧ 婆罗白头鹰＋约克送鹰折服。'
    'md 21,956 行／3,461,545 B／裸 LF 0） | 2026-11-24 |'
)
new_detail = (
    '| **v2.79 临摹落地** | 用户交付镜厅近景段＋十四项标注：§1.7 名言 #156–#161'
    '（#159 志向伏笔挂 §3.1.1 准则④、#157 面具型反讽、#160／#161 叙述者语只用于叙述层）；'
    '§1.7 v2.79 文风解构甲乙（拉扯笔法六法、「不写怒写志向」五法，分题材不互借）；'
    '§7.1 v2.79 六大教团补五（五席原创可驳，不与两院六部／三大直属武装混轴）；'
    '§7.1 v2.79 两廷互派布道（头等大敌不妨碍布道）＋黑暗使徒对位（≠守夜者同一机构）；'
    '§1.4 v2.79 镜厅 13／13／17（段作「13 扇」不改表）；'
    '§5.2 v2.79 魔法难题（四色／哥尼斯堡 13 不援现实解法）；'
    '§3.1.1 第七条；§8.5 婆罗白头鹰（不套 2 级）；§3.14 十一约克送鹰折服。 | 2026-11-24 |'
)
new_prev = old_cur.replace('**当前版本**', '**上一版**', 1)
M[ci0] = new_cur
M.insert(ci0 + 1, new_detail)
M.insert(ci0 + 2, new_prev)
M[pi0 + 2] = old_prev.replace('**上一版**', '**上上版**', 1)
M[ppi0 + 2] = old_preprev.replace('**上上版**', '**历史版**', 1)
txt = '\r\n'.join(M)
io.open(T, 'w', encoding='utf-8', newline='').write(txt)
mirror = 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md'
if os.path.exists(os.path.dirname(mirror)):
    io.open(mirror, 'w', encoding='utf-8', newline='').write(txt)
    print('台账镜像 OK')
print('台账 OK', len(M))

# ---------- 4. 脚本版本号 ----------
Q = '_md2docx.py'
s = io.open(Q, encoding='utf-8').read()
assert s.count('v2.78') == 3, s.count('v2.78')
io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace('v2.78', 'v2.79'))
print('脚本版本号 OK')

# ---------- 5. 升版：先复制旧版入历史，再改名 ----------
hist = '历史版本/设定集各版/'
md_old, md_new = '天神下凡设定集_归纳整理版_v2.78.md', '天神下凡设定集_归纳整理版_v2.79.md'
doc_old = '天神下凡设定集_归纳整理版_v2.78.docx'
assert not os.path.exists(hist + md_old) and not os.path.exists(hist + doc_old)
shutil.copy2(md_old, hist + md_old)
shutil.move(doc_old, hist + doc_old)
os.rename(md_old, md_new)
print('升版 OK：', md_new)
