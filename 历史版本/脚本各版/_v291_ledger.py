# -*- coding: utf-8 -*-
"""v2.91 台账同步（只跑台账，说明集已由 _v291_meta.py 写入）。CRLF 写回。"""
import io

L = "设定集_裁定台账.md"
t = io.open(L, "rb").read().decode("utf-8").split("\r\n")

# 当前版本行：取第一条
cur = [i for i, l in enumerate(t) if l.startswith("| **当前版本** |")]
assert cur, "当前版本行缺失"
i = cur[0]
assert "v2.90" in t[i]
t[i] = ("| **当前版本** | v2.91 | 2026-11-25 | 后传脉代奥拉三年岁月段二十项分类归位·主角18岁核定＋5项原创表＋2项改名核查 | "
        "22,827 行／3,604,285 B |")
print("当前版本行 ->", i + 1)

# 上一版行：取第一条（紧跟当前版本之后的留档）
prev = [i for i, l in enumerate(t) if l.startswith("| **上一版** |")]
assert prev, "上一版行缺失"
j = prev[0]
t[j] = ("| **上一版** | 本机 **v2.90**（第一百三十轮·**后传拥抱段十一项分类归位**：后传 L2821–L2862"
        "整段本机命中，5 项新立（密特朗冰龙涎香／海因甸部落／维腾堡公爵夫人画作+历史人物／木乃伊法老术·卡劳玛炼金干尸／黑暗果实）"
        "＋6 项升格确认（玻璃杯神祗伏笔／沉默名言 §1.7 第145条／逻辑实证侧描／关系伏笔等）；两处旧判定（画作 v1.25 排除·名言候选）明写处置不静默覆盖）"
        "——本版升 v2.91 后归档，22,690 行／3,587,869 B |")
print("上一版行 ->", j + 1)

io.open(L, "wb").write("\r\n".join(t).encode("utf-8"))
b = io.open(L, "rb").read()
print("裸LF", b.count(b"\n") - b.count(b"\r\n"))
assert b.count(b"\n") == b.count(b"\r\n")
