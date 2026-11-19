# -*- coding: utf-8 -*-
"""_rzz.py —— 「XX 人物志」自动化工作流工具（v1.0）

子命令：
  python _rzz.py pick "人物名" "别名1" "别名2"   # 第1步取批：原文命中＋设定集存量＋查重，出取批单
  python _rzz.py new  "人物名"                    # 第4步：从模板生成推导稿骨架
  python _rzz.py check                            # 第6步收口：CRLF/空行/表格/preflight/verify/docx同步

设计原则：
  · 只读原文与设定集，不改任何正文；
  · 凡"查重"结论必须来自文件实际命中，不靠记忆；
  · 输出一律 utf-8，落盘到 人物志工作流/ 下。
"""
import io
import os
import re
import subprocess
import sys
import zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(BASE, '宗教裁判所.txt')
POST = os.path.join(BASE, '《天神下凡》.txt')
OUTDIR = os.path.join(BASE, '人物志工作流')
PICKDIR = os.path.join(OUTDIR, '取批')
DRAFTDIR = os.path.join(OUTDIR, '推导稿')
TPL_DRAFT = os.path.join(OUTDIR, '03_推导稿模板.md')


# ------------------------------------------------------------------ 工具函数
def read_lines(path):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding='utf-8', errors='replace') as f:
        return f.read().replace('\r\n', '\n').split('\n')


def latest_md():
    cands = [f for f in os.listdir(BASE)
             if re.match(r'^天神下凡设定集_归纳整理版_v[\d.]+\.md$', f)]
    if not cands:
        return None
    def key(f):
        v = re.search(r'v([\d.]+)\.md$', f).group(1)
        return tuple(int(x) for x in v.split('.'))
    return os.path.join(BASE, sorted(cands, key=key)[-1])


def section_of(lines, idx):
    """返回最近的二级/三级标题，用于归类。"""
    for i in range(idx, -1, -1):
        m = re.match(r'^(#{2,4})\s+(.*)$', lines[i])
        if m:
            return m.group(2).strip()
    return '(文首)'


# ------------------------------------------------------------------ pick
def cmd_pick(args):
    if not args:
        print('用法: python _rzz.py pick "人物名" ["别名1" ...]')
        return 2
    name = args[0]
    keys = [a for a in args if a.strip()] or [name]
    keys = list(dict.fromkeys(keys))

    print('=' * 66)
    print('取批：%s    关键词：%s' % (name, ' / '.join(keys)))
    print('=' * 66)

    # ---- 原文命中
    hits = []
    for tag, path in (('前传', PRE), ('后传', POST)):
        lines = read_lines(path)
        for i, ln in enumerate(lines):
            if any(k in ln for k in keys):
                hits.append((tag, i + 1, ln.strip()))
    pre_n = sum(1 for h in hits if h[0] == '前传')
    post_n = len(hits) - pre_n
    print('原文命中：前传 %d 处 / 后传 %d 处 / 合计 %d 处' % (pre_n, post_n, len(hits)))

    # ---- 设定集存量
    md = latest_md()
    stock = []      # 精确名命中
    broad = 0       # 仅别名命中（噪音层，只计数不列全）
    blocks = []
    if md:
        slines = read_lines(md)
        for i, ln in enumerate(slines):
            if name in ln:
                stock.append((i + 1, section_of(slines, i), ln.strip()[:200]))
            elif any(k in ln for k in keys):
                broad += 1
        # 已有该人物补注块？优先按「名字」精确匹配，退回整名包含
        other_blocks = []
        for i, ln in enumerate(slines):
            if ln.startswith('####') and '补注' in ln and name in ln:
                if '人物志' in ln:
                    blocks.append((i + 1, ln.strip()))
                else:
                    other_blocks.append((i + 1, ln.strip()))
        print('设定集（%s）存量：精确名 %d 行（别名另 %d 行）；人物志补注块：%d 个；其他相关补注块：%d 个' %
              (os.path.basename(md), len(stock), broad, len(blocks), len(other_blocks)))

    # ---- 证据密度建议
    n = len(hits)
    if n == 0:
        verdict = '⚠️ 零命中——先向用户索要素材（docx／理解长文），不要硬推'
    elif n < 5:
        verdict = '⚠️ 命中很少——可能是次要角色，建议简版人物志，或先索要素材'
    elif n < 30:
        verdict = '✅ 命中适中——重要配角，按全流程执行'
    else:
        verdict = '✅ 证据充足——主要人物，按全流程执行，注意原文事实层勿重抄'
    if blocks:
        verdict += '；**已有补注块，默认「已有项不重写」，只补新增**'
    if pre_n == 0 or post_n == 0:
        verdict += '｜⚠️ 单侧 0 命中，很可能是**称号差异**（如前传作「卡妙皇帝」、后传作「卡妙女皇」），请补别名重跑'
    print('判断：%s' % verdict)

    # ---- 写取批单
    if not os.path.isdir(PICKDIR):
        os.makedirs(PICKDIR)
    out = os.path.join(PICKDIR, '%s_取批单.md' % name)
    buf = []
    buf.append('# 「%s」取批单（自动生成 %s）\n' % (name, '2026-11-19'))
    buf.append('- 关键词：%s' % ' / '.join('`%s`' % k for k in keys))
    buf.append('- 原文命中：前传 **%d** 处 / 后传 **%d** 处 / 合计 **%d** 处' % (pre_n, post_n, n))
    buf.append('- 设定集存量：精确名 **%d** 行（别名另 **%d** 行）；同名补注块：**%d** 个' % (len(stock), broad, len(blocks)))
    buf.append('- 自动化判断：%s\n' % verdict)

    buf.append('## 一、原文命中清单\n')
    buf.append('| # | 出处 | 行号 | 原句（截断） |')
    buf.append('| --- | --- | --- | --- |')
    for j, (tag, no, ln) in enumerate(hits, 1):
        buf.append('| %d | %s | **L%d** | %s |' % (j, tag, no, ln[:180].replace('|', '｜')))
    if not hits:
        buf.append('| — | — | — | 无命中 |')

    buf.append('\n## 二、设定集存量（先查重，防重复添加）\n')
    if stock:
        buf.append('| 行号 | 所属章节 | 内容（截断） |')
        buf.append('| --- | --- | --- |')
        for no, sec, ln in stock[:60]:
            buf.append('| L%d | %s | %s |' % (no, sec.replace('|', '｜'), ln.replace('|', '｜')))
        if len(stock) > 60:
            buf.append('| … | 另有 %d 行 | |' % (len(stock) - 60))
    else:
        buf.append('（设定集内无该关键词命中——属全新条目，需新建）')

    buf.append('\n## 三、已有补注块\n')
    if blocks:
        for no, ln in blocks:
            buf.append('- **人物志块** L%d %s' % (no, ln))
        buf.append('\n> 已有块 → 按「已有项不重写」，本轮只补新增，**不重复添加整块**。')
    else:
        buf.append('（无人物志块）→ 本轮需新建 `#### vX.XX 补注｜「%s」` 块。' % name)
    if other_blocks:
        buf.append('\n其他相关补注块（非人物志，写时勿与之冲突）：')
        for no, ln in other_blocks:
            buf.append('- L%d %s' % (no, ln))

    buf.append('\n## 四、下一步（按流程卡）\n')
    buf.append('1. 精读上表第一条到最后一条，**不跳读**；')
    buf.append('2. 把要引用的原句抄成行号清单；')
    buf.append('3. 逐条回查（带上下文核行号，禁止全局数字替换）；')
    buf.append('4. `python _rzz.py new "%s"` 生成推导稿骨架；' % name)
    buf.append('5. 出稿 → 交裁定 → 落盘 → `python _rzz.py check`。')

    io.open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(buf) + '\n')
    print('\n取批单已生成：%s' % out)
    return 0


# ------------------------------------------------------------------ new
def cmd_new(args):
    if not args:
        print('用法: python _rzz.py new "人物名"')
        return 2
    name = args[0]
    if not os.path.exists(TPL_DRAFT):
        print('❌ 缺模板：%s' % TPL_DRAFT)
        return 2
    if not os.path.isdir(DRAFTDIR):
        os.makedirs(DRAFTDIR)
    out = os.path.join(DRAFTDIR, '%s_推导稿.md' % name)
    if os.path.exists(out):
        print('⚠️ 已存在，不覆盖：%s' % out)
        return 1
    tpl = io.open(TPL_DRAFT, encoding='utf-8').read()
    tpl = tpl.replace('<人物名>', name)
    io.open(out, 'w', encoding='utf-8', newline='\n').write(tpl)
    print('推导稿骨架已生成：%s' % out)
    return 0


# ------------------------------------------------------------------ check
def run_script(name):
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        return None
    try:
        p = subprocess.run([sys.executable, path], cwd=BASE,
                           capture_output=True, text=True, timeout=300)
        return (p.returncode, (p.stdout or '') + (p.stderr or ''))
    except Exception as e:
        return (99, str(e))


def docx_text(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    return re.sub(r'<[^>]+>', '', xml)


def cmd_check(_args):
    md = latest_md()
    if not md:
        print('❌ 找不到设定集 md')
        return 2
    ver = re.search(r'v([\d.]+)\.md$', os.path.basename(md)).group(1)
    docx = md[:-3] + '.docx'
    print('=' * 66)
    print('收口自检：v%s' % ver)
    print('=' * 66)

    raw = io.open(md, encoding='utf-8', newline='').read()
    lines = raw.split('\r\n')
    fails = []

    # 1 CRLF
    bare = raw.count('\n') - raw.count('\r\n')
    print('[1] 行数 %d ／ 字节 %d ／ 裸 LF %d' % (len(lines) - 1, len(raw.encode('utf-8')), bare))
    if bare:
        fails.append('裸 LF %d 处（应为 0）' % bare)

    # 2 3+ 连续空行
    big = len(re.findall(r'(\r\n){4,}', raw))
    print('[2] 3 行以上连续空行：%d' % big)
    if big:
        fails.append('连续空行 %d 处' % big)

    # 3 表格列数
    bad, in_tbl, cols = [], False, 0
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('|') and s.endswith('|'):
            n = s.count('|') - 1
            if not in_tbl:
                in_tbl, cols = True, n
            elif n != cols:
                bad.append(i + 1)
        else:
            in_tbl = False
    print('[3] 表格列数异常：%d 行 %s' % (len(bad), bad[:8] if bad else ''))
    if len(bad) > 3:
        fails.append('表格列数异常 %d 行' % len(bad))
    elif bad:
        print('    注：≤3 行为既有问题（阿芙罗狄表），不阻断')

    # 4 preflight / verify
    for s in ('_preflight.py', '_verify_fact.py'):
        r = run_script(s)
        if r is None:
            print('[4] %s 不存在，跳过' % s)
            continue
        code, out = r
        tail = [x for x in out.strip().split('\n') if x.strip()][-2:]
        ok = (code == 0)
        print('[4] %s → %s' % (s, 'OK' if ok else 'FAIL(code=%d)' % code))
        for x in tail:
            print('      %s' % x[:150])
        if not ok:
            fails.append('%s 未通过' % s)

    # 5 docx 同名与关键块
    if not os.path.exists(docx):
        print('[5] 同名 docx：缺失')
        fails.append('缺同名 docx')
    else:
        size = os.path.getsize(docx)
        md_size = os.path.getsize(md)
        print('[5] 同名 docx：%d B（md %d B，比 %.2f）' % (size, md_size, size / md_size))
        try:
            dt = docx_text(docx)
            # 取版本号最高的 4 个补注块标题 + 最高 2 条登记行，验证已在 docx
            def vkey(s):
                m = re.search(r'v([\d.]+)', s)
                return tuple(int(x) for x in m.group(1).split('.')) if m else (0,)
            def clean(s):
                return re.sub(r'[#>*`]', '', s).strip()
            blk, regs = [], []
            for l in lines:
                s = l.strip()
                if s.startswith('#### v') and '补注' in s:
                    blk.append(s)
                elif re.match(r'^> \*\*v[\d.]+ 登记', s) or re.match(r'^> \*\*v[\d.]+ 补记', s):
                    regs.append(s)
            blk = [clean(b) for b in sorted(blk, key=vkey)[-4:]]
            regs = [clean(r) for r in sorted(regs, key=vkey)[-2:]]
            checks = blk + regs
            # 用「最长中文片段」比对，绕开 #、*、数字写法等标记差异
            miss = []
            for c in checks:
                frags = re.findall(r'[\u4e00-\u9fa5，。：；、「」·—]{12,}', c)
                probe = frags[0] if frags else c[:20]
                if probe not in dt:
                    miss.append((c[:56], probe[:30]))
            print('    关键块比对：%d 项，缺 %d 项' % (len(checks), len(miss)))
            for m, probe in miss:
                print('      缺：%s … 片段「%s」' % (m, probe))
            if miss:
                fails.append('docx 关键块缺 %d 项' % len(miss))
        except Exception as e:
            print('    docx 解析失败：%s' % e)
            fails.append('docx 解析失败')

    print('-' * 66)
    if fails:
        print('CHECK FAIL：')
        for f in fails:
            print('  ! ' + f)
        return 1
    print('CHECK OK —— 可提交。')
    return 0


# ------------------------------------------------------------------ main
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == 'pick':
        return cmd_pick(args)
    if cmd == 'new':
        return cmd_new(args)
    if cmd == 'check':
        return cmd_check(args)
    print('未知子命令：%s' % cmd)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
