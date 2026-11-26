# -*- coding: utf-8 -*-
p = 'E:/天神下凡/天神下凡设定集版本更新说明集.md'
raw = open(p, 'rb').read()
old = '写引荐信（L4157）。'.encode('utf-8')
new = ('写引荐信（L4157）。**落盘**：md **25,569 行／4,106,610 B／裸 LF 0**；'
       'docx **2,409,528 B**；四件套全绿；V4.4 md／docx＋`_v45_apply.py` 归档，'
       '根目录只留 V4.5；归档实数 **281／409／201／19，合计 919 件／926.0 MB**；未上传资料库。').encode('utf-8')
assert raw.count(old) == 1, raw.count(old)
open(p, 'wb').write(raw.replace(old, new))
t = open(p, 'rb').read()
print('bareLF', t.count(b'\n') - t.count(b'\r\n'))
s = t.decode('utf-8')
for k in ['919 件', '926.0 MB', '25,569 行', '_v45_apply.py']:
    print(k, s.count(k))
