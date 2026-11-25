# -*- coding: utf-8 -*-
import io, re
F = 'E:/天神下凡/天神下凡设定集_归纳整理版_v2.99.md'
L = io.open(F, 'r', encoding='utf-8', newline='').read().split('\r\n')

GROUPS = {
 '第6章0命中变体': ['笼子.*咬','咬人','兔子','兰花','人妖','娘娘腔','混吃等死','九条命','杀死.*猫',
   '澳狄斯.*女儿','女儿.*轮椅','螺旋.*大理石','大理石楼梯','水晶吊灯','莱因哈特',
   '十一幅肖像','十一.*肖像','肖像.*十一'],
 '第7章0命中变体': ['三曲腿','三曲枝','三曲.*螺旋','螺旋图','六层.*罗盘','罗盘.*六层',
   '思想.*巨人','行动.*侏儒','巨人.*侏儒','一粒.*希望','希望.*种子','种子.*希望',
   '食言','陌生的名字','陌生.*名字','神秘女人','究竟是谁',' wondering'],
 '第8章0命中变体': ['正式骑士','出生.*骑士','骑士.*出生','司宗谱','纹章官','谱纹章',
   '液态.*标本','标本','第七骑士','第七.*骑士','六层楼','六楼.*窗','跳窗'],
}
for sec, kws in GROUPS.items():
    print('\n===== %s =====' % sec)
    for kw in kws:
        hits = [i+1 for i, l in enumerate(L) if re.search(kw, l)]
        print('%-22s %s' % (kw, ('0' if not hits else '%d first=%d' % (len(hits), hits[0]))))
    print()

# P014 家族代数、P015 祖父身份 既有落点上下文
print('===== 代数12/14/11 既有 =====')
for i, l in enumerate(L):
    if re.search(r'12/14|12 代|14 代|十一幅.*代|代数', l) and ('待裁' in l or '挂起' in l or '两存' in l):
        print('%d| %s' % (i+1, l[:300]))
print('\n===== 祖父身份既有 =====')
for i, l in enumerate(L):
    if re.search(r'祖父', l) and re.search(r'潘多拉', l):
        print('%d| %s' % (i+1, l[:300]))
