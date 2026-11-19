# -*- coding: utf-8 -*-
"""v2.16 导图同步：兵甲轴三条级名改判（只换级名，保留「枢机骑士团制式」等普通词）"""
import json, subprocess, sys

EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "sid_mwn8bwxf_yt8w7td7"

PAIRS = [
    ("兵甲只称粗坯／制式／名器／附魔／秘藏／传说／神铸",
     "兵甲只称粗坯／通造／具名／附魔／孤品／传说／神铸"),
    ("2 成器：制式 ↔ 匠杖", "2 成器：通造 ↔ 匠杖"),
    ("3 入级：名器 ↔ 呢喃", "3 入级：具名 ↔ 呢喃"),
    ("5 世不二出：秘藏 ↔ 咏叹", "5 世不二出：孤品 ↔ 咏叹"),
    ("2 位 成器｜制式 · 匠杖", "2 位 成器｜通造 · 匠杖"),
    ("3 位 入级｜名器 · 呢喃", "3 位 入级｜具名 · 呢喃"),
    ("5 位 世不二出｜秘藏 · 咏叹", "5 位 世不二出｜孤品 · 咏叹"),
    ("「秘藏级法杖」皆为误", "「孤品级法杖」皆为误"),
]

def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    return out.strip()

for find, repl in PAIRS:
    out = call("mind_find_replace_text", find=find, replace=repl)
    ok = '"count":1' in out or '"count": 1' in out
    print(("  OK  " if ok else "  ??  ") + find[:24] + " -> " + repl[-14:])
    if not ok:
        print("       " + out[:300])

print("\n=== 保存 ===")
print(call("save_file", file_path="E:/天神下凡/物品等级体系.xmind")[:400])
