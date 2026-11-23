# -*- coding: utf-8 -*-
"""v2.70 归档：根目录只留最新版，其余一律移入 历史版本\\ 六类子目录。"""
import os, re, shutil, io

ROOT = "."
HIST = "历史版本"

DIRS = {
    "set":   os.path.join(HIST, "设定集各版"),
    "bak":   os.path.join(HIST, "备份_bak"),
    "py":    os.path.join(HIST, "脚本各版"),
    "extra": os.path.join(HIST, "配套旧版"),
    "draft": os.path.join(HIST, "推导稿"),
    "dup":   os.path.join(HIST, "重复副本"),
}
for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

SET_RE = re.compile(r"^天神下凡设定集_归纳整理版_v[0-9].*\.(md|docx)$")
PY_RE  = re.compile(r"^_v\d{3}_.*\.py$")

KEEP = set("""
天神下凡设定集_归纳整理版_v2.70.md
天神下凡设定集_归纳整理版_v2.70.docx
天神下凡设定集版本更新说明集.md
天神下凡设定集版本更新说明集.docx
设定集_裁定台账.md
双机同步_云盘同步目录清单.md
宗教裁判所.txt
《天神下凡》.txt
天神下凡_世界地图_v1.1.svg
天神下凡_神圣帝国示意图_v1.2.svg
奥古斯丁关系网_六度分隔.xmind
拜占奥教廷_组织架构图.xmind
梵特兰蒂冈教廷_组织架构图.xmind
物品等级体系.xmind
生物等级体系.xmind
_preflight.py
_rzz.py
_verify_fact.py
_v251_struct.py
_md2docx.py
_md2docx_hist.py
_lib_sync.py
_lib_upload_md.py
_lib_upload_svg.py
_lib_overwrite.py
_gen_empire_map_v12.py
make_epub.py
_svg_overlap.py
kaoju_notes.txt
天神下凡.epub
宗教裁判所（前传）.epub
天神下凡_游戏大纲_v0.3.md
天神下凡_游戏大纲_v0.3.docx
天神下凡_角色与座主详设_v0.4.md
天神下凡_角色与座主详设_v0.4.docx
天神下凡_续写正文_第一辑.md
_v270_apply.py
.gitattributes
.gitignore
.lib_sync_state.json
""".split())

EXTRA_ROOT = {
    "天神下凡_世界地图_v1.0.svg",
    "天神下凡_神圣帝国示意图_v1.0.svg",
    "天神下凡_神圣帝国示意图_v1.1.svg",
    "天神下凡_创作参考库_v1.2.md",
    "天神下凡_游戏大纲_v0.3_合并前备份.md",
    "天神下凡_游戏大纲_v0.3_合并前备份.docx",
    "天神下凡_角色与座主详设_v0.4_首版备份.md",
    "逆位教皇_游戏大纲_v0.2.md",
    "逆位教皇_游戏大纲_v0.2.docx",
}
DUP_ROOT = {
    "天神下凡_八百万字完本总纲.md",
    "续写《天神下凡》之规则_v1.0.md",
}
PY_EXTRA = {"_map_v11.py", "_merge_v166.py", "_p3_apply.py", "_p3_blocks.py",
            "_gen_empire_map.py", "_gen_empire_map_v11.py"}

plan = []          # (src, dst_dir, tag)


def add(src, key, tag):
    plan.append((src, DIRS[key], tag))


# ---------- 根目录 ----------
for f in sorted(os.listdir(ROOT)):
    if not os.path.isfile(f) or f in KEEP:
        continue
    if SET_RE.match(f):
        add(f, "set", "设定集各版")
    elif f.startswith("_bak_"):
        add(f, "bak", "回滚备份")
    elif PY_RE.match(f) or f in PY_EXTRA:
        add(f, "py", "逐版脚本")
    elif f in EXTRA_ROOT:
        add(f, "extra", "配套旧版")
    elif f in DUP_ROOT:
        add(f, "dup", "重复副本")
    elif f.startswith("_人物志其三_"):
        add(f, "draft", "推导稿")
    else:
        raise SystemExit("UNCLASSIFIED: " + f)

# ---------- 历史版本内既有文件（扁平归一） ----------
HIST_SET = {"天神下凡设定集_归纳整理版_v1.0.md",
            "天神下凡设定集_归纳整理版_v1.0.docx",
            "天神下凡设定集_归纳整理版_v1.1.md",
            "天神下凡设定集_归纳整理版_v1.1.docx"}
HIST_EXTRA = {"天神下凡_游戏大纲_v0.1.md",
              "天神下凡_游戏大纲_v0.1.docx",
              "天神下凡_六百万字完本总纲_v1.2备份.md",
              "天神下凡_六百万字完本总纲_v1.3.docx",
              "_tpl_base_v1.77.docx"}

for f in sorted(os.listdir(HIST)):
    p = os.path.join(HIST, f)
    if not os.path.isfile(p):
        continue
    if f.startswith("_bak_"):
        add(p, "bak", "回滚备份(旧)")
    elif f in HIST_SET:
        add(p, "set", "设定集各版(旧)")
    elif f in HIST_EXTRA:
        add(p, "extra", "配套旧版(旧)")
    else:
        raise SystemExit("UNCLASSIFIED in 历史版本: " + f)

# ---------- 执行 ----------
total = 0
by_tag = {}
for src, dstdir, tag in plan:
    dst = os.path.join(dstdir, os.path.basename(src))
    if os.path.exists(dst):
        raise SystemExit("COLLISION: " + dst)
    sz = os.path.getsize(src)
    shutil.move(src, dst)
    total += sz
    by_tag[tag] = by_tag.get(tag, 0) + 1

print("=== 归档结果 ===")
for k in sorted(by_tag):
    print("  %-14s %4d 个" % (k, by_tag[k]))
print("  合计 %d 个，%.1f MB" % (len(plan), total / 1048576.0))

print("\n=== 归档后 历史版本 各目录 ===")
for k, d in DIRS.items():
    n = len([x for x in os.listdir(d) if os.path.isfile(os.path.join(d, x))])
    print("  %-22s %4d" % (d, n))
print("  %-22s %4d" % (HIST + "\\svg",
      len(os.listdir(os.path.join(HIST, "svg")))))

print("\n=== 根目录剩余文件 ===")
left = sorted(f for f in os.listdir(ROOT) if os.path.isfile(f))
for f in left:
    print("   %-52s %10d" % (f, os.path.getsize(f)))
print("   共 %d 个文件" % len(left))
