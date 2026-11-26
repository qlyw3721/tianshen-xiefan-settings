# -*- coding: utf-8 -*-
import zipfile, io, sys, re
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
BASE = 'D:/AI产出/宗教裁判所/宗教裁判所第二卷分析/'
FILES = [
    ('第031章', '宗教裁判所_卷二·第031章_分析.docx'),
    ('第032章', '宗教裁判所_卷二·第032章_分析.docx'),
    ('第034章', '宗教裁判所_卷二·第034章_分析.docx'),
    ('第035章', '宗教裁判所_卷二·第035章_分析.docx'),
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
