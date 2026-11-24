# -*- coding: utf-8 -*-
import io, os, shutil

MD = '天神下凡设定集_归纳整理版_v2.77.md'

# ---------- 1. 主稿头部戳 ----------
L = io.open(MD, encoding='utf-8').read().split('\n')
assert 'v2.77' in L[3] and 'v2.77' in L[5], (L[3][:80], L[5][:80])
L[3] = L[3].replace('**v2.77**', '**v2.78**')
L[5] = L[5].replace('v2.77', 'v2.78')
io.open(MD, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('主稿头部戳 OK：v2.78')

# ---------- 2. 说明集 ----------
S = '天神下凡设定集版本更新说明集.md'
L = io.open(S, encoding='utf-8').read().split('\n')
old = [l for l in L if l.startswith('> **现行版本**：')]
assert len(old) == 1
L[L.index(old[0])] = (
    '> **现行版本**：**v2.78**｜2026-11-24（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.78.md`'
    '｜**本版一事**：**荷稣复活大教堂夜战段**（用户交付 · 原文补充，本机零命中不写行号）'
    '——敌基督坎舵瑟檀、西陀四继承人与钦察侯爵、三阵实战显形、名言 #154／#155、'
    '打斗笔法文风解构。（v2.77 戳依次下移。）'
)
assert L[10] == '## 一、版本戳（最新在上 · v2.77 → v1.0）', L[10][:80]
L[10] = '## 一、版本戳（最新在上 · v2.78 → v1.0）'
stamp = (
    '> 更新时间戳：2026-11-24（GMT+8）｜**v2.78**｜**第一百一十七轮：荷稣复活大教堂夜战段**'
    '——用户交付一大段教堂夜战原文＋八项标注，本机 epub／两 txt **零命中**（「坎舵瑟檀」「钦察」'
    '「奇猹琴」「珐特岛」「大地指纹」「处子血液」皆 0），全标【用户交付·原文补充】、**不写行号**。'
    '① **坎舵瑟檀**（§7.3 v2.78）：撒旦陆地化身「敌基督」，钉死圣人于骷髅地（**梵特兰蒂冈记载口径**），'
    '补 §1.4 受难像防误判③——凶手已给、**圣人名仍未点名**。'
    '② **西陀族谱系**（§8.1 v2.78）：皇族宠物／饲狼已在库只补细节——**四位继承人**、'
    '**亲王级长老沉睡 300 年·圣棺**，钦察为**最年轻侯爵**（≠罗素）；爵位与继承顺序两轴不并。'
    '③ **三阵**（§5.2 v2.78）：奇猹琴螺旋星座（红手套织物阵·末日审判图案）、'
    '珐特岛石头阵（17 土元素·瞬发·挡不穿狼人）、大地指纹（**金色水元素**防御阵·名含大地而质为水）。'
    '④ **名言 #154**（钦察「力量比处子血液更陶醉」·倒喻型）／**#155**（阿乐翰「太阳如金色蜘蛛」·预言型星象喻，'
    '§阿乐翰块补归属）。⑤ **打斗笔法**（§1.7 v2.78）：以静写烈、以物写杀，七法表；与 v2.76 侧写笔法分题材不互借。'
    '⑥ §3.7 A3.6 行迹补 ⑮（索菲亚夜战）。md 21,820 行／3,433,765 B／裸 LF 0；四件套全绿。'
)
assert L[12].startswith('> 更新时间戳：') and 'v2.77' in L[12]
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
assert 'v2.77' in old_cur and 'v2.76' in old_prev and 'v2.75' in old_preprev

new_cur = (
    '| **当前版本** | 本机 **v2.78**（第一百一十七轮·**荷稣复活大教堂夜战段**：用户交付整段，'
    '本机 epub／两 txt 零命中→全标【用户交付·原文补充】不写行号。'
    '① 坎舵瑟檀（敌基督·撒旦陆地化身·钉圣人于骷髅地，梵特兰蒂冈记载口径）；'
    '② 西陀四继承人／亲王沉睡 300 年／钦察最年轻侯爵（≠罗素）；'
    '③ 三阵（奇猹琴／珐特岛／大地指纹·水元素）；④ 名言 #154／#155；'
    '⑤ 打斗笔法七法表；⑥ A3.6 行迹 ⑮。md 21,820 行／3,433,765 B／裸 LF 0） | 2026-11-24 |'
)
new_detail = (
    '| **v2.78 夜战落地** | 用户交付教堂夜战段＋八项标注：§7.3 v2.78 坎舵瑟檀（与撒旦七化身／两颗黑暗种子'
    '并列不互训；§1.4 受难像防误判③改定：凶手已给、圣人名未给）；§8.1 v2.78 西陀谱系（四位继承人≠四位侯爵、'
    '亲王沉睡不写名不写成家主、钦察≠罗素、不代拟胜负）；§5.2 v2.78 三阵（大地指纹水元素不据名推土系、'
    '奇猹琴≠黑日王冠、17 土元素不写固定编制）；§1.7 名言 #154／#155＋打斗笔法七法表【文风解构·非强制规则】；'
    '§3.7 A3.6 行迹 ⑮；§阿乐翰块补遗言归属。 | 2026-11-24 |'
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
assert s.count('v2.77') == 3, s.count('v2.77')
io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace('v2.77', 'v2.78'))
print('脚本版本号 OK')

# ---------- 5. 升版：先复制旧版入历史，再改名 ----------
hist = '历史版本/设定集各版/'
md_old, md_new = '天神下凡设定集_归纳整理版_v2.77.md', '天神下凡设定集_归纳整理版_v2.78.md'
doc_old = '天神下凡设定集_归纳整理版_v2.77.docx'
assert not os.path.exists(hist + md_old) and not os.path.exists(hist + doc_old)
shutil.copy2(md_old, hist + md_old)
shutil.move(doc_old, hist + doc_old)
os.rename(md_old, md_new)
print('升版 OK：', md_new)
