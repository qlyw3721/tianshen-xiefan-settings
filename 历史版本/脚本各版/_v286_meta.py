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

# ---- 1. 说明集现行版本戳 ----
P = BASE + '天神下凡设定集版本更新说明集.md'
L = load(P)
old = [i for i, l in enumerate(L) if l.startswith('> **现行版本**：')]
assert len(old) == 1
L[old[0]] = ('> **现行版本**：**v2.86**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.86.md`｜**本版一事**：**中央教区改名中部大教区、'
             '红衣盖穆执掌**（用户裁定）——消解 v2.84「中部去留待裁」留白，并推翻 v2.38 '
             '「中央≠中部两席不并」旧判；§7.1 就地改判九区第 1 席＋新增 v2.86 裁定块'
             '（改名换主表＋三项连带判定＋九区现状表＋「九区八红衣」新张力待裁＋五条防误判）。'
             '牧首柏拉图斯鸠退出该席（仍为新牧首）；前传 L1477 原文留档不回改。（v2.85 戳依次下移。）')
save(P, L)

# ---- 2. 台账四行滚动 ----
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

newcur = ('| **当前版本** | 本机 **v2.86**（第一百二十五轮·**中央教区改名中部大教区、'
          '红衣盖穆执掌**：用户裁「中央教区改为中部大教区，负责人盖穆」。后传 L44「执掌中部教区的'
          '红衣大主教盖穆」原文级锚——九区第 1 席由「中央教区／牧首柏拉图斯鸠兼领、不设红衣」'
          '就地改为「**中部大教区／盖穆（红衣）**」；v2.38「中央≠中部两席不并」判作废、'
          'v2.84「中部去留待裁」结案；牧首退出该席（仍为新牧首）；前传 L1477 原文留档不回改；'
          '「九区八红衣」算术新张力标待裁、不擅改红衣总数。md 22,405 行／3,541,422 B／裸 LF 0） | 本轮 |')
detail = ('| **v2.86 落地** | 用户裁定：§7.1 九区表第 1 席就地改判（中央教区→**中部大教区**、'
          '掌者牧首兼领→**红衣盖穆**）；v2.84 八红衣注／防误判②／柏拉图斯鸠行加 v2.86 结案或张力注；'
          'v2.81 历史表第 1 席、v2.38 登记③、§7.1「一处须辨」「不合并」、防误判④等旧判标作废留档；'
          '新增 §7.1 v2.86 裁定块（改名换主表＋三项连带判定＋九区现状表＋八红衣新张力待裁＋'
          '五条防误判＋定句「名字从中央改成中部，椅子从牧首换成盖穆」）。九区现状：中部盖穆／'
          '东部摩诺法蒂／南部葛吕泽／西北伊耶塔／北部圣本尼第／西南威尔森／东南尼科洛／西部·东北仍空；'
          '在库红衣七位。红衣编制总数（原文八位）与中部设红衣之张力待用户裁定。 | 本轮 |')

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
print('meta OK: 说明集 %d 行, 台账 %d 行' % (len(load(BASE + '天神下凡设定集版本更新说明集.md')), len(out)))
