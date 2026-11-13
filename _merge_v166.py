import re

local_path = "E:/天神下凡/天神下凡设定集_归纳整理版_v1.2.md"
space_path = "E:/天神下凡/_compare_space_v1.4.1.md"
out_path   = "E:/天神下凡/天神下凡设定集_归纳整理版_v1.66整合.md"

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

local = read(local_path)
space = read(space_path)
local_lines = local.split('\n')
space_lines = space.split('\n')

def parse_sections(lines):
    heads = []
    for i, ln in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            heads.append({'level': len(m.group(1)), 'title': m.group(2).strip(), 'idx': i})
    return heads

def normalize(t):
    t = t.strip().lower()
    t = re.sub(r'[（(][^）)]*v?\d+\.\d+[^）)]*[)）]', '', t)  # 版本后缀
    t = re.sub(r'[（(]整合版[)）]', '', t)
    t = re.sub(r'[（(]整合[)）]', '', t)
    t = re.sub(r'[（(]新增[)）]', '', t)
    t = re.sub(r'[（(][^）)]*[)）]', '', t)                  # 其余括号内容
    t = re.sub(r'[#*`\\_~.。]', '', t)                       # 标点/星号/点
    t = re.sub(r'\s+', '', t)
    return t

local_heads = parse_sections(local_lines)
space_heads = parse_sections(space_lines)

def ranges(heads, total):
    out = []
    n = len(heads)
    for k, h in enumerate(heads):
        start = h['idx']
        end = total
        for j in range(k+1, n):
            if heads[j]['level'] <= h['level']:
                end = heads[j]['idx']
                break
        out.append((h, start, end))
    return out

local_ranges = ranges(local_heads, len(local_lines))
space_ranges = ranges(space_heads, len(space_lines))

local_keys = {}
for (h, s, e) in local_ranges:
    local_keys[(h['level'], normalize(h['title']))] = True

EXCLUDE_NORMS = {normalize('12 家族'), normalize('13 机构与组织')}
FORCE_NORM = normalize('13.4 剑士协会 与 「罗兰之歌」秘密剑士协会（v1.3 新增）')

result_blocks = []

def process(start_idx, end_idx, parent_excluded):
    i = start_idx
    while i < end_idx:
        h, s, e = space_ranges[i]
        norm = normalize(h['title'])
        level = h['level']
        # children range
        j = i + 1
        child_end = end_idx
        while j < end_idx:
            if space_ranges[j][0]['level'] <= level:
                child_end = j
                break
            j += 1
        if level == 1:
            i = child_end
            continue
        excluded = parent_excluded
        force = False
        if level == 2 and norm in EXCLUDE_NORMS:
            excluded = True
        if norm == FORCE_NORM:
            force = True
        if force:
            excluded = False
        if excluded and not force:
            process(i+1, child_end, True)   # 仍扫描子节（可能有强制项）
            i = child_end
            continue
        if (level, norm) in local_keys and not force:
            process(i+1, child_end, False)  # 已覆盖：仅抽取独有子节
        else:
            result_blocks.append((h, s, e))  # 整段并入
        i = child_end

# 从第一个非 H1 标题开始处理整棵空间文档树
first = 0
while first < len(space_ranges) and space_ranges[first][0]['level'] == 1:
    first += 1
process(first, len(space_ranges), False)

# ---- 组装成品 ----
# 1) 更新本地版本标记
local = local.replace("｜v1.66｜", "｜v1.66（整合）｜", 1)
local = local.replace("**版本**：v1.2-r1（封圣制度补遗版 · 终局裁定同步）",
                      "**版本**：v1.66（整合版 · 本地 v1.66 为基底，并入 v1.4.1 整合版独有章节）", 1)
# 在「版本」行后插入合并说明
merge_note = (
    "\n\n"
    "> **合并说明（v1.66 整合版）**：本版以本地《归纳整理版 v1.2.md》（内部已至 **v1.66**，共 "
    + str(len(local_lines)) + " 行）为骨架；经逐节标题比对，并入空间文档《v1.4.1（整合）》中本地所缺的章节／子节"
    "（含 §0.6/§0.7 变更摘要、§3.14 重点配角、§6.5 神祇·亡灵诅咒术·傀儡术、§13.4 剑士协会、§14 种族，"
    "以及各章独有子节如 §1.2.1/§1.2.5/§1.3.1/§3.1.1/§9.3 子词条等），统一收束于文末「§15. 整合补充」。\n"
    "> 空间文档中已被本地 §1.2.3/§7 覆盖的 §12 家族、§13.1–§13.3 机构组织整章**未重复并入**（仅保留其独有子节 §13.4）；"
    "与原著同文的段落一律不重复录入。版本号依指令取较高者，标为 **v1.66（整合）**。\n"
)
local = local.replace("**版本**：v1.66（整合版 · 本地 v1.66 为基底，并入 v1.4.1 整合版独有章节）",
                      "**版本**：v1.66（整合版 · 本地 v1.66 为基底，并入 v1.4.1 整合版独有章节）" + merge_note, 1)

# 2) 拼接待并入区块
appendix = ["", "", "---", "", "## 15. 整合补充（源自 v1.4.1 整合版独有内容）", "",
            "> 以下章节／子节为空间文档《v1.4.1（整合）》所独有、本地 v1.66 未涵盖者，按原标题与编号并入，"
            "仅作录入、不擅改内容；与原著同文或已被本地覆盖者不在此列。", ""]
for (h, s, e) in result_blocks:
    block = '\n'.join(space_lines[s:e])
    appendix.append(block)

merged = local + '\n'.join(appendix) + '\n'

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(merged)

print("本地行数:", len(local_lines))
print("并入区块数:", len(result_blocks))
print("成品行数:", merged.count('\n')+1)
print("---- 并入的章节标题（按出现顺序）----")
for (h, s, e) in result_blocks:
    print(f"  L{s+1}: {h['title']}")
