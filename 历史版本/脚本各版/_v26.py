# -*- coding: utf-8 -*-
import io, os, shutil, hashlib

BASE = 'E:/天神下凡/'
SRC = BASE + '天神下凡设定集_归纳整理版_V2.5.md'
DOCX = BASE + '天神下凡设定集_归纳整理版_V2.5.docx'
DST = BASE + '天神下凡设定集_归纳整理版_V2.6.md'
ARCH = BASE + '历史版本/设定集各版/'

# ---------- 1. 归档 V2.5 原稿 ----------
raw = open(SRC, 'rb').read()
h0 = hashlib.sha256(raw).hexdigest()
assert b'\r\n' in raw and b'\n' not in raw.replace(b'\r\n', b''), 'SRC not CRLF'
arch_md = ARCH + '天神下凡设定集_归纳整理版_V2.5.md'
arch_docx = ARCH + '天神下凡设定集_归纳整理版_V2.5.docx'
assert not os.path.exists(arch_md) and not os.path.exists(arch_docx), 'archive target exists'
open(arch_md, 'wb').write(raw)
shutil.copy2(DOCX, arch_docx)
h1 = hashlib.sha256(open(arch_md, 'rb').read()).hexdigest()
h2 = hashlib.sha256(open(DOCX, 'rb').read()).hexdigest()
h3 = hashlib.sha256(open(arch_docx, 'rb').read()).hexdigest()
assert h0 == h1 and h2 == h3, ('archive hash mismatch', h0[:16], h1[:16], h2[:16], h3[:16])
print('archived V2.5 md', h0[:16], 'docx', h2[:16])

# ---------- 2. 改写 ----------
b = raw.decode('utf-8')
lines = b.split('\r\n')

def rep_line(old, new, tag):
    idx = [i for i, l in enumerate(lines) if old in l]
    assert len(idx) == 1, (tag, len(idx))
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)

rep_line('（GMT+8）｜**V2.5**｜', '（GMT+8）｜**V2.6**｜', 'stamp')
rep_line('**版本**：V2.5（2026-11-26）', '**版本**：V2.6（2026-11-26）', 'ver')

# 结构修复：L10252 撤回标记（按行插入，避免裸 LF）
old_row = '> 而 **9 = 4＋3＋2** 的结构本身是一张**知识地图**：**前 7 个考勤勉，后 2 个考眼界。**'
note = ('> **【v2.39 撤回·标记】** 上句「前 7 个考勤勉，后 2 个考眼界」之三层读法**已撤回**'
        '（L21392 ⑦：凡原文已给出「为了什么」，不得再为同一件事另造一层「为了什么」）。'
        '现行口径：**7 ＝ 4＋3 ＝ 两本基础书所覆盖的全部**；第三档 2 处原文条件是「让我惊讶」，为**加分项**，非「考眼界」。'
        '原句照录不删，仅加此标记（v2.6 补）。')
idx_r = [i for i, l in enumerate(lines) if l == old_row]
assert len(idx_r) == 1, ('retract row', len(idx_r))
r = idx_r[0]
assert lines[r+1] == '', 'expect blank after row'
lines[r+1:r+1] = ['>', note]

# 插入补注块
block = io.open(BASE + '_v26_block.md', encoding='utf-8').read().rstrip('\n')
anchor = '## 4. 使徒牌与帕雅战棋'
idx = [i for i, l in enumerate(lines) if l == anchor]
assert len(idx) == 1, ('anchor', len(idx))
i = idx[0]
assert lines[i-1] == '', 'no blank before anchor'
lines[i:i] = block.split('\n') + ['']

out = '\r\n'.join(lines)
assert '\n' not in out.replace('\r\n', ''), 'bare LF'
io.open(DST, 'w', encoding='utf-8', newline='').write(out)
os.remove(SRC)
print('OK lines', len(lines), 'bytes', len(out.encode('utf-8')))
