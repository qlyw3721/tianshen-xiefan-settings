# -*- coding: utf-8 -*-
import zipfile, io, sys, re
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
BASE = 'D:/AI产出/宗教裁判所/宗教裁判所第二卷分析/'
FILES = [
    ('第036章', '宗教裁判所_卷二·第036章_分析.docx'),
    ('第037章', '宗教裁判所_卷二·第037章_分析.docx'),
    ('第038章', '宗教裁判所_卷二·第038章_分析.docx'),
    ('第039章', '宗教裁判所_卷二·第039章_分析.docx'),
    ('第040章', '宗教裁判所_卷二·第040章_分析.docx'),
    ('第041章', '宗教裁判所_卷二·第041章_分析.docx'),
    ('第042章', '宗教裁判所_卷二·第042章_分析.docx'),
    ('第043章', '宗教裁判所_卷二·第043章_分析.docx'),
    ('第044章', '宗教裁判所_卷二·第044章_分析.docx'),
    ('外篇1方块Q', '宗教裁判所_外篇1_方块Q.docx'),
]

def para_text(p):
    out = []
    for t in p.iter(W + 't'):
        out.append(t.text or '')
    return ''.join(out).strip()

def dump(path):
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    body = root.find(W + 'body')
    lines = []
    for el in body:
        tag = el.tag
        if tag == W + 'p':
            s = para_text(el)
            if s:
                lines.append(s)
        elif tag == W + 'tbl':
            rows = []
            for tr in el.findall(W + 'tr'):
                cells = []
                for tc in tr.findall(W + 'tc'):
                    txt = ' '.join([para_text(p) for p in tc.findall(W + 'p') if para_text(p)])
                    cells.append(txt)
                rows.append(' | '.join(cells))
            lines.append('[TABLE]')
            lines.extend(['  ' + r for r in rows])
            lines.append('[/TABLE]')
    return lines

for label, fn in FILES:
    print('\n' + '=' * 70)
    print('###', label, fn)
    print('=' * 70)
    try:
        for ln in dump(BASE + fn):
            print(ln)
    except Exception as e:
        print('ERR', e)
