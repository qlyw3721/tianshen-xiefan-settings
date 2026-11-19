# -*- coding: utf-8 -*-
"""v2.18 导图同步：生物等级体系加「阶位分水岭」分支"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/生物等级体系.xmind"
CALL_SUMMON = "fcb4b3751c7341028b2b9c3e1a"


def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()


# 1. 上限节点加指针
print(call("mind_find_replace_text",
           find="上限：≤ 召唤师阶位（神明级为理论上限）",
           replace="上限：≤ 召唤师阶位（神明级为理论上限）｜阶位刻度见「阶位分水岭」")[:220])

# 2. 新增「阶位分水岭」节点
r = call("mind_add_node", parent_id=CALL_SUMMON, title="阶位分水岭（v2.18 · 用户令）：能否开位面门＝低阶／高阶之分界")
print(r[:300])
try:
    nid = json.loads(r).get("node_id") or json.loads(r).get("id")
except Exception:
    nid = None
print("新节点 id:", nid)

# 3. 其下挂三条
if nid:
    print(call("mind_add_nodes", parent_id=nid, titles=[
        "1–6 级（原文低阶＋中阶）只走契约召唤：本世界物种",
        "7 级（高阶·剑蝶菊）起方可开位面门：异位面物种与亡魂【推定】",
        "阶位刻度：前传 L2524（低阶宿根草／中阶紫百合／高阶剑蝶菊）＋后传 L664–L665（1–3／4–6／7–9）",
        "5 级门槛与阶位门槛并行不替代：前者管召什么，后者管谁能召",
    ])[:400])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:220])
