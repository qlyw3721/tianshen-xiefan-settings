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
L[old[0]] = ('> **现行版本**：**v2.85**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.85.md`｜**本版一事**：**两条裁定结案**——'
             '① **白蔷薇皇朝与金雀花王朝是两个不同王朝**（用户裁定），消解 v2.84 留白②，'
             '§1.7 就地改判＋新增 v2.85 王朝辨正块（两王朝各为其朝、不互训、不合并）；'
             '② **葛吕泽继任柏拉图斯鸠南部大教区红衣**（用户裁定），消解 v2.84 留白③，'
             '§7.1 就地改判＋新增 v2.85 继任结案块（三段继任链）；v2.81「南部误书判」彻底作废、'
             '交付段「是南部的那位」确认为原文不误。（v2.84 戳依次下移。）')
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

newcur = ('| **当前版本** | 本机 **v2.85**（第一百二十四轮·**两条裁定结案**：用户裁「1. 列九大教区表 2. '
          '白蔷薇和金雀花是两个王朝 3. 葛吕泽是继任」。① 王朝辨正——白蔷薇皇朝≠金雀花王朝，'
          '两处「拜占奥教皇承认者」各为其朝、不互训、不合并，消解 §1.7 v2.84 留白②；'
          '② 继任结案——葛吕泽继任柏拉图斯鸠南部大教区红衣之位（柏拉图斯鸠由南部红衣升新牧首兼中央，'
          '腾出南部），消解 §7.1 v2.84 留白③，v2.81「南部误书（南部↔西南）」判彻底作废、'
          '交付段「是南部的那位」确认原文不误。md 22,355 行／3,535,093 B／裸 LF 0） | 本轮 |')
detail = ('| **v2.85 落地** | 用户裁定：§1.7 两廷选举表注就地改判（白蔷薇皇朝与金雀花王朝是两个不同王朝，'
          '旧「两称并列待裁定」结案作废）＋新增 v2.85 王朝辨正块（两王朝出处语境表＋三条边界＋'
          '定句「名字不同，王朝不同」）；§7.1 v2.84 防误判③就地改判（葛吕泽继任结案）＋v2.81 两解表'
          '与 v2.80 三席表补 v2.85 作废标注＋新增 v2.85 继任结案块（三段继任链表＋就地改判表＋'
          '三条边界＋定句「空出来的那把椅子，葛吕泽坐了」）。九区表本体未动（中央柏拉图斯鸠／'
          '东部摩诺法蒂／南部葛吕泽／西北伊耶塔／北部圣本尼第／西南威尔森／东南尼科洛／西部·东北仍空）；'
          '中部教区（盖穆）去留仍待裁。 | 本轮 |')

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
