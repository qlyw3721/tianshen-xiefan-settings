# -*- coding: utf-8 -*-
SRC='天神下凡设定集_归纳整理版_V4.6.md'
OUT='天神下凡设定集_归纳整理版_V4.7.md'
blk=open('_v47_block.md',encoding='utf-8').read().replace('\r\n','\n').strip('\n')
raw=open(SRC,'rb').read().decode('utf-8')
assert raw.count('\r\n')==raw.count('\n'), '源稿非纯CRLF'
lines=raw.split('\r\n')
anchor='### 4.7 使徒牌五表总汇（v2.93 新建 · 归类归口 · 已有表只索引不重建）'
idx=[i for i,l in enumerate(lines) if l==anchor]
assert len(idx)==1, ('anchor',len(idx))
i=idx[0]
assert lines[i-1].strip()=='', 'pre-anchor 非空'
new=blk.split('\n')
lines=lines[:i]+new+['']+lines[i:]
# 封面
c=[j for j,l in enumerate(lines) if '**V4.6**｜**版本号口径**' in l]
assert len(c)==1,('cover',len(c))
lines[c[0]]=lines[c[0]].replace('**V4.6**','**V4.7**')
v=[j for j,l in enumerate(lines) if l.startswith('**版本**：V4.6')]
assert len(v)==1,('ver',len(v))
lines[v[0]]='**版本**：V4.7（2026-11-27）'
data='\r\n'.join(lines)
open(OUT,'wb').write(data.encode('utf-8'))
raw2=open(OUT,'rb').read()
assert raw2.count(b'\n')==raw2.count(b'\r\n'), '裸LF'
print('ok bytes=%d lines=%d'%(len(raw2), raw2.count(b'\r\n')+1))
