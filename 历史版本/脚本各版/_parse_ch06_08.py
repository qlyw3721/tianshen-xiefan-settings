# -*- coding: utf-8 -*-
import zipfile, xml.etree.ElementTree as ET, io

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SRC = 'D:/AI产出/宗教裁判所/宗教裁判所_第00{ch}章_分析.docx'

def text_of(el):
    return ''.join(t.text or '' for t in el.iter(NS + 't'))

for ch in ['6', '7', '8']:
    p = SRC.format(ch=ch)
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(NS + 'body')
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
    text = '\n'.join(out)
    dst = 'E:/天神下凡/_tmp_ch00%s_analysis.txt' % ch
    io.open(dst, 'w', encoding='utf-8').write(text)
    print('ch%s: %d lines, %d chars -> %s' % (ch, len(out), len(text), dst))

# 导出原文 L227 起
lines = io.open('E:/天神下凡/宗教裁判所.txt', 'r', encoding='utf-8-sig').read().split('\n')
with io.open('E:/天神下凡/_tmp_preq_l227_420.txt', 'w', encoding='utf-8') as f:
    for i in range(226, min(420, len(lines))):
        f.write('%4d| %s\n' % (i + 1, lines[i][:130]))
print('原文导出行数', min(420, len(lines)) - 226, '总行数', len(lines))
