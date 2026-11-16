# -*- coding: utf-8 -*-
"""校正 §0.6／§16 中原文 txt 的文件名引用（实际文件名无「_原著小说」后缀）。"""
import io

P = '天神下凡设定集_归纳整理版_v1.80.md'
raw = open(P, 'rb').read()
t = raw.decode('utf-8')
assert t.count('_原著小说.txt') == 4, t.count('_原著小说.txt')

t = t.replace('_原著小说.txt', '.txt')

ADD = (' **v1.80 文件名订正**：本条原写 `《天神下凡》_原著小说.txt`／`宗教裁判所_原著小说.txt`，'
       '与本机实际文件名不符，已按实际改为 `《天神下凡》.txt`／`宗教裁判所.txt`'
       '（sha 未变，仍为 `7950234a2f11785f`／`351bf2163181bdb8`），属路径更正、不影响任何引文与行号。')
ANCHOR = '（承 §0.6 第五款）。'
i = t.find('1. **「原文」口径**')
j = t.find(ANCHOR, i)
assert i > 0 and j > 0
t = t[:j + len(ANCHOR)] + ADD + t[j + len(ANCHOR):]

open(P, 'wb').write(t.encode('utf-8'))
b = open(P, 'rb').read().decode('utf-8')
print('LF', b.count('\n'), 'CRLF', b.count('\r\n'), '裸LF', b.count('\n') - b.count('\r\n'))
print('残留旧名', b.count('_原著小说'))
print('新名命中', b.count('《天神下凡》.txt'), b.count('宗教裁判所.txt'))
