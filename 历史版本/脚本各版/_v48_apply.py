# -*- coding: utf-8 -*-
SRC='天神下凡设定集_归纳整理版_V4.7.md'
OUT='天神下凡设定集_归纳整理版_V4.8.md'
blk=open('_v48_block.md',encoding='utf-8').read().replace('\r\n','\n').strip('\n')
raw=open(SRC,'rb').read().decode('utf-8')
assert raw.count('\r\n')==raw.count('\n'), '源稿非纯CRLF'
lines=raw.split('\r\n')

# 1) 插入补注块（### 4.7 前）
anchor='### 4.7 使徒牌五表总汇（v2.93 新建 · 归类归口 · 已有表只索引不重建）'
idx=[i for i,l in enumerate(lines) if l==anchor]
assert len(idx)==1,('anchor',len(idx))
i=idx[0]
assert lines[i-1].strip()=='', 'pre-anchor 非空'
lines=lines[:i]+blk.split('\n')+['']+lines[i:]

# 2) §5.3 阶位段补括注（唯一替换）
old='大骑士初试级数 10、中枢骑士 16，位于顶点的帝国六大骑士被誉为「圣棺骑士」，是 20 级左右徘徊的怪物，根本不屑配备任何勋章。圣棺骑士死后葬于'
new=('大骑士初试级数 10、中枢骑士 16（原文 L343 另以「**皇家2号骑士**」为 16 级之实例，'
 '称「高居**圣骑士阶段**」），位于顶点的帝国六大骑士被誉为「圣棺骑士」，是 20 级左右徘徊的怪物，'
 '根本不屑配备任何勋章——**「皇家2号骑士」（16 级，近侍编制）≠「帝国第二骑士」拉法叶（序位榜，前传 L333），两人不并**（v4.8）。'
 '圣棺骑士死后葬于')
hits=[j for j,l in enumerate(lines) if old in l]
assert len(hits)==1,('sec5.3',len(hits))
lines[hits[0]]=lines[hits[0]].replace(old,new)

# 3) V3.2 防误判① 补交叉
old2='前者是皇帝近侍／王室骑士团编制，后者是帝国荣誉序位榜，**不并、不互推**。'
new2=(old2+'**V4.8 补**：L343 原文另载其为「高居**圣骑士阶段**的 **16 级**骑士」——'
 '等级刻度是本块之外的**新事实**，「帝国第二骑士」原文未给级数；两者**编制／序位**之别不变，详见 §5.3 与 v4.8 块。')
h2=[j for j,l in enumerate(lines) if old2 in l]
assert len(h2)==1,('v3.2',len(h2))
lines[h2[0]]=lines[h2[0]].replace(old2,new2)

# 4) 封面与版本
c=[j for j,l in enumerate(lines) if '**V4.7**｜**版本号口径**' in l]
assert len(c)==1,('cover',len(c))
lines[c[0]]=lines[c[0]].replace('**V4.7**','**V4.8**')
v=[j for j,l in enumerate(lines) if l.startswith('**版本**：V4.7')]
assert len(v)==1,('ver',len(v))
lines[v[0]]='**版本**：V4.8（2026-11-27）'

data='\r\n'.join(lines)
open(OUT,'wb').write(data.encode('utf-8'))
r=open(OUT,'rb').read()
assert r.count(b'\n')==r.count(b'\r\n'),'裸LF'
print('ok bytes=%d lines=%d'%(len(r), r.count(b'\r\n')+1))
