# -*- coding: utf-8 -*-
import io

def rd(p):
    return io.open(p, 'rb').read().decode('utf-8').split('\r\n')
def wr(p, lines):
    io.open(p, 'w', encoding='utf-8', newline='').write('\r\n'.join(lines))

# ---------- 说明集 ----------
NP = '天神下凡设定集版本更新说明集.md'
n = rd(NP)

# 现行版本行
idx = [i for i, l in enumerate(n) if l.startswith('> **现行版本**：')]
assert len(idx) == 1, ('notes current', len(idx))
i = idx[0]
old = n[i]
n[i] = ('> **现行版本**：**v2.93**｜2026-11-25（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.93.md`'
        '｜**本版一事**：后传第四十四章「黑暗咏叹调前奏」主角青年时期收尾归位（23 项）＋五表归口使徒牌目录＋818 五事件后移 822。')
print('notes current:', n[i][:70])

# 在现行版本行后插入 v2.93 登记
reg = ('> **v2.93 登记**：后传「黑暗咏叹调前奏」整段标【用户交付·原文补充】（本机同章异文零命中）；23 项归位'
       '（拉伯德水晶厅／莱茵王圆桌骑士／普尔阀孜徽章／香布榭街／艾曼／浮克内拉／切司菲尔德／安德烈娅公主新立；'
       '隆美尔·庞培侯爵·彭龙纳·罗桐柴尔德补全；尼禄喜欢的人／克拉苏寡妇／卡妙私生子三伏笔；两条伊耶塔遗言名言）；'
       '三军团原创番号【可驳】（提尔之鞭／奥丁神眸／赫尔曼狼牙）；§4.7 使徒牌五表总汇；'
       '时间线 818→822（守 841-42 红线、主角 23 岁、守夜者 818 张力两存）。')
n.insert(i+1, reg)
print('notes reg inserted')

wr(NP, n)

# ---------- 台账 ----------
LP = '设定集_裁定台账.md'
t = rd(LP)

idxc = [i for i, l in enumerate(t) if l.startswith('| **当前版本** |')]
assert len(idxc) >= 1, 'no current'
ic = idxc[0]
t[ic] = ('| **当前版本** | v2.93 | 2026-11-25 | 后传第四十四章青年收尾23项归位＋使徒牌五表总汇'
         '＋818五事件后移822（守841-42红线） | 23,018 行／3,625,253 B |')
print('ledger current:', t[ic][:60])

idxp = [i for i, l in enumerate(t) if l.startswith('| **上一版** |')]
assert len(idxp) >= 1, 'no prev'
ip = idxp[0]
t[ip] = ('| **上一版** | 本机 **v2.92**（第一百三十二轮·**修正红桃牌误读**：红桃牌＝使徒红心战争花色非地名，'
         '赫尔曼狼群默认入红心十大军团）——本版升 v2.93，v2.92 md／docx 哈希核对一致后归档。 |')
print('ledger prev:', t[ip][:60])

wr(LP, t)
print('DONE')
