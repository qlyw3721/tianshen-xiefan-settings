# -*- coding: utf-8 -*-
"""将《天神下凡》前后传 txt 转换为 EPUB2（UTF-8，卷→章嵌套目录，去广告/网页残留）。"""
import re, os, zipfile, datetime, uuid

SRC = r"E:/天神下凡（2026-11-09-17-44-13）"

AD_PREFIX = ["更多精校", "更多免费", "本书由", "手机阅读", "扫一扫", "微信公众号",
             "更新最快", "（未完待续", "TXT下载", "电子书"]
AD_PHRASE = ["未完待续", "如欲知后事", "图片下载标记", "支持正版阅读",
             "起点中文网", "知轩藏书"]
AD_URL = ["http://", "https://", "www.", "panlay", "qidian", ".com", ".net"]

VOL_RE = re.compile(r'^\s*第[一二三四五六七八九十百零0-9]{1,4}卷')
CHAP_RE = re.compile(r'^\s*第[一二三四五六七八九十百零0-9]{1,4}章')

CONTAINER = (
    '<?xml version="1.0"?>\n'
    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
    '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
    '</rootfiles></container>'
)

CSS = (
    'body{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC",serif;'
    'margin:1em;}\n'
    'h1{font-size:1.3em;text-align:center;margin:1em 0;}\n'
    'p{text-indent:2em;line-height:1.9;margin:0.4em 0;text-align:justify;}\n'
)

XHTML_TMPL = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
    '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    '<html xmlns="http://www.w3.org/1999/xhtml">\n'
    '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
    '<title>{title}</title></head>\n'
    '<body><h1>{title}</h1>{body}</body></html>'
)

OPF_TMPL = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">\n'
    '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
    '<dc:identifier id="bookid">{uid}</dc:identifier>\n'
    '<dc:title>{title}</dc:title>\n'
    '<dc:creator>{author}</dc:creator>\n'
    '<dc:language>zh</dc:language>\n'
    '<dc:date>{date}</dc:date>\n'
    '</metadata>\n'
    '<manifest>\n'
    '<item id="ncx" href="toc.ncx" media-type="application/x-document-navigation-control-xml"/>\n'
    '<item id="css" href="style.css" media-type="text/css"/>\n'
    '{items}\n'
    '</manifest>\n'
    '<spine toc="ncx">\n{spine}\n</spine>\n'
    '</package>'
)

NCX_TMPL = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
    '<head>\n'
    '<meta name="dtb:uid" content="{uid}"/>\n'
    '<meta name="dtb:depth" content="1"/>\n'
    '<meta name="dtb:totalPageCount" content="0"/>\n'
    '<meta name="dtb:maxPageNumber" content="0"/>\n'
    '</head>\n'
    '<docTitle><text>{title}</text></docTitle>\n'
    '<navMap>\n{nav}\n</navMap>\n'
    '</ncx>'
)


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    # v1.19 用户裁定：设定层统一「迪米特」。此处仅作用于 EPUB 阅读本，
    # 前后传原文 .txt 按「原文一字不改」纪律保持原字不动。
    return text.replace("帝米特", "迪米特")


def is_ad(line):
    s = line.strip()
    if not s:
        return False
    if any(s.startswith(p) for p in AD_PREFIX):
        return True
    if any(k in s for k in AD_PHRASE):
        return True
    if any(u in s for u in AD_URL):
        return True
    return False


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def parse_vol_chap(text):
    """返回 parts = [ [part_title, [(chap_title, [paras]), ...]], ... ] 或 None（无卷）。"""
    lines = text.split("\n")
    start = None
    for i, l in enumerate(lines):
        if VOL_RE.search(l):
            start = i
            break
    if start is None:
        return None
    parts = []
    cur_part = None
    cur_chap = None
    for l in lines[start:]:
        if is_ad(l):
            continue
        s = l.strip()
        if not s:
            continue
        if VOL_RE.search(l):
            if cur_part is not None:
                parts.append(cur_part)
            cur_part = [s, []]
            cur_chap = None
        elif CHAP_RE.search(l):
            if cur_part is None:
                cur_part = ["正文", []]
            cur_chap = [s, []]
            cur_part[1].append(cur_chap)
        else:
            if cur_part is None:
                cur_part = ["正文", []]
            if cur_chap is None:
                cur_chap = ["（引子）", []]
                cur_part[1].append(cur_chap)
            cur_chap[1].append(s)
    if cur_part is not None:
        parts.append(cur_part)
    return parts


def auto_split(text, target=34000):
    """前传：无章节标记，按字数自动切分。"""
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l and not is_ad(l)]
    chapters = []
    cur = []
    n = 0
    for l in lines:
        cur.append(l)
        n += len(l.encode("utf-8"))
        if n >= target:
            chapters.append(cur)
            cur = []
            n = 0
    if cur:
        chapters.append(cur)
    return [("第%d章" % i, c) for i, c in enumerate(chapters, 1)]


def build_epub(parts, title, author, out_path):
    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "tsxf:" + title))
    now = datetime.date.today().isoformat()

    show_part = len(parts) > 1 and any(p[0] for p in parts)
    flat = []
    for p_title, chaps in parts:
        for c_title, paras in chaps:
            fn = "ch%d.xhtml" % (len(flat) + 1)
            flat.append((p_title if show_part else None, c_title, fn, paras))

    xhtml_docs = []
    items = []
    spine = []
    for i, (pt, ct, fn, paras) in enumerate(flat, 1):
        body = "\n".join("<p>%s</p>" % esc(p) for p in paras)
        xhtml = XHTML_TMPL.replace("{title}", esc(ct)).replace("{body}", body)
        xhtml_docs.append((fn, xhtml))
        items.append('<item id="id%d" href="%s" media-type="application/xhtml+xml"/>' % (i, fn))
        spine.append('<itemref idref="id%d"/>' % i)

    # 嵌套目录
    play = [0]
    nav = []
    if show_part:
        SENTINEL = object()
        cur_part = SENTINEL
        for pt, ct, fn, paras in flat:
            if pt is not cur_part:
                if cur_part is not SENTINEL:
                    nav.append("</navPoint>")
                cur_part = pt
                play[0] += 1
                nav.append(
                    '<navPoint id="part_%d" playOrder="%d"><navLabel><text>%s</text>'
                    '</navLabel><content src="%s"/>' % (play[0], play[0], esc(pt), fn))
            play[0] += 1
            nav.append('<navPoint id="chap_%d" playOrder="%d"><navLabel><text>%s</text>'
                       '</navLabel><content src="%s"/></navPoint>'
                       % (play[0], play[0], esc(ct), fn))
        if cur_part is not SENTINEL:
            nav.append("</navPoint>")
    else:
        for i, (pt, ct, fn, paras) in enumerate(flat, 1):
            play[0] += 1
            nav.append('<navPoint id="chap_%d" playOrder="%d"><navLabel><text>%s</text>'
                       '</navLabel><content src="%s"/></navPoint>'
                       % (i, play[0], esc(ct), fn))

    opf = OPF_TMPL.replace("{uid}", uid).replace("{title}", esc(title)).replace(
        "{author}", esc(author)).replace("{date}", now).replace(
        "{items}", "\n".join(items)).replace("{spine}", "\n".join(spine))
    ncx = NCX_TMPL.replace("{uid}", uid).replace("{title}", esc(title)).replace(
        "{nav}", "\n".join(nav))

    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", CONTAINER, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        for fn, xhtml in xhtml_docs:
            z.writestr("OEBPS/" + fn, xhtml, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)

    return out_path, len(flat)


if __name__ == "__main__":
    # 正传/后传
    txf = load(os.path.join(SRC, "《天神下凡》.txt"))
    parts_txf = parse_vol_chap(txf)
    p, n = build_epub(parts_txf, "天神下凡", "烽火戏诸侯",
                      os.path.join(SRC, "天神下凡.epub"))
    print("天神下凡.epub ->", p, "章节数:", n)

    # 前传（无章节标记 -> 自动切分）
    zj = load(os.path.join(SRC, "宗教裁判所.txt"))
    parts_zj = parse_vol_chap(zj)
    if parts_zj is None:
        parts_zj = [("正文", auto_split(zj))]
    p2, n2 = build_epub(parts_zj, "宗教裁判所（前传）", "烽火戏诸侯",
                        os.path.join(SRC, "宗教裁判所（前传）.epub"))
    print("宗教裁判所（前传）.epub ->", p2, "章节数:", n2)
    print("done")
