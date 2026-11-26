# -*- coding: utf-8 -*-
"""解析《宗教裁判所》第二卷第1-5章分析 docx，输出纯文本供比对。"""
import io, os, zipfile, xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
SRC = r'D:/AI产出/宗教裁判所/宗教裁判所第二卷分析'


def text_of(el):
    return ''.join(t.text or '' for t in el.iter(W + 't'))


def parse(path):
    out = []
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    body = root.find('w:body', NS)
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            t = text_of(child).strip()
            if t:
                out.append(t)
        elif tag == 'tbl':
            for tr in child.findall('w:tr', NS):
                cells = [text_of(tc).strip() for tc in tr.findall('w:tc', NS)]
                out.append(' | '.join(cells))
    return out


for n in range(1, 6):
    p = os.path.join(SRC, '宗教裁判所_卷二·第%03d章_分析.docx' % n)
    lines = parse(p)
    dst = r'E:/天神下凡/_tmp_vol2_ch%03d_analysis.txt' % n
    io.open(dst, 'w', encoding='utf-8').write('\n'.join(lines))
    print('ch%03d -> %d lines, %d chars' % (n, len(lines), sum(len(x) for x in lines)))
