# -*- coding: utf-8 -*-
"""v2.31 关系网同步：新增「忏悔地·羔羊」分支"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/奥古斯丁关系网_六度分隔.xmind"


def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()


print("=== open ===")
print(call("open_file", file_path=FID, file_type="xmind", wait=True)[:300])

print("=== add parent ===")
out = call("mind_add_nodes", parent_id="n2",
           titles=["忏悔地·羔羊（神父—忏悔者 · 终身关系 · v2.31）"])
print(out[:500])

# 取新建节点 id
try:
    pid = json.loads(out.split("\n")[0]).get("node_ids", [None])[0]
except Exception:
    pid = None
print("pid =", pid)
if pid:
    print("=== add children ===")
    print(call("mind_add_nodes", parent_id=pid, titles=[
        "德黑撒（大占星师·忏悔者｜110 岁【用户裁定】）",
        "老克拉夫（彭龙纳·克拉夫·波洛克底｜忏悔者【推定·强】）",
        "二号房间老人（梵特兰蒂冈前馆长·大异端｜原文无名）",
        "制度五条：终身·单向·绝对保密·房号代名·不传承",
    ])[:500])
    print("=== save ===")
    print(call("save_file", file_path=FID)[:200])
