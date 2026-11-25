# -*- coding: utf-8 -*-
"""把设定集 md 转成 docx（复用 _tpl_base_v1.77.docx 的 styles/sectPr/页脚），无 pandoc 依赖。
使用：改下方 SRC_MD / OUT 两个文件名即可（md 与 docx 须同名，见设定集 §0.6 第十六款）。"""
import io, os, re, zipfile, datetime, html

BASE = 'E:/天神下凡/'
SRC_MD = BASE + '天神下凡设定集_归纳整理版_v2.89.md'
TPL = BASE + '历史版本/_tpl_base_v1.77.docx'
OUT = BASE + '天神下凡设定集_归纳整理版_v2.89.docx'

ILLEGAL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f]')


def esc(t):
    return html.escape(ILLEGAL.sub('', t), quote=False)


# ---------------- 行内 ----------------
def _run(txt, rpr, extra=''):
    txt = scrub(txt)
    body = esc(txt.replace('\x01', '*').replace('\x02', '_'))
    return '<w:r><w:rPr>%s%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, extra, body)


MASK = '\ue000'


def scrub(t):
    """落单标记清理：保护 *** （屏蔽词占位），清掉未配对的 ** 与反引号。"""
    t = t.replace('***', MASK)
    t = t.replace('**', '').replace('`', '')
    return t.replace(MASK, '***')


def runs(text, base_rpr='', code_font='Consolas'):
    """逐字符扫描，避免反引号/星号奇偶错位导致整段失效。"""
    text = text.replace('\\*', '\x01').replace('\\_', '\x02')
    # 独立 *** 视作屏蔽词占位，先占位保护，避免被斜体分支拆散
    text = re.sub(r'(?<!\*)\*\*\*(?!\*)', MASK, text)
    out, buf, i, n = [], '', 0, len(text)

    def flush():
        nonlocal buf
        if buf:
            out.append(_run(scrub(buf), base_rpr))
            buf = ''

    while i < n:
        c = text[i]
        if c == '`':
            j = text.find('`', i + 1)
            if j > i + 1 and '\n' not in text[i + 1:j] and j - i < 400:
                flush()
                out.append(_run(text[i + 1:j], base_rpr,
                                '<w:rFonts w:ascii="%s" w:hAnsi="%s"/>'
                                '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>'
                                % (code_font, code_font)))
                i = j + 1
                continue
            buf += c
            i += 1
            continue
        if text.startswith('**', i):
            j = text.find('**', i + 2)
            if j > i + 2 and '\n' not in text[i + 2:j]:
                flush()
                out.append(_run(text[i + 2:j], base_rpr, '<w:b w:val="1"/>'))
                i = j + 2
                continue
            buf += c
            i += 1
            continue
        if text.startswith('~~', i):
            j = text.find('~~', i + 2)
            if j > i + 2:
                flush()
                out.append(_run(text[i + 2:j], base_rpr, '<w:strike w:val="1"/>'))
                i = j + 2
                continue
            buf += c
            i += 1
            continue
        if c == '*':
            # 单星在中文稿中多为脱敏/占位标记，一律按字面保留，避免误配成斜体
            buf += c
            i += 1
            continue
        buf += c
        i += 1

    flush()
    if not out:
        out.append(_run('', base_rpr))
    return ''.join(out)


# ---------------- 块级 ----------------
HDR = {1: '000005', 2: '000001', 3: '000003', 4: '000006', 5: '000006', 6: '000006'}


def p_heading(level, text):
    sid = HDR.get(level, '000006')
    if level == 1:
        ppr = ('<w:pPr><w:pStyle w:val="%s"/><w:jc w:val="center"/>'
               '<w:spacing w:before="240" w:after="240"/></w:pPr>' % sid)
        rpr = '<w:rFonts w:hint="eastAsia"/><w:b w:val="1"/><w:sz w:val="44"/><w:szCs w:val="44"/>'
    elif level == 2:
        ppr = '<w:pPr><w:pStyle w:val="%s"/><w:spacing w:before="240" w:after="120"/></w:pPr>' % sid
        rpr = '<w:rFonts w:hint="eastAsia"/><w:b w:val="1"/><w:sz w:val="30"/><w:szCs w:val="30"/>'
    elif level == 3:
        ppr = '<w:pPr><w:pStyle w:val="%s"/><w:spacing w:before="200" w:after="100"/></w:pPr>' % sid
        rpr = '<w:rFonts w:hint="eastAsia"/><w:b w:val="1"/><w:sz w:val="26"/><w:szCs w:val="26"/>'
    else:
        ppr = '<w:pPr><w:pStyle w:val="%s"/><w:spacing w:before="160" w:after="80"/></w:pPr>' % sid
        rpr = '<w:rFonts w:hint="eastAsia"/><w:b w:val="1"/><w:sz w:val="23"/><w:szCs w:val="23"/>'
    return '<w:p>%s%s</w:p>' % (ppr, runs(text, rpr))


def p_body(text, ind=0, after=80):
    ppr = '<w:pPr><w:spacing w:before="0" w:after="%d" w:line="300" w:lineRule="auto"/>' % after
    if ind:
        ppr += '<w:ind w:left="%d"/>' % ind
    ppr += '</w:pPr>'
    return '<w:p>%s%s</w:p>' % (ppr, runs(text, '<w:rFonts w:hint="eastAsia"/>'))


def p_quote(text):
    ppr = ('<w:pPr><w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="C0C4CC"/></w:pBdr>'
           '<w:shd w:val="clear" w:color="auto" w:fill="F7F8FA"/>'
           '<w:spacing w:before="0" w:after="40" w:line="280" w:lineRule="auto"/>'
           '<w:ind w:left="240" w:right="80"/></w:pPr>')
    return '<w:p>%s%s</w:p>' % (ppr, runs(text, '<w:rFonts w:hint="eastAsia"/><w:color w:val="404A5C"/><w:sz w:val="19"/><w:szCs w:val="19"/>'))


def p_code(lines):
    out = []
    for ln in lines:
        ppr = ('<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F5F5F5"/>'
               '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
               '<w:ind w:left="160"/></w:pPr>')
        out.append('<w:p>%s<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:hint="eastAsia"/>'
                   '<w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
                   % (ppr, esc(ln)))
    return ''.join(out)


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    cells, buf, i = [], '', 0
    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            buf += '|'
            i += 2
            continue
        if ch == '|':
            cells.append(buf.strip())
            buf = ''
            i += 1
            continue
        buf += ch
        i += 1
    cells.append(buf.strip())
    return cells


SEP = re.compile(r'^\s*\|?[\s:|-]+\|[\s:|-]*$')


def p_table(rows):
    ncol = max(len(r) for r in rows)
    total = 9300
    per = int(total / ncol)
    grid = ''.join('<w:gridCol w:w="%d"/>' % per for _ in range(ncol))
    sz = 17 if ncol <= 6 else (15 if ncol <= 9 else 13)
    trs = []
    for ri, row in enumerate(rows):
        tcs = []
        for ci in range(ncol):
            cell = row[ci] if ci < len(row) else ''
            rpr = ('<w:rFonts w:hint="eastAsia"/>%s<w:sz w:val="%d"/><w:szCs w:val="%d"/>'
                   % ('<w:b w:val="1"/>' if ri == 0 else '', sz, sz))
            fill = '<w:shd w:val="clear" w:color="auto" w:fill="F2F4F7"/>' if ri == 0 else ''
            ppr = ('<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F2F4F7"/>' if ri == 0 else '<w:pPr>')
            ppr += ('<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
                    '<w:jc w:val="left"/></w:pPr>')
            tcs.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr><w:p>%s%s</w:p></w:tc>'
                       % (per, fill, ppr, runs(cell, rpr)))
        trpr = '<w:trPr><w:tblHeader w:val="1"/></w:trPr>' if ri == 0 else '<w:trPr><w:cantSplit/></w:trPr>'
        trs.append('<w:tr>%s%s</w:tr>' % (trpr, ''.join(tcs)))
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
             '<w:top w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '<w:left w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '<w:bottom w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '<w:right w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '<w:insideH w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '<w:insideV w:val="single" w:color="CBCDD1" w:sz="6" w:space="0"/>'
             '</w:tblBorders><w:tblLayout w:type="autofit"/>'
             '<w:tblCellMar><w:top w:w="20" w:type="dxa"/><w:left w:w="70" w:type="dxa"/>'
             '<w:bottom w:w="20" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    return '<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>' % (tblpr, grid, ''.join(trs))


# ---------------- 主流程 ----------------
def main():
    raw = io.open(SRC_MD, 'rb').read().decode('utf-8')
    lines = raw.replace('\r\n', '\n').split('\n')

    body = []
    i = 0
    n = len(lines)
    stats = dict(h=0, p=0, tbl=0, tr=0, code=0, quote=0, list=0)
    last_was_tbl = False

    while i < n:
        t = lines[i]

        # 代码块
        if t.strip().startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            body.append(p_code(buf))
            stats['code'] += len(buf)
            last_was_tbl = False
            continue

        # 表格
        if t.lstrip().startswith('|'):
            rows = []
            while i < n and lines[i].lstrip().startswith('|'):
                if not SEP.match(lines[i]):
                    rows.append(split_row(lines[i]))
                i += 1
            if rows:
                if last_was_tbl:
                    body.append('<w:p><w:pPr><w:spacing w:after="0" w:line="120" w:lineRule="auto"/></w:pPr></w:p>')
                body.append(p_table(rows))
                body.append('<w:p><w:pPr><w:spacing w:before="0" w:after="60" w:line="120" w:lineRule="auto"/></w:pPr></w:p>')
                stats['tbl'] += 1
                stats['tr'] += len(rows)
            last_was_tbl = True
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', t)
        if m:
            lv = len(m.group(1))
            body.append(p_heading(lv, m.group(2).strip()))
            stats['h'] += 1
            last_was_tbl = False
            i += 1
            continue

        # 引用
        if t.startswith('>'):
            buf = []
            while i < n and lines[i].startswith('>'):
                s = lines[i][1:]
                if s.startswith(' '):
                    s = s[1:]
                buf.append(s)
                i += 1
            for s in buf:
                if s.strip():
                    body.append(p_quote(s))
                    stats['quote'] += 1
            last_was_tbl = False
            continue

        # 分隔线
        if re.match(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', t):
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="DDE1E6"/></w:pBdr>'
                        '<w:spacing w:before="80" w:after="80"/></w:pPr></w:p>')
            last_was_tbl = False
            i += 1
            continue

        # 列表
        m = re.match(r'^(\s*)([-*+]\s+|\d+[.)]\s+)(.*)$', t)
        if m:
            lead = len(m.group(1).replace('\t', '    '))
            lvl = min(lead // 2, 3)
            mark = m.group(2).strip()
            if re.match(r'^\d', mark):
                bullet = re.sub(r'[.)]$', '.', mark)
            else:
                bullet = '· '
            body.append(p_body(bullet + m.group(3), ind=240 + lvl * 240, after=40))
            stats['list'] += 1
            last_was_tbl = False
            i += 1
            continue

        # 空行
        if not t.strip():
            i += 1
            continue

        # 正文
        body.append(p_body(t))
        stats['p'] += 1
        last_was_tbl = False
        i += 1

    # 组装 document.xml（继承模板 sectPr）
    tpl = zipfile.ZipFile(TPL)
    tpl_doc = tpl.read('word/document.xml').decode('utf-8')
    si = tpl_doc.rfind('<w:sectPr')
    sect = tpl_doc[si:tpl_doc.rfind('</w:body>')]

    head = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
            'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
            'mc:Ignorable="w14"><w:body>')
    doc = head + ''.join(body) + sect + '</w:body></w:document>'

    # 跨 run 清洗：两个 run 各带一个 * 时，拼起来才成 **
    PARA = re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>', re.S)
    TT = re.compile(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)')
    fixed = [0]

    def fix_para(m):
        seg = m.group(0)
        ts = list(TT.finditer(seg))
        if len(ts) < 2:
            return seg
        old = ''.join(html.unescape(x.group(2)) for x in ts)
        new = scrub(old)
        if new == old:
            return seg
        out, last, first = [], 0, True
        for x in ts:
            out.append(seg[last:x.start()])
            content = new if first else ''
            out.append(x.group(1) + html.escape(content, quote=False) + x.group(3))
            first = False
            last = x.end()
        out.append(seg[last:])
        fixed[0] += 1
        return ''.join(out)

    doc = PARA.sub(fix_para, doc)

    # 打包
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    zout = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
    for item in tpl.infolist():
        data = tpl.read(item.filename)
        if item.filename == 'word/document.xml':
            data = doc.encode('utf-8')
        elif item.filename == 'docProps/core.xml':
            x = data.decode('utf-8')
            x = re.sub(r'<dc:title>.*?</dc:title>',
                       '<dc:title>《天神下凡》设定集 · 归纳整理版 v2.89</dc:title>', x, flags=re.S)
            x = re.sub(r'<dcterms:modified[^>]*>.*?</dcterms:modified>',
                       '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>' % now, x, flags=re.S)
            data = x.encode('utf-8')
        zout.writestr(item, data)
    zout.close()

    print('=== 生成 ===')
    print(' 源 md : %s (%s bytes, %d 行)' % (os.path.basename(SRC_MD), format(len(raw.encode('utf-8')), ','), len(lines)))
    print(' 输出  : %s (%s bytes)' % (os.path.basename(OUT), format(os.path.getsize(OUT), ',')))
    print(' document.xml : %s bytes' % format(len(doc.encode('utf-8')), ','))
    print(' 跨 run 清洗段落: %d' % fixed[0])
    print(' 标题 %d | 正文段 %d | 表格 %d (行 %d) | 引用行 %d | 列表 %d | 代码行 %d'
          % (stats['h'], stats['p'], stats['tbl'], stats['tr'], stats['quote'], stats['list'], stats['code']))


main()
