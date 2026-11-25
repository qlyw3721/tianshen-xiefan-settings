# -*- coding: utf-8 -*-
import zipfile, xml.etree.ElementTree as ET, io

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
BASE = 'D:/AI产出/宗教裁判所/宗教裁判所第一卷分析/'

def text_of(el):
    return ''.join(t.text or '' for t in el.iter(NS + 't'))

for n in [31, 32, 33, 34, 35]:
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

# 导出原文 L1329-2100 段（第30章止于L1328，第31章从L1329起）
lines = io.open('宗教裁判所.txt', 'r', encoding='utf-8-sig').read().split('\n')
with io.open('_tmp_preq_l1329_2100.txt', 'w', encoding='utf-8') as f:
    for i in range(1328, min(2100, len(lines))):
        f.write('%4d| %s\n' % (i + 1, lines[i]))
print('原文导出 L1329-2100, 实际末行', min(2100, len(lines)))
