# -*- coding: utf-8 -*-
"""v2.20 导图同步：阶位分水岭下增「逐阶上限梯度」"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/生物等级体系.xmind"
GATE = "e318dc625164523a2fb748ce"


def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()


# 1. 改「上限」指针节点
print(call("mind_find_replace_text",
           find="上限：≤ 召唤师阶位（神明级为理论上限）｜阶位刻度见「阶位分水岭」",
           replace="上限：≤ 召唤师阶位上限｜逐阶数字见「逐阶上限梯度（v2.20）」")[:200])

# 2. 新增父节点
print(call("mind_add_nodes", parent_id=GATE, titles=[
    "逐阶上限梯度（v2.20 · 与 §8.0 一一对应；主表在 §5.2 v2.20 补记）",
])[:300])

# 3. 取父节点 id
out = call("mind_get_info")
d = json.loads(out)


def walk(n, depth=0):
    if n.get("title", "").startswith("逐阶上限梯度"):
        return n.get("id")
    for c in n.get("children", []):
        r = walk(c, depth + 1)
        if r:
            return r
    return None


pid = walk(d["tree"])
print("父节点 id =", pid)

kids = [
    "口径：下限恒 5 级（4 级及以下不可召）；A＝契约召唤（本世界）／B＝位面召唤（异位面·须 4 级起）",
    "低阶 1–3：A 5 级（单体·须先击败）｜B 无门【推定】",
    "中阶 4–6：A 6 级（区域霸主）｜B 5 级（低层异位面·卡德科依 L2805）【锚】",
    "高阶 7–9：A 7 级（成熟黄金亚种）｜B 7 级【推定】",
    "大魔法师 10–16：A 8–9 级｜B 8–9 级（L4068 冰霜巨龙·L1659 九阶媲美巨龙）【锚】",
    "贤者 17–20：A 10 级｜B 10 级（神话生物·最高阶上限）【锚·§8.0】",
    "11 级不列本表：任何过门槛者皆只召其「象征」（L1921），非实力",
    "纪律：上限是门槛非保底；超限是做不到而非禁令；本表不改任何生物级",
]
print(call("mind_add_nodes", parent_id=pid, titles=kids)[:400])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:200])
