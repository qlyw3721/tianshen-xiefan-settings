# -*- coding: utf-8 -*-
import io, shutil, os
BASE = 'E:/天神下凡/'
NL = '\r\n'
def load(p): return io.open(p, encoding='utf-8').read().split('\n')
def save(p, lines):
    io.open(p, 'w', encoding='utf-8', newline='').write(NL.join(lines))
    raw = open(p, 'rb').read()
    assert raw.count(b'\n') == raw.count(b'\r\n'), ('naked LF', p)

# ---- 1. 说明集现行版本戳 ----
P = BASE + '天神下凡设定集版本更新说明集.md'
L = load(P)
old = [i for i, l in enumerate(L) if l.startswith('> **现行版本**：')]
assert len(old) == 1
L[old[0]] = ('> **现行版本**：**v2.87**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.87.md`｜**本版二事**：① **核心不变·九区不变·'
             '盖穆位置暂定待裁**——用户令部分回退 v2.86，改名换主整体挂起、恢复前传 L1477 '
             '「牧首兼朱庇特城和中央大教区主教」原文核心，v2.38「中央≠中部不并」恢复、'
             '八红衣维持原制；② **巫婆「促狭」伏笔**——唯独对主角露出俏皮一面（原文），'
             '用户推测其对主角不同、为「征服巫婆」假设之前提（她的默认），标【用户推测·大胆假设】'
             '不排产。§7.1 新增 v2.87 裁定块、§1.7 剧情篇新增「三之二」补注块。（v2.86 戳依次下移。）')
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

newcur = ('| **当前版本** | 本机 **v2.87**（第一百二十六轮·**核心不变·九区不变·盖穆位置暂定待裁'
          '＋巫婆「促狭」伏笔**）：用户裁「牧首兼朱庇特城和中央大教区主教核心不变，九大教区不变，'
          '盖穆的位置暂定，留待以后裁定」——**部分回退 v2.86**：改名换主整体挂起、恢复前传 L1477 '
          '原文核心（九区第 1 席＝中央教区／牧首柏拉图斯鸠兼领、不设红衣）；v2.38「中央≠中部不并」'
          '恢复、八红衣维持原制；盖穆（中部教区·后传 L44 身份原文级）位置暂定待裁、不入九区表。'
          '另用户补巫婆「促狭唯独对主角」→推测其对主角不同→「征服巫婆」假设之前提（她的默认），'
          '标【用户推测·大胆假设】不排产。md 22,474 行／3,550,916 B／裸 LF 0） | 本轮 |')
detail = ('| **v2.87 落地** | 用户裁定一：§7.1 v2.86 裁定块**整体挂起留档**；九区表第 1 席回退'
          '「中央教区／牧首兼领」（v2.81 历史表行、v2.84 表行、§7.1 主线诸处同步标挂起/恢复）；'
          'v2.38「中央≠中部不并」恢复有效、v2.86 作废标注撤销；八红衣维持原制、张力消解；'
          '新增 §7.1 v2.87 裁定块（回退表＋现行九区表＋连带处置＋五条防误判）。用户裁定二：'
          '§1.7 剧情篇新增「三之二」补注块（冷漠为常／促狭为例外／例外只对一人／征服伏笔四环节表'
          '＋与既有三线互见＋五条纪律），层级标【用户推测·大胆假设】、不排产、不写 txt 行号。 | 本轮 |')

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
