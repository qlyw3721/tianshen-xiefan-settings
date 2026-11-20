# -*- coding: utf-8 -*-
import json, subprocess, sys
EDSDK = ("C:/Users/yanpeijie/.workbuddy/plugins/cache/workbuddy-builtin/tencent-xmind/"
         "5.11.3-wb.43806934.gecace0f7.ha395516167d4/skills/tencent-xmind/scripts/edsdk.py")
FID = "E:/天神下凡/奥古斯丁关系网_六度分隔.xmind"
def call(tool, **kw):
    kw["file_id"] = FID
    r = subprocess.run([sys.executable, EDSDK, "call", tool, "--json", json.dumps(kw, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip()

jobs = [
 ("2eb5c6ccfbe277474391a29d", [
   "关系线：他称她「尊敬的先知德黑撒」；她是他师姐（同为圣阿尔忒弥斯弟子），也是他第一批忏悔者之一——他听她的忏悔，她不教他占星（「她不肯教，你也学不会」）",
   "关系线·遗物：死后「遗留」六七颗黑水晶球给他（L2919）——忏悔者的东西归其神父",
   "原文锚点：前传 L2836／L2847／L2853（大占星师·枯老·龙眼法杖·走出皇宫后居脉代奥拉）／L2919；110 岁＝原文补充；指认＝用户裁定 2026-11-20",
 ]),
 ("5299a5f6b05505aebc69f8e1", [
   "关系线：忏悔者兼赌局对手——「年轻却野心勃勃的神父与年迈却不肯休息的忏悔者」（L3399）；一枚波旁银币起赌，一个月得 12 枚，每枚换 10 名高阶扈从骑士的忠诚",
   "身份链【推定·强】：朱庇特城克拉夫家族府邸·老家主（L3392）＋脉代奥拉神学院苦修 20 多年后复出（L3394）＋被称忏悔者（L3399）",
   "原文锚点：前传 L3392／L3394／L3399；§3.5.3 克拉夫条、§3.13 v2.31 块",
 ]),
 ("6e523ce585639bfa6c82bd05", [
   "关系线：二号房间的忏悔者；奥古斯丁以羊皮纸朴勒凯契数魔法阵相询，他授神圣比例、斐伯纳数分割与大地脉络假象结点的禁忌知识",
   "身份：梵特兰蒂冈教廷昔日大神学家与大异端／图书馆前馆长／魔法书籍管理章程修订者；房间「没有存放一本经书或者魔法书籍」",
   "原文锚点：前传 L2902（另 L2908 六号房间老魔法为另一人）；姓名原文未给，永久不填",
 ]),
 ("da01e48d13ed03fa292f0557", [
   "五条：终身（不可辞不可换）／单向（只听不告解）／绝对保密（权在知道、责在不说）／房号代名（制度先抹名）／不传承（神父死则封门·推定）",
   "「羔羊」二义：少年期＝忏悔者（宗教义）；成年后＝势力棋子（世俗义，L3399「放养了多少头羔羊」）——转折点＝离开脉代奥拉",
   "禁令：禁审问逼供（忏悔地非监狱）／禁泄密／禁代填名；§0.6 第三十九款",
 ]),
]
for pid, titles in jobs:
    print(call("mind_add_nodes", parent_id=pid, titles=titles)[:200])
print("=== save ===")
print(call("save_file", file_path=FID)[:150])
