# -*- coding: utf-8 -*-
import io

def load(p):
    b = io.open(p, 'r', encoding='utf-8', newline='').read()
    return b, b.split('\r\n')

def save(p, lines):
    out = '\r\n'.join(lines)
    assert '\n' not in out.replace('\r\n', '')
    io.open(p, 'w', encoding='utf-8', newline='').write(out)
    return out

# ---------- 说明集 ----------
P = '天神下凡设定集版本更新说明集.md'
_, L = load(P)
def rep1(lines, old, new, tag):
    idx = [i for i, l in enumerate(lines) if old in l]
    assert len(idx) == 1, (tag, len(idx))
    lines[idx[0]] = lines[idx[0]].replace(old, new)

rep1(L, '**现行版本**：**v2.95**｜2026-11-25（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.95.md`｜**本版一事**：《天神下凡》第1章「第四巨头」整编（分析文档归位＋查漏补缺 12 项＋教廷权势前十表＋830 年开端锚）；续写规则 v1.1 增补主角出场八法',
     '**现行版本**：**v2.96**｜2026-11-25（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.96.md`｜**本版一事**：《宗教裁判所》第1章「平庸的继承人」分析查漏补缺（重复项忽略／确缺 7 项补入／拿不准 5 项交裁定）',
     'cur_ver')

anchor = '> **v2.95 登记**：'
idx = [i for i, l in enumerate(L) if l.startswith(anchor)]
assert len(idx) == 1, ('v295 reg', len(idx))
new_reg = ('> **v2.96 登记**：《宗教裁判所》第1章「平庸的继承人」分析 docx（13 节）查漏补缺，原文 L1–L45 逐条回核、sha `351bf2163181bdb8` 未变。'
           '① 重复项 13 组已归位忽略（公爵 L6／L26、母亲全名与随夫姓 L28、康费双极 L29、史诗大陆十家族、主角平庸 L30、黑袍女人外貌 L3–L15、年龄错觉 L12–L13、五芒星 L21、三封印 L15–L16、绝密手札 L44–L45、顺位继承人 L26、父母结局与代数冲突、公爵四不）；'
           '② 确缺 7 项补入（抓周择物四物 L33／母亲黄金向日葵笑 L41／古怪强悍逻辑 L32／期许金句 L41／黑袍藏獒式兴趣 L22／主角前世判词 L11·L25·L27 存照不入正典／术与魔法并列 L29·L33）；'
           '③ 拿不准 5 项交裁定（P005 黑袍女人是否＝海姬、P006 母亲下落是否维持 830、P007 老管家、P008 穿越是否入设定维持正典、代数 12/14 已挂起不重裁）。'
           '前传 P8（L1–L500）尚待梳理，本块为先行补注、不改写既有词条原行；分析文档推断不冒充原文，前世参照系按 §15 删除穿越正典存照不入正典。')
L.insert(idx[0], new_reg)
save(P, L)
print('说明集 updated, lines', len(L))

# ---------- 台账（取第一条当前/上一版） ----------
P2 = '设定集_裁定台账.md'
_, L2 = load(P2)
ci = [i for i, l in enumerate(L2) if l.startswith('| **当前版本** |')]
pi = [i for i, l in enumerate(L2) if l.startswith('| **上一版** |')]
assert ci and pi, ('ledger rows', len(ci), len(pi))
c, p = ci[0], pi[0]
L2[c] = '| **当前版本** | v2.96 | 2026-11-25 | 《宗教裁判所》第1章分析查漏补缺：重复13组忽略／确缺7项补入／拿不准5项交裁定；前传P8先行补注 | 23,226 行／3,656,999 B |'
L2[p] = ('| **上一版** | 本机 **v2.95**（第一百三十六轮·《天神下凡》第1章「第四巨头」整编：分析文档归位＋查漏补缺 12 项＋教廷权势前十表＋830 年开端锚，续写规则 v1.1 增补主角出场八法）——本版升 v2.96，v2.95 md／docx 哈希核对一致后归档。 |')
save(P2, L2)
print('台账 updated')
