# -*- coding: utf-8 -*-
import io, os, shutil

MD = '天神下凡设定集_归纳整理版_v2.76.md'

# ---------- 1. 主稿头部戳（v2.76 曾漏改，本轮务必改对） ----------
L = io.open(MD, encoding='utf-8').read().split('\n')
assert 'v2.76' in L[3] and 'v2.76' in L[5], (L[3][:80], L[5][:80])
L[3] = L[3].replace('**v2.76**', '**v2.77**')
L[5] = L[5].replace('v2.76', 'v2.77')
io.open(MD, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('主稿头部戳 OK：L4/L6 → v2.77')

# ---------- 2. 说明集 ----------
S = '天神下凡设定集版本更新说明集.md'
L = io.open(S, encoding='utf-8').read().split('\n')
old = [l for l in L if l.startswith('> **现行版本**：')]
assert len(old) == 1
L[L.index(old[0])] = (
    '> **现行版本**：**v2.77**｜2026-11-24（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.77.md`'
    '｜**本版一事**：**白阿育王归属通则**（用户裁定「只能是牧首宠物，上任牧首死亡过继给下任牧首，所以不冲突」）'
    '——作废 v2.76「时点差不并写」之规避，改定六处为**牧首专属·随任过继**，'
    '咬合拿破仑＝未来牧首，加固黑／白两猫分明。（v2.76 戳依次下移。）'
)
assert L[10] == '## 一、版本戳（最新在上 · v2.76 → v1.0）', L[10][:80]
L[10] = '## 一、版本戳（最新在上 · v2.77 → v1.0）'
stamp = (
    '> 更新时间戳：2026-11-24（GMT+8）｜**v2.77**｜**第一百一十六轮：白阿育王归属通则**'
    '——用户插一嘴裁定：「白阿育王只能是**牧首宠物**，**上任牧首死亡过继给下任牧首**，所以不冲突」。'
    '**关键咬合**：主稿 §3.15 已载用户裁定「拿破仑＝**未来牧首**」，故旧「现属拿破仑」本即「牧首宠物」的另一种说法，'
    'v2.76 判为「时点差、不并写为同一刻」属**多余规避**，本轮作废。'
    '改定六处：§8.4 主行、v2.76 补注归属行与防误判②、v2.19 防误判②、§3.1 #10、§3.5 终局行——'
    '统一为**牧首专属、上任死→过继下任、一脉单传**；新增 §8.4 **v2.77 通则块**，立三条边界'
    '（黑／红阿育王不受此限；苏卡娜误认黑猫为白猫被**加固**；过继＝所有权随职转移、不推死亡时点）。'
    'md 21,758 行／3,420,571 B／裸 LF 0；四件套全绿。'
)
assert L[12].startswith('> 更新时间戳：') and 'v2.76' in L[12]
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
assert 'v2.76' in old_cur and 'v2.75' in old_prev and 'v2.74' in old_preprev

new_cur = (
    '| **当前版本** | 本机 **v2.77**（第一百一十六轮·**白阿育王归属通则**：用户裁定「只能是牧首宠物，'
    '上任牧首死亡过继给下任牧首，所以不冲突」——作废 v2.76「时点差不并写」之规避，'
    '改定六处为**牧首专属·随任过继**，咬合拿破仑＝未来牧首〔§3.15〕，'
    '新增 §8.4 v2.77 通则块立三条边界。md 21,758 行／3,420,571 B／裸 LF 0） | 2026-11-24 |'
)
new_detail = (
    '| **v2.77 白阿育王归属落地** | 用户裁定：白阿育王**只属牧首**，**上任牧首死亡→过继下任**，一脉单传。'
    '旧判「现属拿破仑 vs 这一任牧首有一头＝时点差、不并写」**作废**——拿破仑已由用户裁定为**未来牧首**，'
    '两处表述本是同一过继链。改定：§8.4 主行／v2.76 补注归属行与防误判②／v2.19 防误判②／§3.1 #10／§3.5 终局行；'
    '新增 §8.4 v2.77 通则块（黑／红阿育王不受限、苏卡娜误认被加固、过继不推死亡时点）。 | 2026-11-24 |'
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
assert s.count('v2.76') == 3, s.count('v2.76')
io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace('v2.76', 'v2.77'))
print('脚本版本号 OK')

# ---------- 5. 升版：先复制旧版入历史，再改名 ----------
hist = '历史版本/设定集各版/'
md_old, md_new = '天神下凡设定集_归纳整理版_v2.76.md', '天神下凡设定集_归纳整理版_v2.77.md'
doc_old = '天神下凡设定集_归纳整理版_v2.76.docx'
assert not os.path.exists(hist + md_old) and not os.path.exists(hist + doc_old)
shutil.copy2(md_old, hist + md_old)
shutil.move(doc_old, hist + doc_old)
os.rename(md_old, md_new)
print('升版 OK：', md_new)
