# -*- coding: utf-8 -*-
"""v2.23 导图同步：红阿育王 8 级由【推定·待裁】转【定稿】"""
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
    ("红阿育王（圣子阿育王傀儡｜8 级【推定·待裁】·v2.22）",
     "红阿育王（圣子阿育王傀儡｜8 级·大禁术方毁【定稿 v2.23】）"),
    ("黑阿育王／白阿育王（伊甸盖娅／上任牧首宠物｜7 级·v2.22）",
     "黑阿育王／白阿育王（伊甸盖娅／上任牧首宠物｜7 级·v2.22 定）"),
]

for old, new in pairs:
    out = call("mind_find_replace_text", find=old, replace=new)
    print(out[:200])

print("\n=== save ===")
print(call("save_file", file_path=FID)[:200])
