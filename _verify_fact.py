# -*- coding: utf-8 -*-
"""
_verify_fact.py —— 事实性断言校验（纯文字比对，对抗 markdown 噪声）

替代脆弱的「精确字符串匹配」。v2.00 教训：错误句 "拜占奥总部在**金雀花**"
被加粗打断后，精确匹配查不出来，导致首轮漏检 2 处。

核心：把 md 里的 **加粗** / ~~删除线~~ / `代码` / [链接](url) / #标题 等
语法标记全部剥离，只留「纯文字」再做子串比对。这样无论目标词被什么
markdown 语法包裹/打断，都能命中。

区分两类命中：
  - 活跃命中：在正常正文里出现 → 若是错误句，必须清零
  - 留档命中：在 ~~删除线~~ 内出现 → 是历史留档，合规（可追溯）

用法:
  python _verify_fact.py                      # 跑内置规则集（最新设定集）
  python _verify_fact.py <指定.md路径>        # 指定文件
  python _verify_fact.py --self-test          # 归一化函数自测
退出码: 0=全部符合预期; 1=有断言不符
"""
import io
import os
import re
import sys
import glob

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------- markdown 语法剥离 ----------
def strip_md(line):
    """把一行 md 剥成纯文字：去语法标记，保留可读文字。"""
    s = line
    # 删除线：整段标记去掉（内容保留，但记录在 callers 里另判）
    s = s.replace('~~', '')
    # 加粗/斜体
    s = s.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
    # 行内代码
    s = s.replace('`', '')
    # 链接 [text](url) -> text；图片 ![alt](url) -> alt
    s = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', s)
    # 标题井号 / 引用符 / 列表符（只去行首标记）
    s = re.sub(r'^\s*#{1,6}\s*', '', s)
    s = re.sub(r'^\s*>\s?', '', s)
    s = re.sub(r'^\s*[-*+]\s+', '', s)
    s = re.sub(r'^\s*\d+\.\s+', '', s)
    # 表格分隔管道 -> 空格（避免 |词| 粘连）
    s = s.replace('|', ' ')
    # 折叠多余空白
    s = re.sub(r'\s+', '', s)  # 连空白都去掉，彻底抗格式噪声
    return s

def is_historical(line, norm_pat):
    """该命中是否处于「历史引用语境」（合规，非活跃错误）。
    三类：① 删除线留档；② 目标词被引号「」""包裹（被当作对象引用）；
    ③ 整行是纠错/留档描述（含 更正为/旧记/系误/留档/作废/注销 等语境词）。"""
    if '~~' in line:
        return True
    # 目标词（纯文字态）被中文引号包裹 → 引用对象
    if ('「' + norm_pat + '」') in strip_md(line) or ('"' + norm_pat + '"') in strip_md(line):
        return True
    # 纠错语境词
    for kw in ('更正为', '更正', '旧记', '系误', '留档', '作废', '注销', '旧口径', '已清零', '连带口径'):
        if kw in line:
            return True
    return False

# ---------- 内置规则集 ----------
# (名称, 纯文字模式, 期望)  期望: 'absent'=必须清零 / 'present'=必须存在
# 模式写成连续中文（strip_md 会去空白），匹配时用 strip_md 后的模式
RULES = [
    # —— 教廷总部纠错（v2.00）——
    ('活跃错误:教廷总部在金雀花', '总部在金雀花', 'absent'),
    ('活跃错误:总部位于金雀花',   '总部位于金雀花', 'absent'),
    ('活跃错误:教廷在金雀花',     '教廷在金雀花', 'absent'),
    ('活跃错误:总部在金雀花王朝', '总部在金雀花王朝', 'absent'),
    # —— 应有事实 ——
    ('应有:总部在白蔷薇',         '总部在白蔷薇', 'present'),
    ('应有:后传L4300锚',          '后传L4300', 'present'),
    ('应有:朱庇特第六大城市',     '第六大城市', 'present'),
    # —— 前五城市逻辑禁区 ——
    ('活跃错误:朱庇特入前五',     '朱庇特城约', 'absent'),  # 防旧表残留
]

def load_target(path_arg):
    if path_arg:
        return path_arg
    mds = glob.glob(os.path.join(BASE, '天神下凡设定集_归纳整理版_[vV]*.md'))
    best = None
    bv = (-1,)
    for m in mds:
        mt = re.search(r'_[vV](\d+\.\d+)\.md$', os.path.basename(m))
        if mt:
            v = tuple(int(x) for x in mt.group(1).split('.'))
            if v > bv:
                bv, best = v, m
    return best

def self_test():
    cases = [
        ('拜占奥总部在**金雀花**王朝', '总部在金雀花王朝', True),
        ('拜占奥总部在金雀花王朝',     '总部在金雀花王朝', True),
        ('~~旧记总部在金雀花~~',       '总部在金雀花', True),
        ('拜占奥总部在`金雀花`',       '总部在金雀花', True),
        ('拜占奥  总部在  金雀花',     '总部在金雀花', True),
        ('教廷总部在白蔷薇',           '总部在金雀花', False),
    ]
    ok = True
    for raw, pat, want in cases:
        got = strip_md(pat) in strip_md(raw)
        flag = 'OK' if got == want else 'FAIL<<<'
        print('  %-30s 含「%s」= %s (%s)' % (raw, pat, got, flag))
        if got != want:
            ok = False
    # 历史语境判定：这些命中应被识别为「归档」而非「活跃错误」
    hist = [
        ('| 2 | 全稿13处「教廷总部在金雀花」连带口径就地更正为白蔷薇 |', '总部在金雀花', True),
        ('~~用户明定金雀花，以《天神》为准~~ **【v2.00更正·旧行留档】**总部在白蔷薇', '金雀花', True),
        ('拜占奥教廷总部在金雀花王朝。', '总部在金雀花', False),  # 真活跃错误，不得归档
    ]
    for raw, pat, want_hist in hist:
        np = strip_md(pat)
        got = is_historical(raw, np) if np in strip_md(raw) else None
        flag = 'OK' if got == want_hist else 'FAIL<<<'
        print('  历史语境「%s」-> %s (%s)' % (raw[:24], got, flag))
        if got != want_hist:
            ok = False
    print('SELF-TEST', 'OK' if ok else 'FAIL')
    return 0 if ok else 1

def main():
    args = sys.argv[1:]
    if '--self-test' in args:
        return self_test()
    target = load_target(args[0] if args else None)
    if not target or not os.path.exists(target):
        print('找不到目标 md: %s' % target)
        return 1
    raw = io.open(target, encoding='utf-8', newline='').read()
    lines = raw.splitlines()
    print('=' * 70)
    print('事实性断言校验（纯文字比对）：%s' % os.path.basename(target))
    print('行数=%d' % len(lines))
    print('=' * 70)

    bad = []
    for name, pat, expect in RULES:
        norm_pat = strip_md(pat)
        hits_active, hits_archive = [], []
        for i, line in enumerate(lines, 1):
            if norm_pat in strip_md(line):
                (hits_archive if is_historical(line, norm_pat) else hits_active).append(i)

        if expect == 'absent':
            ok = len(hits_active) == 0
            detail = ('活跃命中 %d 处 %s' % (len(hits_active), hits_active[:8])) if hits_active else '已清零'
            if hits_archive:
                detail += '；历史引用/留档 %d 处(合规)' % len(hits_archive)
        else:  # present
            ok = len(hits_active) > 0
            detail = ('存在 %d 处 %s' % (len(hits_active), hits_active[:8])) if hits_active else '不存在'

        print('  [%s] %-32s %s' % ('OK' if ok else 'FAIL<<<', name, detail))
        if not ok:
            bad.append('%s: %s' % (name, detail))

    print('=' * 70)
    if bad:
        print('VERIFY FAIL —— %d 条断言不符:' % len(bad))
        for b in bad:
            print('  ! ' + b)
        return 1
    print('VERIFY OK —— 全部 %d 条事实断言符合预期。' % len(RULES))
    return 0

if __name__ == '__main__':
    sys.exit(main())
