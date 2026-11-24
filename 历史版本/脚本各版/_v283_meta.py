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

# ---- 1. 说明集：现行版本戳改为 v2.83 ----
P = BASE + '天神下凡设定集版本更新说明集.md'
L = load(P)
old = [i for i, l in enumerate(L) if l.startswith('> **现行版本**：')]
assert len(old) == 1, ('ex-version', len(old))
L[old[0]] = ('> **现行版本**：**v2.83**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.83.md`｜**本版一事**：**十大神学院席位替换结案**——'
             '用户答「替换」（不扩容）：波克斯替索尔邦入第 9 席、纽芬兰替圣卡洛尔入第 10 席，'
             '两校本体不删；十席表收录说明／边界4／v2.82 待裁行同步标注结案，新增 v2.83 '
             '替换对位表＋四条边界。（v2.82 戳依次下移。）')
save(P, L)

# ---- 2. 台账：四行滚动 ----
P = BASE + '设定集_裁定台账.md'
L = load(P)
idx = {}
for i, l in enumerate(L):
    for key in ('**当前版本**', '**上一版**', '**上上版**', '**历史版**'):
        if l.startswith('| ' + key + ' |'):
            idx.setdefault(key, []).append(i)
idx = {k: v[:1] for k, v in idx.items()}
assert all(k in idx and len(idx[k]) == 1 for k in ('**当前版本**', '**上一版**', '**上上版**', '**历史版**'))
cur = L[idx['**当前版本**'][0]]
prev = L[idx['**上一版**'][0]]
prevprev = L[idx['**上上版**'][0]]

newcur = ('| **当前版本** | 本机 **v2.83**（第一百二十二轮·**十大神学院席位替换结案**：'
          '用户就 v2.82 所留「二校替换还是扩容」之问答「**替换**」——不扩容，十席仍十席，'
          '按交付段登记顺序相邻对位：波克斯入第 9 席（原索尔邦【原创】）、纽芬兰入第 10 席（原圣卡洛尔）；'
          '两校本体不删，只退出神学院十席。十席表第 9／10 行、收录说明、边界4、v2.82 待裁行同步结案，'
          '新增 §1.4 v2.83 替换对位表＋四条边界。md 22,198 行／3,509,125 B／裸 LF 0） | 本轮 |')
detail = ('| **v2.83 落地** | 用户裁「替换」：§1.4 十席表第 9 席索尔邦→**波克斯神学院**、'
          '第 10 席圣卡洛尔→**纽芬兰神学院**（皆【用户交付·原文补充·用户裁定】，非 AI 原创、不冒充原文级）；'
          '原两校本体保留（索尔邦见 §1.5.11、圣卡洛尔见 §1.4 建筑表／§3.13 塔科·苔莉思条）；'
          '收录说明改「二校补入、原创席退出」、边界4 改「第 9／10 席经裁定补入」、'
          'v2.82「待裁」行标结案存照；新增 §1.4 v2.83 裁定块（对位表＋四条边界：替换席位非机构／不扩容／'
          '序号不等于强弱／层级不升级）。 | 本轮 |')

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

mirror = 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md'
if os.path.exists(os.path.dirname(mirror)):
    shutil.copy2(P, mirror)
    print('mirror synced')
else:
    print('mirror dir missing, skipped')

print('meta OK: 说明集 %d 行, 台账 %d 行' % (len(load(BASE + '天神下凡设定集版本更新说明集.md')), len(out)))
