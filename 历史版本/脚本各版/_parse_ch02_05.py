# -*- coding: utf-8 -*-
import zipfile, xml.etree.ElementTree as ET, io

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def parse(p):
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(NS + 'body')
    def text_of(el):
        return ''.join(t.text or '' for t in el.iter(NS + 't'))
    out = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            out.append(text_of(child))
        elif tag == 'tbl':
            out.append('[TABLE]')
            for tr in child.findall(NS + 'tr'):
                cells = [text_of(tc).replace('\n', ' ') for tc in tr.findall(NS + 'tc')]
                out.append(' | '.join(cells))
            out.append('[/TABLE]')
    return '\n'.join(out)

for ch in range(2, 6):
    src = 'D:/AI产出/宗教裁判所/宗教裁判所_第%03d章_分析.docx' % ch
    txt = parse(src)
    dst = 'E:/天神下凡/_tmp_ch%03d_analysis.txt' % ch
    io.open(dst, 'w', encoding='utf-8').write(txt)
    print('ch%02d: %d lines / %d chars -> %s' % (ch, len(txt.split('\n')), len(txt), dst))
