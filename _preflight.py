# -*- coding: utf-8 -*-
"""
_preflight.py —— 设定集归位任务「开工自检」强制脚本

任何归位/纠错/升版任务开工前必须先跑本脚本，通过（全 OK）方可动手。
把「回查原文」从自觉变成机制：台账里声明的行号，逐字回原文核验；
纠错档案里登记的错误行号，反向验证其确实不含目标词（证明它们真的错）。

四项检查：
  1. 前后传原文 sha256 锚 —— 变了就停（原文被改动，一切行号作废）
  2. 台账原文锚点逐字核验 —— 每个 (作品,行号,关键词) 必须命中
  3. 纠错档案反向验证 —— 错误行号必须「不含」目标词（否则纠错本身错了）
  4. 设定集版本与 CRLF 纯净度 —— 报当前最高版本、裸 LF 必须为 0

用法： python _preflight.py           （在工作目录 E:/天神下凡 下运行）
退出码：0=全通过；1=有 FAIL（禁止开工）
"""
import io
import os
import re
import sys
import glob
import hashlib

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(BASE, '宗教裁判所.txt')
POST = os.path.join(BASE, '《天神下凡》.txt')

# ---------- 1. 原文哈希锚 ----------
ANCHOR = {
    PRE:  ('前传《宗教裁判所》', '351bf2163181bdb8', 3107),
    POST: ('后传《天神下凡》',   '7950234a2f11785f', 6982),
}

def sha16(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()[:16]

fails = []
print('=' * 70)
print('【1/4】原文哈希锚校验')
lines_cache = {}
for path, (name, want, want_lines) in ANCHOR.items():
    got = sha16(path)
    nlines = len(io.open(path, encoding='utf-8').read().splitlines())
    ok = (got == want and nlines == want_lines)
    print('  %s sha=%s(%s) 行数=%d(%s) -> %s'
          % (name, got, 'OK' if got == want else 'ERR', nlines,
             'OK' if nlines == want_lines else 'ERR', 'OK' if ok else 'FAIL'))
    if not ok:
        fails.append('%s 哈希锚/行数不符，原文可能被改动，所有行号作废' % name)
    lines_cache[path] = io.open(path, encoding='utf-8').read().splitlines()

# ---------- 2. 台账原文锚点逐字核验 ----------
# (作品key, 行号, 必须逐字出现的关键词) —— 来自《设定集_裁定台账》第二节
ANCHORS = [
    ('POST', 4300, '拜占奥教廷就位于它的心脏位置'),
    ('PRE',  2052, '位于白蔷薇皇朝中的拜占奥教廷有教皇厅'),
    ('PRE',  1926, '拥有拜占奥教廷的白蔷薇皇朝一直是黑桃'),
    ('POST', 3810, '开始走下坡路'),
    ('PRE',  1562, '她的教徒遍及史诗大陆'),
    ('PRE',  2562, '拥有梵特兰蒂冈六倍信徒的拜占奥教廷'),
    ('PRE',  2440, '拜占奥教廷的核心圣徒石碑大教堂曾是史诗大陆上最高的建筑'),
    ('POST', 5727, '大陆精神之父'),
    ('POST', 4005, '史诗大陆第六大城市，拥有百万人口'),
    ('PRE',  2104, '接近70万人'),
    ('PRE',  55,   '帝都之外的第二大城'),
    ('PRE',  2442, '帝国西北部第一大城市'),
    ('POST', 5423, '被四大国家监管'),
    ('PRE',  2564, '卡妙帝国的心脏'),
    ('POST', 3030, '卡妙帝国的心脏'),
    ('POST', 1460, '大陆9条龙脉'),
    ('POST', 1314, '乔纳森龙脉'),
    ('PRE',  2032, '介于大贵族和平民之间的阶层'),
    ('PRE',  2036, '鲜红色刺目基调'),
    ('PRE',  2038, '附属国斯拉格公国'),
    ('PRE',  2441, '卡妙新皇帝增高了北极钟声大教堂的高度'),
    ('POST', 6506, '三十六个小国'),
    ('POST', 1866, '金雀花文还是史诗大陆的首席语言'),
]
PATHKEY = {'PRE': PRE, 'POST': POST}
print('=' * 70)
print('【2/4】台账原文锚点逐字核验（%d 条）' % len(ANCHORS))
for key, n, kw in ANCHORS:
    line = lines_cache[PATHKEY[key]][n - 1]
    hit = kw in line
    if not hit:
        fails.append('锚点 %s L%d 不含关键词「%s」' % (key, n, kw))
    print('  %s L%-5d %-28s %s' % (key, n, kw[:26], 'OK' if hit else 'FAIL<<<'))

# ---------- 3. 纠错档案反向验证 ----------
# (作品key, 错误行号, 目标词) —— 错误行号必须「不含」目标词，否则是纠错写错了
WRONG = [
    ('POST', 1459, '大陆9条龙脉'),     # 实为「巨龙。」
    ('POST', 1790, '被四大国家监管'),  # 实为多明戈隐修会
    ('POST', 676,  '大陆精神之父'),    # 实为教皇招牌段
    ('PRE',  1866, '老大帝国'),        # 实为金雀花文首席语言
    ('POST', 2564, '卡妙帝国的心脏'),  # 后传 L2564 为捧头颅父亲段
]
print('=' * 70)
print('【3/4】纠错档案反向验证（错误行号应「不含」目标词，%d 条）' % len(WRONG))
for key, n, kw in WRONG:
    line = lines_cache[PATHKEY[key]][n - 1]
    absent = kw not in line
    if not absent:
        fails.append('纠错档案 %s L%d 竟含「%s」，纠错记录有误，需复核' % (key, n, kw))
    print('  %s L%-5d 不含「%-16s」 %s' % (key, n, kw[:14], 'OK' if absent else 'FAIL<<<'))

# ---------- 4. 设定集版本与 CRLF ----------
print('=' * 70)
print('【4/4】设定集版本与 CRLF 纯净度')
mds = glob.glob(os.path.join(BASE, '天神下凡设定集_归纳整理版_[vV]*.md'))
vers = []
for m in mds:
    mt = re.search(r'_[vV](\d+\.\d+)\.md$', os.path.basename(m))
    if mt:
        vers.append((tuple(int(x) for x in mt.group(1).split('.')), mt.group(1), m))
vers.sort()
if vers:
    top = vers[-1]
    print('  当前最高版本: v%s  (%s)' % (top[1], os.path.basename(top[2])))
    raw = open(top[2], 'rb').read()
    bare_lf = raw.count(b'\n') - raw.count(b'\r\n')
    print('  字节=%d  裸LF=%d  -> %s' % (len(raw), bare_lf, 'OK' if bare_lf == 0 else 'FAIL<<<'))
    if bare_lf != 0:
        fails.append('设定集 v%s 存在 %d 个裸 LF，CRLF 不纯' % (top[1], bare_lf))
    # 同名 docx 检查
    docx = top[2][:-3] + '.docx'
    print('  同名 docx: %s' % ('存在 OK' if os.path.exists(docx) else '缺失 FAIL<<<'))
    if not os.path.exists(docx):
        fails.append('设定集 v%s 缺同名 docx' % top[1])
else:
    fails.append('未找到设定集 md')

# ---------- 结论 ----------
print('=' * 70)
if fails:
    print('PREFLIGHT FAIL —— 禁止开工，请先修以下问题（%d 项）:' % len(fails))
    for x in fails:
        print('  ! ' + x)
    sys.exit(1)
else:
    print('PREFLIGHT OK —— 原文锚全命中、纠错档案自洽、CRLF 纯净。')
    print('')
    print('开工前六步规程 checklist（逐项确认后再动手）:')
    print('  [ ] 1 取批      —— 明确本批素材范围')
    print('  [ ] 2 精读      —— 逐条读懂，不跳读')
    print('  [ ] 3 回查原文  —— 每条事实性断言附行号（本脚本已核锚，新断言仍需现核）')
    print('  [ ] 4 归类归位  —— 8–16 块，一条设定只归一个主词条')
    print('  [ ] 5 全量校验  —— 跑 _verify_fact.py 纯文字哈希比对')
    print('  [ ] 6 升版同步  —— 升版 + 改 _md2docx.py 三处版本号 + 重生 docx')
    sys.exit(0)
