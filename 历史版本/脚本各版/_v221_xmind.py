# -*- coding: utf-8 -*-
"""v2.21 导图同步：梯度表四格由【推定】改【定稿 v2.21】"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/生物等级体系.xmind"


def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()


pairs = [
    ("低阶 1–3：A 5 级（单体·须先击败）｜B 无门【推定】",
     "低阶 1–3：A 5 级（单体·须先击败）｜B 无门【定稿 v2.21】"),
    ("中阶 4–6：A 6 级（区域霸主）｜B 5 级（低层异位面·卡德科依 L2805）【锚】",
     "中阶 4–6：A 6 级（区域霸主）【定稿 v2.21】｜B 5 级（低层异位面·卡德科依 L2805）【锚】"),
    ("高阶 7–9：A 7 级（成熟黄金亚种）｜B 7 级【推定】",
     "高阶 7–9：A 7 级（成熟黄金亚种）｜B 7 级【定稿 v2.21】"),
    ("逐阶上限梯度（v2.20 · 与 §8.0 一一对应；主表在 §5.2 v2.20 补记）",
     "逐阶上限梯度（v2.20 · 四推定格 v2.21 定稿；与 §8.0 一一对应；主表在 §5.2 v2.20 补记）"),
    ("纪律：上限是门槛非保底；超限是做不到而非禁令；本表不改任何生物级",
     "纪律：上限是门槛非保底；超限是做不到而非禁令；本表不改任何生物级｜定稿≠原文：定稿只表示本设定集采此数（v2.21）"),
]

for old, new in pairs:
    out = call("mind_find_replace_text", find=old, replace=new)
    print(out[:160])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:200])
