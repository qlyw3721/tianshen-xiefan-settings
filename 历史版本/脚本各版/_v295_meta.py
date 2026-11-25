# -*- coding: utf-8 -*-
import io

def load(p):
    b = io.open(p, 'rb').read().decode('utf-8')
    return b.split('\r\n') if '\r\n' in b else b.split('\n')

def save(p, lines):
    io.open(p, 'w', encoding='utf-8', newline='').write('\r\n'.join(lines))

# ---- 说明集 ----
p = '天神下凡设定集版本更新说明集.md'
t = load(p)
idx = [i for i, l in enumerate(t) if l.startswith('> **现行版本**：')]
assert len(idx) >= 1, 'notes current version'
i = idx[0]
assert 'v2.94' in t[i], t[i][:100]
t[i] = t[i].replace('v2.94', 'v2.95', 1).replace('3,632,949 B', '3,649,052 B', 1)
reg = '> **v2.95 登记**：《天神下凡》第1章「第四巨头」整编（原文 L16–L125 全命中，本机 txt 可写行号）：用户分析 docx 14 栏整编＋【AI 补】查漏补缺 12 项（百花廊＝家族徽章集合／黄金怀表／《佛伦蒂大教典》／比萨主教与皇家专属教堂／盖穆保司祭身份／COSMO＝秩序等）；教廷权势前十表（1–5/7 用户裁定、6/8–10 原创可驳、两院＝国务院＋圣赦院核定）；830 年故事开端（主角 22 岁、建立秩序与父母绞死入大事件）；主角出场八法＋续写总纲同步进续写规则 v1.1。12 代 vs 14 代、8 部 vs 9 部两存待裁。'
t.insert(i + 1, reg)
save(p, t)
print('说明集 OK, 现行版本行', i + 1)

# ---- 台账 ----
p = '设定集_裁定台账.md'
t = load(p)
cur = [i for i, l in enumerate(t) if l.startswith('| **当前版本** |')]
assert len(cur) >= 1, 'ledger current'
i = cur[0]
assert 'v2.94' in t[i], t[i][:100]
t[i] = ('| **当前版本** | v2.95 | 2026-11-25 | 《天神下凡》第1章整编：分析文档归位＋查漏补缺＋教廷权势前十表＋830 年开端锚（主角 22 岁）；续写规则 v1.1 增补 | 23,179 行／3,649,052 B |')
# 上一版行（取第一条）
prev = [j for j, l in enumerate(t) if l.startswith('| **上一版** |')]
assert len(prev) >= 1, 'ledger prev'
j = prev[0]
t[j] = ('| **上一版** | 本机 **v2.94**（第一百三十五轮·时间线重锚 808 生／821 发布／827 五事件 19 岁／841 终局 33 岁）——本版升 v2.95，v2.94 md／docx 哈希核对一致后归档。 |')
save(p, t)
print('台账 OK, 当前', i + 1, '上一版', j + 1)
