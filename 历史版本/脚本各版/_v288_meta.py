# -*- coding: utf-8 -*-
"""v2.88 元信息同步：说明集戳 + 台账四行滚动 + 镜像"""
import io, shutil

# 1) 说明集：现行版本戳 v2.87 -> v2.88 + 登记行
P = '天神下凡设定集版本更新说明集.md'
L = io.open(P, encoding='utf-8').read().split('\n')
old = [i for i, l in enumerate(L) if l.startswith('> **现行版本**：**v2.87**')]
assert len(old) == 1, ('ex-version', len(old))
L[old[0]] = L[old[0]].replace('**v2.87**', '**v2.88**')
NEW = ['> **v2.88 登记**：占星阁夜谈（伊耶塔×马可伯特）／巫婆三弟子（蒂姆摩·阿加莎·德黑撒）／特殊感情裁定（非爱情）；名言 #167–#168；费舍二世入院长谱系；那不勒斯（渎神神学家·同名异人）；摩尼黑神学院／佛来堡大教堂／《番迪尔门教宗》登记；毕夏普水杯＋魔法阵总表 35 行。']
L[old[0]+1:old[0]+1] = NEW
io.open(P, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('说明集 ok')

# 2) 台账：四行滚动（同名标签只取每组第一条）
P2 = '设定集_裁定台账.md'
L2 = io.open(P2, encoding='utf-8').read().split('\n')
idx = {}
for i, l in enumerate(L2):
    for key in ('**当前版本**', '**上一版**', '**上上版**', '**历史版**'):
        if l.startswith('| ' + key + ' |') and key not in idx:
            idx[key] = i
assert len(idx) == 4, idx
cur, prev, prev2, hist = L2[idx['**当前版本**']], L2[idx['**上一版**']], L2[idx['**上上版**']], L2[idx['**历史版**']]
new_cur = '| **当前版本** | v2.88 | 2026-11-24 | 占星阁夜谈·巫婆三弟子·魔法阵总表 | 22,625 行／3,572,310 B |'
new_prev = cur
new_prev2 = prev
new_hist = prev2
L2[idx['**当前版本**']] = new_cur
L2[idx['**上一版**']] = new_prev
L2[idx['**上上版**']] = new_prev2
L2[idx['**历史版**']] = new_hist
io.open(P2, 'w', encoding='utf-8', newline='').write('\r\n'.join(L2))
print('台账 ok')

# 3) 镜像
shutil.copy2(P2, 'E:/天神下凡记忆与规则层/.workbuddy/设定集_裁定台账.md')
print('mirror ok')
