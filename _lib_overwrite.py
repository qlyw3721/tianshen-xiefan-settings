#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""资料库大文件就地覆盖：get-upload-credential -> COS PUT -> import-local-file-async -> query-progress.
复用历史上 v1.77 覆盖成功的 COS 直传通道，绕开 create-doc 的 1MB JSON 帧限制。
"""
import json, os, subprocess, sys, time, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SKILL = r"D:/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"
API = os.path.join(SKILL, "space_api.py")
MD = os.path.join(BASE, "天神下凡设定集_归纳整理版_v1.93.md")
NODE = "5kHCNUH7cX9LweAnGz3y0e"
FNAME = "天神下凡设定集_归纳整理版_v1.93.md"
TITLE = "天神下凡设定集_归纳整理版_v1.93（markdown同步·原文梳理工程P1-P7＋用户裁定全量归位）"


def call(api, *args):
    out = subprocess.run([sys.executable, API, api, *args], capture_output=True, text=True, encoding="utf-8")
    raw = out.stdout.strip()
    if not raw:
        print("EMPTY STDOUT:", api, out.stderr[:300]); sys.exit(1)
    try:
        obj = json.loads(raw)
    except Exception:
        print("NON-JSON:", api, raw[:300]); sys.exit(1)
    if "error" in obj:
        print("API ERROR:", api, obj["error"]); sys.exit(1)
    return obj.get("data", obj)


def main():
    size = os.path.getsize(MD)
    print("STEP1 credential, size=", size)
    d = call("space.importer.get-upload-credential",
             "--file-name", FNAME, "--file-size", str(size), "--node-block-id", NODE)
    url, cos_key, task_id = d["uploadUrl"], d["cosKey"], d.get("taskId", "")
    print("  cosKey=", cos_key, " taskId=", task_id)

    print("STEP2 COS PUT")
    with open(MD, "rb") as f:
        body = f.read()
    req = urllib.request.Request(url, data=body, method="PUT")
    req.add_header("Content-Type", "text/markdown; charset=utf-8")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            print("  PUT status=", resp.status)
    except Exception as e:
        print("  PUT FAILED:", repr(e)); sys.exit(1)

    print("STEP3 import-local-file-async")
    args = ["--file-name", FNAME, "--file-size", str(size), "--cos-key", cos_key,
            "--node-block-id", NODE]
    if task_id:
        args += ["--task-id", task_id]
    d2 = call("space.importer.import-local-file-async", *args)
    print("  data=", json.dumps(d2, ensure_ascii=False)[:400])

    print("STEP4 query progress")
    tid = d2.get("taskId", task_id)
    for i in range(30):
        if not tid:
            print("  no taskId to query; relying on async import"); break
        d3 = call("space.importer.query-import-file-progress", "--task-id", tid)
        st = json.dumps(d3, ensure_ascii=False)
        print("  [%d] %s" % (i, st[:300]))
        if any(k in st for k in ('"done"', '"success"', '"finished"', '"status":"done"', '"percent":100')):
            break
        time.sleep(2)

    print("STEP5 rename node title")
    try:
        call("space.workspace.rename-node", "--node-id", NODE, "--title", TITLE)
        print("  renamed")
    except SystemExit:
        print("  rename failed / unsupported; keep old title")
    print("DONE node=", NODE)


if __name__ == "__main__":
    main()
