# -*- coding: utf-8 -*-
"""v2.91 落盘：头部戳 + 集中归位块 + 已有条目单行补锚。CRLF 写回。"""
import io

MD = "天神下凡设定集_归纳整理版_v2.90.md"
OUT = "天神下凡设定集_归纳整理版_v2.91.md"
BLOCK = "_v291_block.md"

raw = io.open(MD, "rb").read().decode("utf-8")
lines = raw.split("\r\n")
print("原行数", len(lines))

# 1) 头部版本戳：仅第 1 个「> 更新时间戳」行与「**版本**」行
stamp = 0
ver = 0
for i, l in enumerate(lines[:12]):
    if l.startswith("> 更新时间戳") and "v2.90" in l:
        lines[i] = l.replace("v2.90", "v2.91"); stamp += 1
    if l.startswith("**版本**：v2.90"):
        lines[i] = l.replace("**版本**：v2.90", "**版本**：v2.91"); ver += 1
assert stamp == 1, ("stamp", stamp)
assert ver == 1, ("ver", ver)

def set_sub(needle, old, new, tag):
    """单行内唯一子串替换"""
    idx = [i for i, l in enumerate(lines) if needle in l]
    assert len(idx) == 1, (tag, len(idx))
    i = idx[0]
    assert old in lines[i], (tag, "old not found", lines[i][:120])
    lines[i] = lines[i].replace(old, new)
    print("  补锚", tag, "->", i + 1)

# 2) 已有条目单行补锚（改 OUT 中 v2.91 文本；轻微补字，不重建块）
# 赫尔曼狼群：仅存名称 -> 补军团属性（用户交付）
set_sub("| **「赫尔曼狼群」** | 世俗组织，泰坦帝国。 |",
        "世俗组织，泰坦帝国。",
        "世俗组织，泰坦帝国；**军团**（【用户交付·原文补充】后传「脉代奥拉三年岁月」段；莱贝卡河战役阻挡黑玫瑰军团）",
        "赫尔曼狼群")
# 中央军团乌尔库希：仅存名称 -> 补庞培家族传统落点
set_sub("| **中央军团乌尔库希部队** | 仅存名称。 |",
        "仅存名称。",
        "仅存名称；【用户交付·原文补充】庞培家族「继承人从小丢军队」传统落点——尼禄之父九岁被其父扔入本部队",
        "乌尔库希")

# 3) 插入集中块：在 v2.90 块尾「本块不写续写正文」行之后、v2.02 标题之前
anchor = "#### v2.02 补注｜莱茵哈泰深化人物志"
idx = [i for i, l in enumerate(lines) if l.startswith(anchor)]
assert len(idx) == 1, ("anchor v2.02", len(idx))
pos = idx[0]
block_raw = io.open(BLOCK, "rb").read().decode("utf-8")
block_lines = block_raw.split("\n")
# block 文件本身是 LF；写回统一 CRLF。块前须有空行、块后须有空行（v2.02 标题前）。
insert = block_lines + [""]
# 若 pos-1 行为空行则不再额外加；确保块与前文之间恰一空行
assert lines[pos - 1].strip() == "", ("prev not blank", repr(lines[pos - 1][:60]))
lines[pos:pos] = insert
print("集中块插入于", pos + 1, "块行数", len(insert))

io.open(OUT, "wb").write("\r\n".join(lines).encode("utf-8"))
# 裸 LF 检查
b = io.open(OUT, "rb").read()
bare = b.count(b"\n") - b.count(b"\r\n")
print("写出", OUT, "行数", len(lines), "裸LF", bare)
assert bare == 0
