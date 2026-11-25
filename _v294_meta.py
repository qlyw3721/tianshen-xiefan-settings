# -*- coding: utf-8 -*-
import io
NOTES = '天神下凡设定集版本更新说明集.md'
LEDGER = '设定集_裁定台账.md'

def load(p):
    return io.open(p, 'rb').read().decode('utf-8').split('\r\n')
def save(p, lines):
    io.open(p, 'wb').write('\r\n'.join(lines).encode('utf-8'))
def first(lines, cond, tag):
    idx = [i for i, l in enumerate(lines) if cond(l)]
    assert idx, (tag, 'not found')
    return idx[0]

# ---- 说明集 ----
t = load(NOTES)
i = first(t, lambda l: l.startswith('> **现行版本**：'), 'notes-current')
t[i] = ('> **现行版本**：**v2.94**｜2026-11-25（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.94.md`｜'
        '**本版一事**：时间线重锚——主角生年 808／使徒牌发布 821／818 五事件顺推 827（主角 19 岁）／841 终局 33 岁；'
        '原文层年龄描述全部留档、明写两层口径分裂。')
ins = ('> **v2.94 登记**：用户裁定推翻旧锚（799 生／821 年 22 岁），小说层重锚 808 生／821 发布／827 五事件 19 岁／841 终局 33 岁。'
       '原文 L1924（812 发布）、L4289（821 最近一次）、L1584（812 快13岁）、L282（24岁）、L4253（约克22岁）等年龄描述一字不改、'
       '标为原文层异文；设定层以裁定为准，两层分裂显式化。§14.0／§14.3／§14.9／§0.6 第九款联动重锚，'
       'v1.88「22 岁定值」块加 v2.94 作废留痕注、原字不删；§3.16 v2.94 总裁定块立双锚点表＋两层口径分裂表＋13 项联动替换表＋6 条防误判。'
       '841 红线年份不动，仅年龄 42→33。')
# 插在现行版本行之后
t.insert(i + 1, ins)
save(NOTES, t)
print('说明集 OK: 现行版本+v2.94登记')

# ---- 台账 ----
l = load(LEDGER)
# 当前版本行（第一条）
i = first(l, lambda x: x.startswith('| **当前版本** |'), 'ledger-current')
l[i] = ('| **当前版本** | v2.94 | 2026-11-25 | 时间线重锚：808 生／821 使徒牌发布／818 五事件顺推 827（主角 19 岁）／841 终局 33 岁；'
        '原文层年龄留档、两层分裂显式化 | 23,078 行／3,632,949 B |')
# 上一版行（第一条）：改成描述 v2.93 → 本版
j = first(l, lambda x: x.startswith('| **上一版** |'), 'ledger-prev')
l[j] = ('| **上一版** | 本机 **v2.93**（第一百三十四轮·后传第四十四章青年收尾 23 项归位＋使徒牌五表总汇＋818 五事件后移 822）——'
        '本版升 v2.94，v2.93 md／docx 哈希核对一致后归档。 |')
save(LEDGER, l)
print('台账 OK: 当前版本+上一版')
