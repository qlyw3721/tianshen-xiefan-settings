# -*- coding: utf-8 -*-
"""v2.32 关系网同步：撒克逊（第三圈/武器来源）、二号房间老人（分类权衣钵）"""
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
print(call("open_file", file_path=FID, file_type="xmind", wait=True)[:200])

print("=== 撒克逊改标题 ===")
print(call("mind_find_replace_text",
           find="撒克逊（黑皇帝·大异端）",
           replace="撒克逊（黑皇帝·大陆最大异端·第三羊圈｜v2.32 立传）")[:200])

print("=== 撒克逊加子节点 ===")
print(call("mind_add_nodes", parent_id="n72", titles=[
    "六重标签·四种来源：经语义「持有利剑守护上帝的虔诚者」／学界「不可战胜的博士」「剃刀」／牌制「黑皇帝」(801·821 连任)／教皇「闯入葡萄园的野猪」／尼禄「先知」",
    "与主角关系：隔代武器来源（非师徒、非盟友）——两人从未见面，关系全由「著作—阅读」建立",
    "主角三层取·一层不取：取方法（剃刀）／取边界（教权与王权分离）／自有位置（异端裁决所）／不取目的（另立第三圈）——武器使用者，非继承人",
    "第三羊圈：教廷分类学只有「圈内（羊）／圈外（狼·盗贼）」两格，他是第三格「另设一圈者」，无词可用，故「现在的你不能够去判定」＝分类失败",
    "原文锚：名实五层 v2.26／案卷 v2.27／下落 v2.28／剃刀与「先知」v2.30／羊圈 v2.32；人物志 §3.14 三",
])[:300])

print("=== 二号老人加子节点 ===")
print(call("mind_add_nodes", parent_id="6e523ce585639bfa6c82bd05", titles=[
    "衣钵实质＝分类权（图书馆长＋魔法书籍管理章程修订者：既掌藏书，又定谁读什么）——正是异端裁决所巨头的本职",
    "与撒克逊对称：两家教廷各判出一个自己最大的异端（拜占奥判撒克逊 61 篇／梵特兰蒂冈判他「头号大异端」）；一个向外建圈，一个向内沉默",
    "衣钵三项：分类权／禁忌知识（神圣比例·斐伯纳数分割·大地脉络假象结点）／一种示范（不必站在教廷外也能被判为异端）——第三项是「路径」不是「知识」",
    "纪律：永不填名（房号代名是忏悔地制度，替制度填名＝废掉制度）；不写他出忏悔地；不写他与撒克逊见面（原文无交集）",
    "v2.32 立传 §3.14 四；身份推定仍为【推定·强】——传可立，推定不可升",
])[:300])

print("=== save ===")
print(call("save_file", file_path=FID)[:150])
