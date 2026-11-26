# -*- coding: utf-8 -*-
"""V2.2 版本号口径切换：v2.109 → V2.2（小数点后只保留 1 位）
只改版本号与文件名，不动任何设定内容；CRLF 保持。
"""
import io, os, re

BASE = 'E:/天神下凡/'
OLD_MD = BASE + '天神下凡设定集_归纳整理版_v2.109.md'
NEW_MD = BASE + '天神下凡设定集_归纳整理版_V2.2.md'
OLD_DX = BASE + '天神下凡设定集_归纳整理版_v2.109.docx'
NEW_DX = BASE + '天神下凡设定集_归纳整理版_V2.2.docx'

b = io.open(OLD_MD, 'rb').read()
assert b.count(b'\n') == b.count(b'\r\n'), 'CRLF broken before edit'
S = b.decode('utf-8').split('\r\n')
print('行数', len(S))

# --- 1) 封面时间戳行（L4）：改版本号 + 立口径 ---
old4 = S[3]
assert old4.startswith('> 更新时间戳：2026-11-26'), old4[:60]
assert '**v2.109**' in old4
new4 = old4.replace(
    '**v2.109**',
    '**V2.2**｜**版本号口径**：依用户 2026-11-26 令，自本版起版本号**只保留小数点后 1 位**'
    '（V2.2 → V2.3 … V2.9 → V3.0）；原 v1.0–v2.109 序列**保留原编号、不回溯改名**',
    1)
assert new4 != old4
S[3] = new4

# --- 2) 版本行（L6）---
old6 = S[5]
assert old6 == '**版本**：v2.109（2026-11-26）', repr(old6)
S[5] = '**版本**：V2.2（2026-11-26）'

# --- 3) 本次补注块标题：保留原编号溯源 ---
hit = [i for i, s in enumerate(S) if s.startswith('#### v2.109 补注｜')]
assert len(hit) == 1, hit
S[hit[0]] = S[hit[0]].replace('#### v2.109 补注｜', '#### V2.2（原 v2.109）补注｜', 1)

io.open(NEW_MD, 'w', encoding='utf-8', newline='').write('\r\n'.join(S))

# --- 4) 旧 md / docx 退场（docx 待重生后删）---
os.remove(OLD_MD)
if os.path.exists(OLD_DX):
    os.rename(OLD_DX, OLD_DX + '.old')

# --- 5) 制稿脚本三处版本号 ---
p = BASE + '_md2docx.py'
s = io.open(p, 'r', encoding='utf-8', newline='').read()
assert s.count('v2.109') == 3, s.count('v2.109')
s = s.replace('天神下凡设定集_归纳整理版_v2.109.md', '天神下凡设定集_归纳整理版_V2.2.md')
s = s.replace('天神下凡设定集_归纳整理版_v2.109.docx', '天神下凡设定集_归纳整理版_V2.2.docx')
s = s.replace('归纳整理版 v2.109</dc:title>', '归纳整理版 V2.2</dc:title>')
assert 'v2.109' not in s, 'residual v2.109 in _md2docx.py'
io.open(p, 'w', encoding='utf-8', newline='').write(s)

print('封面 L4 →', S[3][:150])
print('封面 L6 →', S[5])
print('块标题 →', S[hit[0]][:110])
print('md/docx 改名完成，_md2docx.py 三处已同步')
