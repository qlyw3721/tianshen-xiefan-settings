# -*- coding: utf-8 -*-
import zipfile, re, os
import xml.etree.ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
D=r'D:/AI产出/天神下凡DS/分析'
files=[f'天神下凡_卷二·第{n:03d}章_分析.docx' for n in list(range(91,101))]
out=[]
for f in files:
    p=os.path.join(D,f)
    if not os.path.exists(p):
        out.append(f'### MISSING {f}\n'); continue
    z=zipfile.ZipFile(p)
    xml=z.read('word/document.xml')
    root=ET.fromstring(xml)
    paras=[]
    for pnode in root.iter(W+'p'):
        s=''.join(t.text or '' for t in pnode.iter(W+'t'))
        paras.append(s)
    txt='\n'.join(paras)
    out.append('='*20+f' {f} '+'='*20)
    out.append(txt)
    out.append('')
open('_v46_raw.txt','w',encoding='utf-8').write('\n'.join(out))
print('done', len('\n'.join(out)))
