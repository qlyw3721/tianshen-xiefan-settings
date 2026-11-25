# -*- coding: utf-8 -*-
import zipfile, xml.etree.ElementTree as ET, io

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
BASE = 'D:/AI产出/宗教裁判所/'

def text_of(el):
    return ''.join(t.text or '' for t in el.iter(NS + 't'))

# 第29章缺失跳过
for n in [26, 27, 28, 30]:
    p = BASE + '宗教裁判所_第%03d章_分析.docx' % n
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
    fn = '_tmp_ch%03d_analysis.txt' % n
    io.open(fn, 'w', encoding='utf-8').write(text)
    print('ch%03d: %d lines, %d chars -> %s' % (n, len(out), len(text), fn))

# 导出原文 L1102-1900 段（第25章止于L1101，第26章从L1102起）
lines = io.open('宗教裁判所.txt', 'r', encoding='utf-8-sig').read().split('\n')
with io.open('_tmp_preq_l1102_1900.txt', 'w', encoding='utf-8') as f:
    for i in range(1101, min(1900, len(lines))):
        f.write('%4d| %s\n' % (i + 1, lines[i]))
print('原文导出 L1102-1900, 实际末行', min(1900, len(lines)))
