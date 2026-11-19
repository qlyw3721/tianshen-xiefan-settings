# -*- coding: utf-8 -*-
"""v2.19 导图同步：阶位门槛改判 4 级"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/生物等级体系.xmind"
CALL_SUMMON = "fcb4b3751c7341028b2b9c3e1a"
GATE = "e318dc625164523a2fb748ce"


def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()


pairs = [
    ("阶位分水岭（v2.18 · 用户令）：能否开位面门＝低阶／高阶之分界",
     "阶位分水岭（v2.19 · 门槛 4 级）：能否开位面门＝低阶／高阶之分界"),
    ("1–6 级（原文低阶＋中阶）只走契约召唤：本世界物种",
     "1–3 级（低阶·宿根草）只走契约召唤：本世界物种"),
    ("7 级（高阶·剑蝶菊）起方可开位面门：异位面物种与亡魂【推定】",
     "4 级（中阶初位·一瓣紫百合）起方可开位面门：异位面物种与亡魂（用户裁定）"),
]
for a, b in pairs:
    print(call("mind_find_replace_text", find=a, replace=b)[:160])

print(call("mind_add_nodes", parent_id=GATE, titles=[
    "门槛≠天花板：4 级只获准开门，可召层级随阶上升（5 级上下→更高层→黄金亚种/巨龙→上帝左眼级）",
    "「低阶／高阶召唤师」＝行内能力俗称（未过／已过门槛），非徽章阶位，不与宿根草/剑蝶菊换算",
])[:300])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:200])
