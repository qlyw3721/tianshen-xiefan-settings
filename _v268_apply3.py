# -*- coding: utf-8 -*-
"""v2.68 Part C：微调 + 升版 + 说明集 + 台账"""
import io

P = "天神下凡设定集_归纳整理版_v2.67.md"
lines = io.open(P, encoding="utf-8", newline="").read().split("\r\n")

def rep_line(prefix, new, tag):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, "[%s] %d" % (tag, len(idx))
    lines[idx[0]] = new

# A3.3 标题
rep_line("**A3.3 伊甸盖娅·弟弟：剧情挂起与「尾巴」留档（v1.72 第十轮",
 "**A3.3 伊甸盖娅·弟弟：剧情挂起与「尾巴」留档（v1.72 第十轮 · 用户裁定 · **v2.68 复原伏笔**）**",
 "t33")

# A3.3 状态行
rep_line("| 状态 | **挂起·未闭合**。秘密内容、弟弟成年身份与最终去向",
 "| 状态 | **挂起·未闭合**。秘密**存在但内容未揭**（L6854）；弟弟成年身份、最终去向、后续剧情**一律留白**，待用户以后补充；本版不填、不猜、不推演、不写续写正文。 |",
 "st33")

# A3.3 第十轮注后加 v2.68 注
idx = [i for i, l in enumerate(lines) if l.startswith("> **v1.72 第十轮注（本条状态：挂起）**")]
assert len(idx) == 1
NEW = "> **v2.68 注（状态不变，性质更正）**：v2.64 曾把 L6854 判为伪引、把「尾巴」改称「留白」——**v2.68 回读该行，句子确实存在**：「至于你弟弟，我可以帮你保守那个惊人的秘密，但是老师死后，小猫咪就要归我了。」故：**① 伏笔成立**（原文埋了、未揭）；**② 挂起不变**（用户令「以后补充」仍有效）；**③ 秘密内容仍留白**；**④ 不得再称「伪引」**。见 §3.7 A3.6 卷九 9.3 与附录 A **T-25（已结案）**。"
lines.insert(idx[0] + 1, "")
lines.insert(idx[0] + 2, NEW)

# A3.6 对应表加两行
rep_line("| 卷十 · 写作纪律 |",
 "| 卷六之二 · 与主角的羁绊线 | 无专条（A3 主条「情感弧线」一句） | **v2.68 新补**：六阶段纵线＋三处易错＋双向留白 |\n| 卷九之二 · 后续剧情线预测 | 无专条 | **v2.68 新补**：五条预测线＋弟弟线（原文伏笔）＋五条边界 |\n| 卷十 · 写作纪律 |",
 "maptbl")

# 版本号
idx = [i for i, l in enumerate(lines) if "**v2.67**" in l and l.startswith("> 更新时间戳")]
assert len(idx) == 1
lines[idx[0]] = lines[idx[0]].replace("**v2.67**", "**v2.68**")
idx2 = [i for i, l in enumerate(lines) if l.startswith("**版本**：v2.67（2026-11-23）")]
assert len(idx2) == 1
lines[idx2[0]] = "**版本**：v2.68（2026-11-23）"

io.open(P, "w", encoding="utf-8", newline="").write("\r\n".join(lines))
print("md OK lines=", len(lines))
