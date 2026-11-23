# -*- coding: utf-8 -*-
import io
F = "天神下凡设定集_归纳整理版_v2.61.md"
s = io.open(F, "r", encoding="utf-8", newline="").read().replace("\r\n", "\n")

old = "- **宗教裁判所特权**：【审判】、【裁夺】、【净化】，以及**专属奥古斯丁的【救赎】**。"
new = "- **宗教裁判所特权**：【审判】、【裁夺】、【净化】，以及**专属奥古斯丁的【救赎】**。（此行「宗教裁判所」为**用户所给原字**，所指为**梵特兰蒂冈异端裁决所**一侧——奥古斯丁是梵特兰蒂冈的人；**用字照录不改**，勿据此读成拜占奥侧，见下 v2.61 块「四、称谓三层」。）"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)

io.open(F, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n"))
print("PATCHED")
