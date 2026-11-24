# -*- coding: utf-8 -*-
import os, shutil, io

# 归档本轮脚本（含部分执行的失败脚本，历史一律保留）
for f in ['_v275_apply.py', '_v275_meta.py', '_v275_meta2.py']:
    if os.path.exists(f):
        shutil.move(f, '历史版本/脚本各版/' + f)
print('脚本归档 OK')

root = '历史版本'
cnt = {}
sz_all = 0
for d in os.listdir(root):
    p = os.path.join(root, d)
    if os.path.isdir(p):
        n = 0
        for r, dd, fs in os.walk(p):
            for x in fs:
                n += 1
                sz_all += os.path.getsize(os.path.join(r, x))
        cnt[d] = n
tot = sum(cnt.values())
print('分项', cnt)
print('合计', tot, '件 / %.1f MB' % (sz_all / 1024 / 1024))

p = '历史版本/00_归档索引.md'
L = io.open(p, encoding='utf-8').read().split('\n')
for i, l in enumerate(L):
    if l.startswith('| `设定集各版'):
        L[i] = l.replace('`v2.73`', '`v2.74`').replace('| 165 |', '| %d |' % cnt['设定集各版'])
    if l.startswith('| `脚本各版'):
        L[i] = l.replace('| 206 |', '| %d |' % cnt['脚本各版'])
    if '合计 589 件' in l:
        L[i] = (
            '**合计 %d 件／%.1f MB**（v2.75 收口新增 5 件：设定集 v2.74 md／docx 2、落盘脚本 3）'
            '（另有工具模板 `_tpl_base_v1.77.docx` 一件，**不是历史版本**，为本文件夹下的 docx 生成模板，'
            '`_md2docx.py` 按固定路径读取，**勿移动**）。' % (tot, sz_all / 1024 / 1024)
        )
io.open(p, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('索引更新 OK')
