# -*- coding: utf-8 -*-
import re, sys

SRC = '天神下凡设定集_归纳整理版_V4.1.md'
raw = open(SRC, 'rb').read().decode('utf-8')
lines = raw.split('\r\n')

PH = '\u2410'  # placeholder char

def protect(line):
    store = []
    def repl(m):
        store.append(m.group(0))
        return f'{PH}{len(store)-1}{PH}'
    l = re.sub(r'「[^」]*」', repl, line)
    l = re.sub(r'“[^”]*”', repl, l)
    l = re.sub(r'"[^"]*"', repl, l)
    return l, store

def restore(line, store):
    for i, s in enumerate(store):
        line = line.replace(f'{PH}{i}{PH}', s)
    return line

def convert(line):
    # 并列异写规范化
    line = line.replace('庞培／庞贝', '庞贝').replace('庞贝／庞培', '庞贝')
    line = line.replace('克拉苏／克拉夫', '克拉夫').replace('克拉夫／克拉苏', '克拉夫')
    line = line.replace('庞培', '庞贝')
    line = line.replace('克拉苏', '克拉夫')
    line = line.replace('克罗夫', '克拉夫')
    return line

changed = 0
report = []
for i, l in enumerate(lines):
    if not any(k in l for k in ['庞培', '克拉苏', '克罗夫']):
        continue
    prot, store = protect(l)
    newp = convert(prot)
    newl = restore(newp, store)
    if newl != l:
        changed += 1
        report.append((i+1, l, newl))

print('TOTAL changed lines:', changed)
# 只打印差异中"被替换但原文引号内是否残留"的核查
for n, old, new in report:
    print('L%d' % n)
    print('  OLD:', old[:230])
    print('  NEW:', new[:230])
