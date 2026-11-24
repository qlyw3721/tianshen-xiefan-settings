# -*- coding: utf-8 -*-
"""v2.73 归档：本轮脚本入脚本各版；重算历史版本索引。"""
import io, os, shutil

BASE = 'E:/天神下凡/'
HIST = BASE + '历史版本/'

# 1. 本轮落盘脚本入脚本各版
for name in ['_v273_apply.py', '_v273_apply2.py', '_v273_meta.py', '_v273_ledger.py']:
    src = BASE + name
    if os.path.exists(src):
        shutil.move(src, HIST + '脚本各版/' + name)
        print('moved', name)

# 2. 重算各子目录件数
dirs = ['设定集各版', '备份_bak', '脚本各版', '配套旧版', '推导稿', '重复副本', 'svg']
counts = {}
total, size = 0, 0
for d in dirs:
    n = 0
    for r, ds, fs in os.walk(HIST + d):
        for f in fs:
            n += 1
            size += os.path.getsize(os.path.join(r, f))
    counts[d] = n
    total += n
print('counts', counts, 'total', total, 'MB', round(size / 1024 / 1024, 1))

# 3. 更新索引
p = HIST + '00_归档索引.md'
L = io.open(p, encoding='utf-8').read().split('\n')
for i, l in enumerate(L):
    for d in dirs:
        if l.startswith('| `' + d + '\\`'):
            # 保留前半，替换末尾数字
            parts = l.split('|')
            parts[-2] = ' ' + str(counts[d]) + ' '
            L[i] = '|'.join(parts)
    if l.startswith('**合计 '):
        L[i] = ('**合计 %d 件／%.1f MB**（v2.73 收口新增 6 件：设定集 v2.72 md／docx 2、落盘脚本 4）'
                '（另有工具模板 `_tpl_base_v1.77.docx` 一件，**不是历史版本**，为本文件夹下的 docx 生成模板，`_md2docx.py` 按固定路径读取，**勿移动**）。'
                % (total, size / 1024 / 1024))
io.open(p, 'w', encoding='utf-8', newline='').write('\r\n'.join(L))
print('索引已更新')
