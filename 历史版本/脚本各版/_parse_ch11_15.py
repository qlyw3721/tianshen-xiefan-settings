# -*- coding: utf-8 -*-
"""解析第11-15章分析docx，用标准库zip+ElementTree保留表格结构"""
import zipfile, xml.etree.ElementTree as ET, io, os

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def parse_docx(path):
    z = zipfile.ZipFile(path)
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
    return out

for ch in range(11, 16):
    p = r'D:/AI产出/宗教裁判所/宗教裁判所_第%03d章_分析.docx' % ch
    if not os.path.exists(p):
        print('MISSING', p)
        continue
    lines = parse_docx(p)
    outp = '_tmp_ch%03d_analysis.txt' % ch
    io.open(outp, 'w', encoding='utf-8').write('\n'.join(lines))
    print('CH%02d: %d lines, %d chars -> %s' % (ch, len(lines), sum(len(x) for x in lines), outp))

# 导出原文 L421 起（第8章止于L420，第9/10章未提供，定位第11章起始）
L = io.open('宗教裁判所.txt', 'r', encoding='utf-8-sig').read().split('\n')
with io.open('_tmp_preq_l421_700.txt', 'w', encoding='utf-8') as f:
    for i in range(420, min(700, len(L))):
        f.write('%4d| %s\n' % (i+1, L[i][:130]))
print('原文 L421-700 导出完成')
