# -*- coding: utf-8 -*-
import zipfile, os
import xml.etree.ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
D=r'D:/AI产出/天神下凡DS/分析'
files=['天神下凡_卷二·第101章_分析.docx','天神下凡_卷二·第102章_分析.docx']+\
      [f'天神下凡_卷三·第{n:03d}章_分析.docx' for n in range(1,6)]
out=[]
for f in files:
    p=os.path.join(D,f)
    if not os.path.exists(p):
        out.append(f'### MISSING {f}'); continue
    z=zipfile.ZipFile(p)
    root=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(t.text or '' for t in pn.iter(W+'t')) for pn in root.iter(W+'p')]
    out.append('='*20+f' {f} '+'='*20)
    out.append('\n'.join(paras)); out.append('')
txt='\n'.join(out)
open('_v47_raw.txt','w',encoding='utf-8').write(txt)
print('chars',len(txt),'lines',txt.count('\n'))
