# -*- coding: utf-8 -*-
"""估算 SVG <text> 包围盒并检测重叠（跳过旋转文字）。"""
import re, sys, unicodedata

def boxes(path):
    s = open(path, encoding='utf-8').read()
    out = []
    for m in re.finditer(r'<text([^>]*)>(.*?)</text>', s, re.S):
        attrs, body = m.group(1), m.group(2)
        if 'rotate' in attrs or 'transform' in attrs:
            continue
        gx = re.search(r'\bx="(-?[\d.]+)"', attrs); gy = re.search(r'\by="(-?[\d.]+)"', attrs)
        if not gx or not gy: continue
        x, y = float(gx.group(1)), float(gy.group(1))
        fs = re.search(r'font-size="([\d.]+)"', attrs)
        fs = float(fs.group(1)) if fs else 12.0
        anc = re.search(r'text-anchor="(\w+)"', attrs)
        anc = anc.group(1) if anc else 'start'
        txt = re.sub(r'<[^>]+>', '', body)
        txt = re.sub(r'&#\d+;', 'x', txt)
        w = 0.0
        for ch in txt:
            if unicodedata.east_asian_width(ch) in ('W', 'F'):
                w += fs
            elif ch == ' ':
                w += fs * 0.32
            else:
                w += fs * 0.55
        if anc == 'middle': x0 = x - w / 2
        elif anc == 'end':  x0 = x - w
        else:              x0 = x
        out.append({'x0': x0, 'x1': x0 + w, 'y0': y - fs * 0.88, 'y1': y + fs * 0.22,
                    't': txt[:46], 'fs': fs, 'x': x, 'y': y})
    return out

def report(path, tol=0.0):
    bs = boxes(path)
    hits = []
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i], bs[j]
            ox = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
            oy = min(a['y1'], b['y1']) - max(a['y0'], b['y0'])
            if ox > tol and oy > tol:
                hits.append((round(ox, 1), round(oy, 1), a['t'], b['t']))
    hits.sort(reverse=True)
    print('文本块 %d；重叠对 %d' % (len(bs), len(hits)))
    for h in hits[:40]:
        print('  ox=%5.1f oy=%4.1f | %s || %s' % h)
    return hits

if __name__ == '__main__':
    report(sys.argv[1] if len(sys.argv) > 1 else '天神下凡_世界地图_v1.0.svg')
