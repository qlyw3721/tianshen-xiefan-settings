# -*- coding: utf-8 -*-
"""v2.17 导图同步：生物等级体系加「位面维度」分支"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/生物等级体系.xmind"
ROOT = "7da654e3076d4bf1964cebc06e"
CALL_SUMMON = "fcb4b3751c7341028b2b9c3e1a"

def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()

# 1. 5 级分支的卡德科依加标注
print(call("mind_find_replace_text",
           find="卡德科依·水系魔兽（前传 L2805 熊形水元素兽）",
           replace="卡德科依·水系魔兽（前传 L2805 熊形水元素兽）★异位面")[:200])

# 2. 召唤规则分支下补三条
print(call("mind_add_nodes", parent_id=CALL_SUMMON, titles=[
    "两条通路：A 契约召唤（本世界物种·击败→契约）／B 位面召唤（异位面物种·亡魂·不签契约）",
    "位面归属＝与生物级正交的第二维度（1–11 不并入）",
    "11 级仍只召「象征」（L1921），位面条款不放宽",
])[:300])

# 3. 新建一级分支
r = call("mind_add_node", parent_id=ROOT, title="位面维度（v2.17 · 原文铁律 L2572）")
print(r[:300])
try:
    nid = json.loads(r).get("node_id") or json.loads(r).get("id")
except Exception:
    nid = None
print("新分支 id:", nid)

# 4. 其下挂五条
if nid:
    titles = [
        "原文铁律 L2572：召唤系魔法必然是从另一个位面强制降临生物或者亡魂（同一位面传输才是奇迹·L2657）",
        "异位面三方：天界（天堂·圣子 L1600）／黑暗位面·深渊（深渊物种·塔尔塔洛斯地狱 L5758）／未知位面（L6777）",
        "显形受限：L3855 深渊物种坍缩成十公分玩偶；L2805 卡德科依以污水为凭依",
        "卡德科依＝5 级＋异位面（前传 L2805）；不入 §1.8 生物库，只在 §8.0 七之二登记",
        "三段各管一段：位面归属说来源／生物级说强度／可召上限说权限",
    ]
    print(call("mind_add_nodes", parent_id=nid, titles=titles)[:400])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:200])
