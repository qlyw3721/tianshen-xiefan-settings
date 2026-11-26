# -*- coding: utf-8 -*-
pairs = [
    ('E:/天神下凡/天神下凡设定集版本更新说明集.md',
     '**281／409／201／19，合计 919 件／926.0 MB**',
     '**281／411／201／19，合计 921 件／926.1 MB**'),
    ('E:/天神下凡/设定集_裁定台账.md',
     '**281／409／201／19，919 件／926.0 MB**',
     '**281／411／201／19，921 件／926.1 MB**'),
    ('E:/天神下凡/历史版本/00_归档索引.md',
     '| 409 |', '| 411 |'),
    ('E:/天神下凡/历史版本/00_归档索引.md',
     '**281／409／201／19，合计 919 件／926.0 MB**',
     '**281／411／201／19，合计 921 件／926.1 MB**'),
]
for p, old, new in pairs:
    raw = open(p, 'rb').read()
    o = old.encode('utf-8')
    n = raw.count(o)
    assert n == 1, (p, old, n)
    open(p, 'wb').write(raw.replace(o, new.encode('utf-8')))
    print('OK', p.split('/')[-1], '|', old[:30])

for p in ['E:/天神下凡/天神下凡设定集版本更新说明集.md',
          'E:/天神下凡/设定集_裁定台账.md',
          'E:/天神下凡/历史版本/00_归档索引.md']:
    raw = open(p, 'rb').read()
    print(p.split('/')[-1], 'bareLF', raw.count(b'\n') - raw.count(b'\r\n'),
          '921', raw.decode('utf-8').count('921 件'))
