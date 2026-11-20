# -*- coding: utf-8 -*-
"""把 v2.51 面具块移到该小节防误判之后（避免误读为该节防误判的对象）"""
P = '天神下凡设定集_归纳整理版_v2.51.md'
s = open(P, 'rb').read().decode('utf-8').replace('\r\n', '\n')

start = s.index('#### v2.51 裁定｜救赎面具')
end_mark = '这世上戴着「救赎」的脸，一共有四张。**'
end = s.index(end_mark) + len(end_mark)
block = s[start:end]
assert block.count('#### v2.51 裁定｜救赎面具') == 1

# 剪掉（连同前面两个换行）
s2 = s[:start].rstrip('\n') + '\n\n' + s[end:].lstrip('\n')

anchor = '> **防误判**：「祭坛铠甲」「匣子」二件**无原文出处**，标【用户所给·原文待考】，不得冒充原文、不得据以续写具体情节。'
assert s2.count(anchor) == 1
s3 = s2.replace(anchor, anchor + '\n\n' + block)
print('moved ok')
open(P, 'wb').write(s3.replace('\n', '\r\n').encode('utf-8'))
