# -*- coding: utf-8 -*-
import io, shutil, os

BASE = 'E:/天神下凡/'
NL = '\r\n'

def load(p):
    return io.open(p, encoding='utf-8').read().split('\n')

def save(p, lines):
    io.open(p, 'w', encoding='utf-8', newline='').write(NL.join(lines))
    raw = open(p, 'rb').read()
    assert raw.count(b'\n') == raw.count(b'\r\n'), ('naked LF', p)

# ---- 1. 说明集：现行版本戳改为 v2.82，追加一行版本戳（顶部） ----
P = BASE + '天神下凡设定集版本更新说明集.md'
L = load(P)
old = [i for i, l in enumerate(L) if l.startswith('> **现行版本**：')]
assert len(old) == 1, ('ex-version', len(old))
L[old[0]] = ('> **现行版本**：**v2.82**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.82.md`｜**本版一事**：**牧首选举「第六日」段**——'
             '用户交付 13 条：烟规（白烟／黑烟）、青铜门外众生相（理查德亲王／儒贝尔侯爵／叔本华侧写／'
             '杜兰特×北奥武符／拉比三重身份）、名言 #166、主角爱情观三层（正妻一位·红颜知己数位·'
             '阿芙罗狄好感阶段）、庞培／克拉苏入九大古老家族、考夫曼教堂与波克斯／纽芬兰二校、'
             '德黑撒与拿破仑形象补录。（v2.81 戳依次下移。）')
save(P, L)

# ---- 2. 台账：四行滚动 ----
P = BASE + '设定集_裁定台账.md'
L = load(P)
idx = {}
for i, l in enumerate(L):
    for key in ('**当前版本**', '**上一版**', '**上上版**', '**历史版**'):
        if l.startswith('| ' + key + ' |'):
            idx.setdefault(key, []).append(i)
# 台账下方历史留档区亦有同名标签，滚动位只取每组第一条
idx = {k: v[:1] for k, v in idx.items()}
assert all(k in idx and len(idx[k]) == 1 for k in ('**当前版本**', '**上一版**', '**上上版**', '**历史版**'))
cur = L[idx['**当前版本**'][0]]
prev = L[idx['**上一版**'][0]]
prevprev = L[idx['**上上版**'][0]]
# 新当前行
newcur = ('| **当前版本** | 本机 **v2.82**（第一百二十一轮·**牧首选举「第六日」段**：'
          '用户交付一大段＋13 条标注，本机两 txt／两 epub 核心句零命中（「拥挤不堪」唯一命中系前传 '
          'L4071 教室、非同段），标【用户交付·原文补充】不写行号；唯拉比一线有后传 L5391–L5393 硬锚。'
          '① 烟规白烟／黑烟（§7.1 v2.82）；② 广场人物登记（理查德亲王／果雨儒贝尔侯爵／'
          '叔本华侧写／君士坦丁皇家魔法学院深造／杜兰特×北奥武符世代交好·政治婚姻·拉斐尔追阿芙罗狄）；'
          '③ 拉比三重身份＋帝国十大魔法师第十席落定；④ 名言 #166；⑤ 爱情观三层（正妻一位·'
          '红颜知己数位·好感不限）与阿芙罗狄追求主角＋拿破仑情敌；⑥ 庞培／克拉苏入九大古老家族；'
          '⑦ 考夫曼教堂（§1.4）＋波克斯／纽芬兰二校（十大席位冲突登记）；⑧ 德黑撒与拿破仑形象补录；'
          '⑨ 白阿育王认主时点。md 22,173 行／3,506,549 B／裸 LF 0） | 本轮 |')
# 新落地行
detail = ('| **v2.82 落地** | 用户交付牧首选举段＋13 条：§7.1 v2.82 烟规表（白烟＝新牧首／黑烟＝继续等待，'
          '「但」系「则」误字逐字留档）、广场人物表（信息不足者只登记不建传）、杜兰特×北奥武符世代交好、'
          '拉比三重身份表（后传 L5391–L5393 原文级）；§1.7 名言 #166（金字塔顶端碾碎美好）＋'
          '人物性格篇 #33（君士坦丁侧写叔本华）；§3.7 v2.82 爱情观三层（正妻一位不点名／红颜知己数位／'
          '好感不限）与阿芙罗狄现状（追求主角＋拿破仑情敌，不升正妻、不排产）；§1.2.3 v2.82 '
          '九大古老家族已定三名（罗桐柴尔德／庞培／克拉苏，余六家不填名，≠十大黄金家族）；'
          '§1.4 考夫曼教堂＋波克斯／纽芬兰二校（十席冲突不代删）；§3.13 德黑撒与拿破仑形象补录；'
          '§8.4 白阿育王认主时点；§9.3 十大魔法师第十席由拉比落定（v2.49「待用户指定」条件成立）。 | 本轮 |')
# 滚动：原当前→上一版，原上一版→上上版，原上上版→历史版（只换首列标签，内容不动）
def relabel(line, newtag):
    return line.replace('| ' + newtag.split('**')[1] + '** |', '| ' + newtag + ' |', 1) if False else line
# 直接按行重组：保留原行内容，仅改首列文字
def swap_tag(line, oldtag, newtag):
    assert line.startswith('| ' + oldtag + ' |'), (oldtag, line[:40])
    return '| ' + newtag + ' |' + line[len('| ' + oldtag + ' |'):]

newprev = swap_tag(cur, '**当前版本**', '**上一版**')
newprevprev = swap_tag(prev, '**上一版**', '**上上版**')
newhist = swap_tag(prevprev, '**上上版**', '**历史版**')

out = []
for i, l in enumerate(L):
    if i == idx['**当前版本**'][0]:
        out.append(newcur); out.append(detail)
    elif i == idx['**上一版**'][0]:
        out.append(newprev)
    elif i == idx['**上上版**'][0]:
        out.append(newprevprev)
    elif i == idx['**历史版**'][0]:
        out.append(newhist)
    else:
        out.append(l)
save(P, out)

# ---- 3. 镜像同步 ----
mirror = 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md'
if os.path.exists(os.path.dirname(mirror)):
    shutil.copy2(P, mirror)
    print('mirror synced')
else:
    print('mirror dir missing, skipped')

print('meta OK: 说明集 %d 行, 台账 %d 行' % (len(load(BASE + '天神下凡设定集版本更新说明集.md')), len(out)))
