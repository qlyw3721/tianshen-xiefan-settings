# -*- coding: utf-8 -*-
"""v2.92 修正：红桃牌=使徒红心花色（非地名）；赫尔曼狼群默认入红心十大军团。CRLF 写回。"""
import io

MD = "天神下凡设定集_归纳整理版_v2.91.md"
OUT = "天神下凡设定集_归纳整理版_v2.92.md"
lines = io.open(MD, "rb").read().decode("utf-8").split("\r\n")
print("原行数", len(lines))

# 1) 头部版本戳（仅头部两处）
stamp = ver = 0
for i, l in enumerate(lines[:12]):
    if l.startswith("> 更新时间戳") and "v2.91" in l:
        lines[i] = l.replace("v2.91", "v2.92"); stamp += 1
    if l.startswith("**版本**：v2.91"):
        lines[i] = l.replace("**版本**：v2.91", "**版本**：v2.92"); ver += 1
assert (stamp, ver) == (1, 1), (stamp, ver)

def rep_line(needle, old, new, tag):
    idx = [i for i, l in enumerate(lines) if needle in l]
    assert len(idx) == 1, (tag, len(idx))
    i = idx[0]
    assert old in lines[i], (tag, "old missing", lines[i][:100])
    lines[i] = lines[i].replace(old, new)
    print("  改", tag, "->", i + 1)

# 2) 归位总表第 6 项：去"待核"
rep_line("| 6 | 赫尔曼狼群／军团榜 |",
         "已有条目补全＋【用户裁定·待核】榜单表",
         "已有条目补全＋【用户裁定】红心（战争）花色十大军团榜",
         "总表第6项")

# 3) 军团段核查说明行：整行替换
rep_line("**四、军团榜（第 6 项）**", None, None, "") if False else None
idx = [i for i, l in enumerate(lines) if l.startswith("**四、军团榜（第 6 项）**")]
assert len(idx) == 1, ("军团段标题", len(idx))
h = idx[0]
assert "待核" in lines[h], lines[h]
lines[h] = "**四、军团榜（第 6 项·红心花色十大军团）**【用户裁定·入榜】"
print("  改 军团段标题 ->", h + 1)

# 该标题下第 2 行（空行后）为核查说明行
check_line = h + 2
assert "全库零命中" in lines[check_line] and "红桃牌大陆" in lines[check_line], lines[check_line][:120]
lines[check_line] = (
    "> **名字核查**：「赫尔曼狼群」在后传／前传／koaju_notes **全库零命中**（连「赫尔曼」亦为 0），"
    "交付原文仅称「被史诗大陆**称作**『赫尔曼狼群』的强大军团」——此为**史诗大陆的通称**，泰方正式番号原文未给、不编造，"
    "名字按交付照录【用户交付·原文补充】。"
    "**「红桃牌」＝使徒扑克牌的红心（红桃）花色，象征战争，不是地名**——原文 **L4288**「红色字母牌绘有大陆上最善战的大军团或者骑士团徽章，"
    "以泰坦帝国占席位最多」（§4.1 花色表在库）；用户裁定此军团**默认进入红心花色的十张字母牌＝大陆十大军团序列**，故非「待核地名」。"
)
print("  改 核查说明 ->", check_line + 1)

# 4) 榜单表第 1 行与第 2-10 行
r1 = [i for i, l in enumerate(lines) if l.startswith("| 1 | **「赫尔曼狼群」**")]
assert len(r1) == 1, ("榜单第1行", len(r1))
lines[r1[0]] = (
    "| 1 | **「赫尔曼狼群」**（泰坦） | 【用户交付·原文补充】名字照录、原文零命中；"
    "莱贝卡河战役阻挡黑玫瑰军团南下；【用户裁定】默认入**使徒牌红心（战争）十张字母牌＝大陆十大军团**，"
    "泰坦占席位最多之原文口径相符（L4288／§4.1） |"
)
print("  改 榜单第1行 ->", r1[0] + 1)

rrest = [i for i, l in enumerate(lines) if l.startswith("| 2–10 | **【待补】** | 用户本批只点名")]
assert len(rrest) == 1, ("榜单余席行", len(rrest))
lines[rrest[0]] = (
    "| 2–10 | **【待补】** | 红心字母牌共十张（L4288）；既有 §5.4「史诗大陆十大骑士团」表为**同花色榜的骑士团序列**，"
    "军团榜余席与本表**不互相填满、不静默合并**；用户本批只点名赫尔曼狼群一席，余九席留白 |"
)
print("  改 榜单余席行 ->", rrest[0] + 1)

# 5) 防误判行
fw = [i for i, l in enumerate(lines) if l.startswith("> **防误判**：① 序位 1 ") and "红桃牌大陆" in l]
assert len(fw) == 1, ("防误判行", len(fw))
lines[fw[0]] = (
    "> **防误判**：① 序位 1 **不等于**最强，仅为检索序；② 「赫尔曼狼群」（泰坦帝国军团·通称）≠ 黑玫瑰军团（澳狄斯亲王）≠ 中央军团乌尔库希部队（神圣帝国）；"
    "③ **红心（红桃）牌是花色不是地名**，「红桃牌大陆」为 v2.91 误读、本版撤销；④ 本榜（**军团**）与 §5.4「十大**骑士团**」同属红心字母牌，"
    "但序列不同、不互训；⑤ 红桃盒子／《红桃扑克密约》之「红桃」为器物／文书名，与花色象征不自动等同。"
)
print("  改 防误判行 ->", fw[0] + 1)

# 6) 块末"红桃牌大陆"待核表述
tail = [i for i, l in enumerate(lines) if "「红桃牌大陆」「二十席数目」「六军区」三项待核" in l]
assert len(tail) == 1, ("块末待核行", len(tail))
lines[tail[0]] = lines[tail[0]].replace(
    "「红桃牌大陆」「二十席数目」「六军区」三项待核／原创均留可驳标记",
    "「二十席数目」「六军区」两项原创留可驳标记（「红桃牌大陆」误读本版已撤销）"
)
print("  改 块末行 ->", tail[0] + 1)

# 7) 交叉引用补入 §4.1 花色表红心行
heart = [i for i, l in enumerate(lines) if l.startswith("| **红心** | 伴随鲜血的战争 |")]
assert len(heart) == 1, ("§4.1红心行", len(heart))
lines[heart[0]] = lines[heart[0]].rstrip() + "（**v2.92 交叉引用**：「赫尔曼狼群」【用户裁定】默认入此十席军团序列，见 §3.16 v2.91 归位块「四、军团榜」）"
print("  补 §4.1 红心行交叉引用 ->", heart[0] + 1)

io.open(OUT, "wb").write("\r\n".join(lines).encode("utf-8"))
b = io.open(OUT, "rb").read()
bare = b.count(b"\n") - b.count(b"\r\n")
print("写出", OUT, "行数", len(lines), "裸LF", bare)
assert bare == 0
