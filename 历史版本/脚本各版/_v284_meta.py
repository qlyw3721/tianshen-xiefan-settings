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
L[old[0]] = ('> **现行版本**：**v2.84**｜2026-11-24（GMT+8）｜对应设定集 '
             '`天神下凡设定集_归纳整理版_v2.84.md`｜**本版一事**：**巫婆对话世界观大块＋九区更正**——'
             '用户交付脉代奥拉重逢整段，逐字解读（占星师最稀少／偷窥命运的小偷／伟大先知＝命运傀儡／'
             '各国占星师分布 0·3·2·7／两廷选举伊拉斯谟改制／迦卡妙女魔法师 vs 疯子伏笔／'
             '欧内特×尤里乌斯二重复合魔法阵），第 11 条定「巫婆见面暂定三次」；第 10 条更正九区：'
             '西南威尔森、东南尼科洛（不合并）、柏拉图斯鸠升新牧首，v2.41／v2.81 旧判留档作废。'
             '（v2.83 戳依次下移。）')
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

newcur = ('| **当前版本** | 本机 **v2.84**（第一百二十三轮·**巫婆对话世界观＋九区更正**：'
          '用户交付脉代奥拉重逢整段＋11 条，本机两 txt／两 epub 特征句零命中→标【用户交付·原文补充】不写行号。'
          '① 剧情篇 #12 逐字解读（承 v1.76 #11 五维纪律）：巫婆冷漠标签／主角「臣服与征服泥潭」情感／'
          '占星师「最稀少·孤僻·手持命运之轮」与「偷窥命运的小偷·伟大先知＝命运傀儡·堕炼狱」／'
          '各国占星师分布（卡妙 0／帝国 3／泰坦尼古拉七世 2／白蔷薇 7）／两廷选举（四世俗君主→伊拉斯谟改制→'
          '否决权百年阴谋）／迦卡妙女魔法师 vs 大精神病患者伏笔／信仰问答；② 第 10 条更正九区：'
          '西南威尔森、东南尼科洛不合并、柏拉图斯鸠升新牧首，v2.41「东南并入东部」与 v2.81「西南＝柏拉图斯鸠」'
          '留档作废，中部教区（盖穆）去留待裁；③ 欧内特圆环×尤里乌斯风洞二重复合魔法阵。'
          'md 22,320 行／3,531,174 B／裸 LF 0） | 本轮 |')
detail = ('| **v2.84 落地** | 用户交付＋裁定：§1.7 剧情篇 #12 v2.84 大块（逐字 15 条＋五维解读＋羁绊归位＋'
          '占星师职业与命运观表＋两廷选举表＋五条防误判，定句「占星师是偷看命运的小偷，看见了也不能动手——'
          '所以她只说，不救」）；§7.1 v2.84 九区更正块（三处更正表＋新九区八席表＋新牧首接线＋五条防误判，'
          '旧判逐处标作废、全文留档）；§5.2 v2.84 欧内特×尤里乌斯二重复合魔法阵补登。'
          '达拉贡黑水晶球／龙骸眼镜／尼古拉七世／玛格丽特嫩羊肉面包皆登记不建传。 | 本轮 |')

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
