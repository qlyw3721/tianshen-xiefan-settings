# -*- coding: utf-8 -*-
"""生成《天神下凡_神圣帝国示意图》自包含 SVG。
体例沿用《天神下凡_世界地图_v1.1.svg》：KaiTi 字体、米黄底、棕框、红/绿/蓝/紫分色。
用户裁定：奥格斯歌城、朱庇特城只标地理位置点位，城内内容一律不标（以后单独出图）。
新规则：后续设定集中与帝国相关内容同步标注到本图（两城例外）。
"""
import io, sys

W = 1100
FONT = "KaiTi, STKaiti, SimSun, serif"

# 符号 -> 颜色
C = {
    "capital": "#8a2f2a",   # ★ 都城（仅位置）
    "city":    "#4a3728",   # ◎ 城
    "county":  "#6b543a",   # ■ 郡/郡省
    "prov":    "#6b543a",   # ▤ 行省
    "manor":   "#6b3a8a",   # ◇ 庄园/城堡
    "church":  "#8a2f2a",   # ✚ 教堂/圣地
    "academy": "#3f6e80",   # ▽ 神学院/修道院
    "nature":  "#5a7d5a",   # ▲ 山脉/森林/水体
    "good":    "#a05a2c",   # ◆ 物产/矿物/生物
    "org":     "#6b543a",   # ▣ 机构/总部
    "plain":   "#4a3728",
}
SYM = {
    "capital":"★","city":"◎","county":"■","prov":"▤","manor":"◇",
    "church":"✚","academy":"▽","nature":"▲","good":"◆","org":"▣","plain":"●",
}

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

out = []
def A(s): out.append(s)

# 已渲染文本记录，供重叠检测 (x, y, w, h, label)
TEXT = []
def tw(s, fs):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2e80:
            w += fs
        elif ch in "★◎■▤◇✚▽▲◆▣●":
            w += fs
        elif ch in "·／〔〕（）()":
            w += fs * 0.7
        else:
            w += fs * 0.56
    return w
def text(x, y, s, fs=11.5, fill="#4a3728", anchor="start", bold=False, key=None):
    A('  <text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" text-anchor="%s"%s>%s</text>'
      % (x, y, fs, fill, anchor, (' font-weight="bold"' if bold else ''), esc(s)))
    w = tw(s, fs)
    x0 = x - w if anchor == "end" else (x - w/2 if anchor == "middle" else x)
    TEXT.append((x0, y - fs*0.85, w, fs*1.05, s, key or ""))

# ---------------- 区块数据 ----------------
# 每项 (类别键, 文本)
BLOCKS = [
    ("北境 · 高原与寒郡", "#e9eef3", 2, [
        ("nature","莱辛葛郡｜北境高原牧区·蓝莓奶酪"),
        ("academy","石崖修道院｜北境断崖·十大修道院候补"),
        ("county","硫磺郡省｜北部荒原·矿石少"),
        ("county","黎塞留郡省｜地表贫瘠／地下有矿〔守夜者机密〕"),
        ("good","乌尔姆军马｜帝国西北部·骑兵重要马源"),
    ]),
    ("西北 · 玛索郡省与塔梅廊", "#eef1e5", 3, [
        ("city","塔梅廊城｜西北大教区·加雅尔郡·迦卡妙家乡"),
        ("academy","脉代奥拉｜24 座山顶修道院·红玛瑙平原·空中修道院"),
        ("county","加雅尔郡｜帝国西北·粮仓·盛产英俊骑士"),
        ("county","玛索郡省｜西北·一湖四领·面积最大"),
        ("manor","白象城堡｜玛索西北角·贝福德山脉顶点·俯瞰黑天鹅湖"),
        ("manor","诗呢哥城堡／黑天鹅湖｜【秩序】总部·脉点·地下九层"),
        ("nature","贝福德山脉（玛索西北）·玛索平原·佛伦萨森林"),
        ("nature","茴香卑斯山脉｜帝国中部·分割南北·纯种军马"),
        ("manor","雅诗庄园／兰黛城堡｜托德家族·密西西竞技场"),
        ("manor","花露领地（格林斯潘）／极乐鸟别墅（康迪·温泉白鹿）"),
        ("manor","白露领地｜白象城堡所在领地"),
        ("good","海泽纯血马｜玛索·「马匹女皇」"),
    ]),
    ("帝都圈 · 东北与中部城", "#f0e8d8", 2, [
        ("capital","朱庇特城（帝都·东北）｜仅标位置，城内另图"),
        ("city","阿尔法城｜帝国中部最大奴隶集市·三集市·40 万人"),
        ("county","索尔邦郡｜学术重镇"),
        ("academy","索尔邦神学院｜四百年古老神学院"),
        ("city","索菲亚城（霍尔顿行省）"),
        ("church","荷稣复活大教堂｜157 米·帝国第三高"),
        ("city","笛卡尔城（暗河）"),
        ("county","佩洛蒂郡省｜阿蒙利界河领·鱼子酱·笛卡尔暗河"),
        ("good","三眼蝰蛇｜佩洛蒂地下暗河·极北无光"),
    ]),
    ("中部 · 守夜者与天然前哨", "#eae7f0", 2, [
        ("org","守夜者总部｜胡安郡／路桑郡交界"),
        ("nature","伯里曼黑暗森林｜守夜者心脏天然前哨"),
        ("church","天使花园｜奥林匹亚天使陨落地之一"),
        ("church","佛西斯精灵塔（森林东北角）／忏悔教堂（西南角）"),
        ("manor","卡萨黄昏城堡｜守夜者东北分部·浮朗西斯神学院背景"),
        ("nature","雅各布森林｜食猿雕·巨爪棕熊·阿加纳蝰蛇·依娜丽莎温泉"),
        ("nature","玛雅山脉／玛雅雪山神庙｜摩纳哥龙脉·黄金双十字切割点"),
        ("org","绿帕蒂海港｜帝国福音返航迎接地"),
    ]),
    ("东南 · 边境与异端", "#f1e6e2", 2, [
        ("capital","奥格斯歌城（东南经济都·东南隅）｜仅标位置，城内另图"),
        ("county","玛敦郡｜帝国东南"),
        ("nature","塞缪耳森林｜玛敦郡·异教徒根据地"),
        ("nature","萨克逊森林／撒波岛｜东南海岸异端据点"),
        ("county","查士叮郡"),
        ("manor","瑕多丽庄园｜罗桐柴尔德采邑·六大村庄·帝国十大领地"),
        ("manor","波撒珊城堡（瑕多丽主体）／罗曼村（辖村）"),
        ("good","血鳞石｜瑕多丽·定序物产·「矿不赋能，只定领地等级」"),
    ]),
    ("南疆 · 盆地与渡口", "#eef1e5", 2, [
        ("city","伊赛亚城｜帝国南部"),
        ("nature","黄昏盆地（帝国南疆）／翡翠河（盆地内渡口）"),
        ("good","毒箭巨蛙｜南部暖湿苇荡·毒随地方走"),
        ("academy","暮玛神学院｜大陆十大神学院之一〔位置未定〕"),
        ("academy","帝国莺桥学院〔位置未定〕"),
    ]),
]

# 分类索引（用户要求的 13 类）
INDEX = [
    ("郡／郡省（一级）", "玛索郡省、玛敦郡、加雅尔郡、莱辛葛郡、索尔邦郡、查士叮郡、佩洛蒂郡省、黎塞留郡省、硫磺郡省、基歇尔郡省、胡安郡／路桑郡、霍尔顿行省"),
    ("行省（二级）", "霍尔顿行省（索菲亚城·荷稣复活大教堂）；【原文明载「行省」实例仅泰坦帝国图拉德行省，不属本图】"),
    ("城（郡省首府／都会）", "塔梅廊、阿尔法、伊赛亚、笛卡尔、思考鲁、索菲亚、梅塞亚；★朱庇特城与★奥格斯歌城仅标点位"),
    ("庄园／领地", "瑕多丽、雅诗、花露、白露、波坎儿〔帝都近郊·不展开〕、极乐鸟别墅、黑天鹅湖庄、诗呢歌"),
    ("城堡", "波撒珊、白象、兰黛、诗呢哥、卡萨黄昏；血族各支总部亦为城堡（见 §8.1）"),
    ("建筑／宗教圣地", "圣马可修女院（思考鲁城）、荷稣复活大教堂、圣徒石碑大教堂、玛雅雪山神庙、天使花园、佛西斯精灵塔、忏悔教堂"),
    ("地名／地标", "红玛瑙平原、黄昏盆地、翡翠河渡、绿帕蒂海港、萨克逊森林、撒波岛、雅各布森林"),
    ("神学院／修道院", "脉代奥拉（24 院）、索尔邦（400 年）、石崖（候补）、暮玛（十大之一）、浮朗西斯；脉代奥拉神学院＝修道院同一实体"),
    ("学校／学院", "帝国莺桥学院；〔马丁／诺灵顿／圣乔治／图拉德等学院在奥格斯歌城，本图不标〕"),
    ("生物／栖息地", "三眼蝰蛇（笛卡尔暗河）、毒箭巨蛙（南部苇荡）、食猿雕·巨爪棕熊（雅各布森林）、乌尔姆军马（西北）、哥德尔芬拉波与茴香卑斯战马、海泽纯血马"),
    ("森林／山脉／水体", "塞缪耳、佛伦萨、萨克逊、伯里曼、雅各布森林；茴香卑斯、贝福德、馥香克斯山麓、玛雅山脉；黑天鹅湖、翡翠河"),
    ("矿物／物产", "血鳞石（瑕多丽）、冰晶石（储存）、潘奥神蚀矿石、奥瓦杜铁晶、大伽玛红铜、火鳞晶矿石、红玛瑙、蓝莓奶酪、鱼子酱；黎塞留地下矿〔守夜者机密〕"),
    ("家族总部（境内）", "罗桐柴尔德（瑕多丽／查士叮郡）、托德（玛索三领地）、康迪（极乐鸟）、海伦（基歇尔郡）、格林斯潘（花露）；〔康斯坦德＝奥古迦、费尔默思＝白蔷薇、瑟特斯＝奥古迦，皆境外不标〕"),
]

# ---------------- SVG 头 ----------------
A('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="2400" viewBox="0 0 %d 2400" font-family="%s">' % (W, W, FONT))
A('  <rect x="0" y="0" width="%d" height="2400" fill="#f3e9d2"/>' % W)
A('  <rect x="16" y="16" width="%d" height="2368" fill="none" stroke="#8a6d3b" stroke-width="3"/>' % (W-32))
A('  <rect x="24" y="24" width="%d" height="2352" fill="none" stroke="#8a6d3b" stroke-width="1" opacity="0.6"/>' % (W-48))
text(W/2, 66, "天神下凡 · 神圣帝国示意图", 30, "#4a3728", "middle", True)
text(W/2, 94, "行政层级：郡／郡省 ＞ 行省 ＞ 城（郡省首府）　｜　原著方位为骨 · 设定集 §1 地理体系为据 · 原创定位已标注", 12.5, "#6b543a", "middle")
text(W/2, 116, "★奥格斯歌城、★朱庇特城仅标地理位置，城内街区／建筑／学院／府邸一律不标（以后单独出图）；本图为分布示意，非精确疆域。", 11.5, "#8a2f2a", "middle")

# 罗盘
A('  <g transform="translate(1040,180)" stroke="#6b543a" fill="none" stroke-width="1.6">')
A('    <circle r="30"/><circle r="3.5" fill="#6b543a"/>')
A('    <path d="M 0,-36 L 5,-7 L 0,0 L -5,-7 Z" fill="#8a2f2a" stroke="none"/>')
A('    <path d="M 0,36 L 5,7 L 0,0 L -5,7 Z" fill="#6b543a" stroke="none"/>')
A('    <text y="-42" text-anchor="middle" font-size="14" fill="#4a3728" stroke="none">北</text></g>')

# 图例
A('  <rect x="40" y="140" width="980" height="34" fill="#f7efdd" stroke="#8a6d3b" stroke-width="1"/>')
legend = [("capital","都城·仅位置"),("city","城"),("county","郡／郡省"),("prov","行省"),
          ("manor","庄园／城堡"),("church","教堂／圣地"),("academy","神学院／修道院"),
          ("nature","山脉／森林／水体"),("good","物产／矿物／生物"),("org","机构／总部")]
lx = 52
for k, lab in legend:
    text(lx, 162, SYM[k], 12.5, C[k], "start", True)
    text(lx+16, 162, lab, 10.5, "#4a3728", "start")
    lx += 16 + tw(lab,10.5) + 20

# ---------------- 区块渲染 ----------------
y = 190
MARGIN = 40
COLGAP = 14
for title, bg, cols, items in BLOCKS:
    nrows = (len(items) + cols - 1) // cols
    rowh = 22
    h = 34 + nrows*rowh + 12
    A('  <rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" stroke="#8a6d3b" stroke-width="1.1" rx="4"/>'
      % (MARGIN, y, W-2*MARGIN, h, bg))
    text(MARGIN+12, y+22, title, 14, "#4a3728", "start", True)
    colw = (W-2*MARGIN-24-(cols-1)*COLGAP)/cols
    for i, (k, lab) in enumerate(items):
        c = i % cols
        r = i // cols
        xx = MARGIN+12 + c*(colw+COLGAP)
        yy = y + 40 + r*rowh
        text(xx, yy, SYM[k], 11.5, C[k], "start", True)
        text(xx+16, yy, lab, 11, C[k], "start")
    y += h + 10

# ---------------- 两城例外说明框 ----------------
A('  <rect x="40" y="%.1f" width="%d" height="106" fill="#f7efdd" stroke="#8a2f2a" stroke-width="1.3" rx="4"/>' % (y, W-80))
text(52, y+22, "两城例外（用户 2026-11-16 裁定）：奥格斯歌城与朱庇特城只标地理位置点位，相关内容暂不标注，以后单独生成这两城示意图。", 11.5, "#8a2f2a", "start", True)
text(52, y+44, "· 奥格斯歌城城内不标：塔伯／罗德里／利拜尔／梛盾等区、泰勒大街、卢甸宫大教堂、诺灵顿／马丁／圣乔治／图拉德学院、巴洛克与哥特两府、占星楼德古拉之牙、斯捷潘园地与答陨石竞技场等。", 10.2, "#6b543a", "start")
text(52, y+64, "· 朱庇特城城内不标：乌尔姆大街 1–46 号、罗伽费因格竞技场、帝国学院、审判之庭、圣约翰大教堂、梵特兰蒂冈两大机构（牧首圣庭／异端裁决所）等。", 10.2, "#6b543a", "start")
text(52, y+84, "· 例外只针对「两城之城内内容」：城外独立领地（如查士叮郡瑕多丽庄园、玛索郡白象城堡）仍按分布标注；其城际方位（奥格斯歌在东南、朱庇特在东北）照常标。", 10.2, "#6b543a", "start")
y += 118

# ---------------- 分类索引表 ----------------
A('  <rect x="40" y="%.1f" width="%d" height="24" fill="#4a3728"/>' % (y, W-80))
text(52, y+17, "分类索引（按地理实体类别穷尽 · 与上方位图互见 · 详见设定集 §1）", 12.5, "#ffffff", "start", True)
y += 24
RH = 46
for i, (cat, body) in enumerate(INDEX):
    bg = "#fbf6e8" if i % 2 == 0 else "#f6edd8"
    A('  <rect x="40" y="%.1f" width="%d" height="%d" fill="%s" stroke="#c9b483" stroke-width="0.6"/>'
      % (y, W-80, RH, bg))
    text(52, y+20, cat, 11, "#4a3728", "start", True)
    # 正文自动折行
    maxw = W-80-200
    line, lines = "", []
    for ch in body:
        if tw(line+ch, 10.2) > maxw:
            lines.append(line); line = ch
        else:
            line += ch
    if line: lines.append(line)
    for j, ln in enumerate(lines[:2]):
        text(240, y+18+j*15, ln, 10.2, "#5a4630", "start")
    y += RH

# 页脚
y += 10
text(52, y+16, "新规则（用户 2026-11-16 令 · 设定集 §0.6 长期强制）：后续设定集中凡与神圣帝国相关的内容，同步更新标注到本示意图；奥格斯歌城、朱庇特城仍按上例例外（只标地理位置）。", 10.5, "#8a2f2a", "start", True)
text(52, y+36, "符号说明：★都城（仅位置）◎城 ■郡／郡省 ▤行省 ◇庄园／城堡 ✚教堂／圣地 ▽神学院／修道院 ▲山脉／森林／水体 ◆物产／矿物／生物 ▣机构／总部。", 10, "#6b543a", "start")
text(52, y+56, "方位依 §1.10 原著骨架（神圣帝国＝史诗大陆东北；奥格斯歌城在东南、朱庇特城为帝都）；无原文坐标者标【续补·原创定位】；前后传原文 txt 一字不改。", 10, "#6b543a", "start")

# 计算需要的真实高度
need = y + 80
out[0] = out[0].replace('height="2400" viewBox="0 0 %d 2400"' % W, 'height="%d" viewBox="0 0 %d %d"' % (need, W, need))
# out[1]=底rect(2400) out[2]=外框(2368) out[3]=内框(2352)
out[1] = out[1].replace('height="2400"', 'height="%d"' % (need-32))
out[2] = out[2].replace('height="2368"', 'height="%d"' % (need-32))
out[3] = out[3].replace('height="2352"', 'height="%d"' % (need-48))
out.append('</svg>')

svg = "\n".join(out) + "\n"
path = r"E:\天神下凡\天神下凡_神圣帝国示意图_v1.0.svg"
with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)

# ---------------- 重叠检测 ----------------
import itertools
# 只检测同一"文字行带"（y 接近）的水平重叠；符号与标签紧邻属设计内，跳过 key 中"符号"
issues = []
for a, b in itertools.combinations(TEXT, 2):
    ax, ay, aw, ah, al, ak = a
    bx, by, bw, bh, bl, bk = b
    if abs(ay - by) < 6:  # 同一行带
        overlap = min(ax+aw, bx+bw) - max(ax, bx)
        if overlap > 3:
            issues.append((round(overlap,1), al[:26], bl[:26], round(ay,1)))
issues.sort(reverse=True)
print("SVG:", path)
print("文本元素:", len(TEXT), " 画布高度:", need, " 字节:", len(svg.encode("utf-8")))
print("重叠候选(同带水平重叠>3px):", len(issues))
for it in issues[:40]:
    print("   ", it)
