# -*- coding: utf-8 -*-
import zipfile, re, sys, io
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = NS['w']

def para_text(p):
    return ''.join(t.text or '' for t in p.iter('{%s}t' % W)).strip()

def parse(path):
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    body = root.find('w:body', NS)
    out = []
    for child in body:
        tag = child.tag.split('}')[1]
        if tag == 'p':
            t = para_text(child)
            if t:
                out.append(t)
        elif tag == 'tbl':
            rows = []
            for tr in child.findall('w:tr', NS):
                cells = []
                for tc in tr.findall('w:tc', NS):
                    ct = ' '.join(para_text(p) for p in tc.findall('w:p', NS)).strip()
                    cells.append(ct)
                rows.append(' | '.join(cells))
            out.append('[TABLE]')
            out.extend(rows)
            out.append('[/TABLE]')
    return out

for n in range(16, 21):
    p = 'D:/AI产出/宗教裁判所/宗教裁判所第二卷分析/宗教裁判所_卷二·第%03d章_分析.docx' % n
    lines = parse(p)
    print('\n' + '='*90)
    print('### 第%03d章  段数=%d' % (n, len(lines)))
    print('='*90)
    for l in lines:
        print(l)
