# -*- coding: utf-8 -*-
import io

BASE = 'E:/天神下凡/'

def load(p):
    b = io.open(p, 'r', encoding='utf-8', newline='').read()
    return b.split('\r\n')

def save(p, lines):
    out = '\r\n'.join(lines)
    assert '\n' not in out.replace('\r\n', ''), ('bare LF', p)
    io.open(p, 'w', encoding='utf-8', newline='').write(out)

def rep1(lines, old, new, tag):
    idx = [i for i, l in enumerate(lines) if old in l]
    assert len(idx) == 1, (tag, len(idx))
    lines[idx[0]] = lines[idx[0]].replace(old, new)

def rep_start(lines, prefix, new_full, tag, first=False):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert idx, (tag, 'none')
    lines[idx[0] if first else idx[-1]] = new_full

# ---------- 说明集 ----------
P = BASE + '天神下凡设定集版本更新说明集.md'
L = load(P)
rep_start(L, '> **现行版本**：**v2.96**',
    '> **现行版本**：**v2.97**｜2026-11-25（GMT+8）｜对应设定集 `天神下凡设定集_归纳整理版_v2.97.md`｜**本版一事**：《宗教裁判所》第1章拿不准 4 项裁定结案（黑袍＝巫婆／殉情／不解释／穿越不入设定）；v2.96 拿不准表状态回填、防误判同步改写',
    'cur_ver')
idx = [i for i, l in enumerate(L) if l.startswith('> **v2.96 登记**：')]
assert len(idx) == 1, ('v296 reg', len(idx))
new_reg = ('> **v2.97 登记**：用户 2026-11-25 就 v2.96 拿不准表 P005–P008 逐条裁定：'
           '① **黑袍为巫婆**——第1章黑袍女人＝巫婆＝圣阿尔忒弥斯（§3.1 #1；长期规则「设定层巫婆特指圣阿尔忒弥斯」），分析方「疑＝海姬」否决，海姬（§1.2.3.1）不并同，L22「藏獒欣喜」显式归巫婆线；'
           '② **殉情**——维持 §14.3 甲 830 年爱葛莉丝与公爵同赴绞架／殉情裁定；'
           '③ **不解释**——老管家 L36／L43 零解释，不代填、不推定、不排产、不设伏笔编号；'
           '④ **穿越不入设定**——维持 §0.6 v0.3-r2 正典「删除穿越、不作彩蛋」，前世参照系存照不入正典。'
           '代数 12／14 本轮未裁，仍挂 §11.1。v2.96 拿不准表状态列已回填「已裁定」，其防误判③同步改写；新增 v2.97 裁结表（4 项）＋6 条防误判。')
L.insert(idx[0], new_reg)
save(P, L)
print('说明集 updated, lines', len(L))

# ---------- 台账 ----------
P2 = BASE + '设定集_裁定台账.md'
L2 = load(P2)
ci = [i for i, l in enumerate(L2) if l.startswith('| **当前版本** |')]
pi = [i for i, l in enumerate(L2) if l.startswith('| **上一版** |')]
assert ci and pi, ('ledger rows', len(ci), len(pi))
L2[ci[0]] = ('| **当前版本** | v2.97 | 2026-11-25 | 《宗教裁判所》第1章拿不准 4 项结案：黑袍＝巫婆（海姬不并同）／殉情维持 830／老管家不解释／穿越不入设定；代数 12/14 仍挂起 | 23,251 行／3,661,180 B |')
L2[pi[0]] = ('| **上一版** | 本机 **v2.96**（第一百三十七轮·《宗教裁判所》第1章分析查漏补缺：重复13组忽略／确缺7项补入／拿不准5项交裁定；前传P8先行补注）——本版升 v2.97，v2.96 md／docx 哈希核对一致后归档。 |')
save(P2, L2)
print('台账 updated')

# ---------- 归档索引 ----------
P3 = BASE + '历史版本/00_归档索引.md'
L3 = load(P3)
rep1(L3, '（`v1.0` → `v2.95`，含 `v1.66整合`） | 209 |',
        '（`v1.0` → `v2.96`，含 `v1.66整合`） | 211 |', 'set-count')
rep1(L3, '| 298 |', '| 300 |', 'script-count')
rep1(L3, '**合计 724 件／660 MB**（v2.96 收口新增 4 件：',
        '**合计 728 件／660 MB**（v2.97 收口新增 4 件：v2.96 归档 md／docx 2＋`_v297.py`／`_v297_docs.py` 2；v2.96 收口新增 4 件：',
        'total')
save(P3, L3)
print('归档索引 updated')

# ---------- 工作日志（追加，反引号安全） ----------
LOG = 'E:/2026-11-10-13-57-56/.workbuddy/memory/2026-11-25.md'
addition = """

---

## v2.97（2026-11-25）·《宗教裁判所》第1章拿不准 4 项裁定结案

用户裁定原文：「1.黑袍为巫婆；2.殉情；3.不解释；4.穿越不入设定」。

**查库前置**：L4644 长期规则「设定层『巫婆』特指圣阿尔忒弥斯」（§3.1 #1）；§1.7 #2/#3/#5/#7 多处坐实黑袍女人＝圣阿尔忒弥斯＝巫婆（背三封印同人）。故第 1 裁与既有体系兼容，非新设；仅正式否决分析方 P005「疑＝海姬」。

**落位**：新增 v2.97 裁结块（§4 前），4 项状态回填 v2.96 拿不准表；防误判③「P005 未裁前」改写为已结案。P005 黑袍＝巫婆＝圣阿尔忒弥斯、海姬不并同、L22 藏獒欣喜归巫婆线；P006 维持 §14.3 甲 830 年殉情；P007 老管家 L36/L43 零解释、不代填不排产；P008 维持 §0.6 删除穿越正典。代数 12/14 用户未裁，仍挂 §11.1。

**教训**：沿用 v2.96 正确流程——先复制归档旧版并哈希核对，再写新版到新文件名后删旧文件；避免覆盖后从 git 恢复导致 CRLF 丢失。

md 23,251 行／3,661,180 B／裸 LF 0；docx 2,138,388 B（780 标题／1236 表）。四件套全绿（preflight OK／verify_fact 8 条 OK／rzz CHECK OK／结构基线：缺空行 1、表格异常 3 行既有、连续空行 0）。v2.96 md/docx 哈希 f2abb7a8／2785fea5 归档。

**未做**：代数 12/14 待裁；未上传资料库（在线仍 v2.52，无双机同步口令）；第2章分析未到。
"""
with io.open(LOG, 'a', encoding='utf-8') as f:
    f.write(addition)
print('日志 appended')
