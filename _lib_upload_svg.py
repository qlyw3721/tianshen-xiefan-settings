#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把《神圣帝国示意图 v1.1》SVG 单独上传到资料库（新节点，父＝space 根）。
新文件走 drive 上传：get-upload-credential(parent-id) -> COS PUT(带返回 headers)
  -> import-local-file-async(confirm-key/task-id) -> query-progress。
"""
import json, os, subprocess, sys, time, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SKILL = r"D:/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"
API = os.path.join(SKILL, "space_api.py")
SVG = os.path.join(BASE, "天神下凡_神圣帝国示意图_v1.1.svg")
FNAME = "天神下凡_神圣帝国示意图_v1.1.svg"
TITLE = "天神下凡_神圣帝国示意图_v1.1"
SPACE = "xCFsStPd4bZ7lwkmk2pnL1"
PARENT = "xCFsStPd4bZ7lwkmk2pnL1"


def call(api, *args):
    out = subprocess.run([sys.executable, API, api, *args], capture_output=True, text=True, encoding="utf-8")
    raw = out.stdout.strip()
    if not raw:
        print("EMPTY STDOUT:", api, out.stderr[:400]); sys.exit(1)
    try:
        obj = json.loads(raw)
    except Exception:
        print("NON-JSON:", api, raw[:400]); sys.exit(1)
    if "error" in obj:
        print("API ERROR:", api, obj["error"]); sys.exit(1)
    return obj.get("data", obj)


def main():
    size = os.path.getsize(SVG)
    print("SVG size=", size)
    print("STEP1 credential")
    d = call("space.importer.get-upload-credential",
             "--file-name", FNAME, "--file-size", str(size), "--parent-id", PARENT)
    url = d["uploadUrl"]
    hdrs = d.get("headers", {})
    confirm_key = d.get("confirmKey", "")
    task_id = d.get("taskId", "")
    print("  uploadType=", d.get("uploadType"), " confirmKey=", confirm_key, " taskId=", task_id)

    print("STEP2 COS PUT")
    body = open(SVG, "rb").read()
    req = urllib.request.Request(url, data=body, method="PUT")
    for k, v in hdrs.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            print("  PUT status=", resp.status)
    except Exception as e:
        print("  PUT FAILED:", repr(e)); sys.exit(1)

    print("STEP3 import-local-file-async")
    d2 = call("space.importer.import-local-file-async",
              "--space-id", SPACE, "--parent-id", PARENT,
              "--file-name", FNAME, "--file-size", str(size), "--title", TITLE,
              "--confirm-key", confirm_key, "--task-id", task_id)
    print("  import resp=", json.dumps(d2, ensure_ascii=False)[:600])

    tid = d2.get("taskId") or d2.get("task_id") or task_id
    if tid:
        print("STEP4 query-progress taskId=", tid)
        for i in range(12):
            p = call("space.importer.query-import-file-progress", "--task-id", tid)
            print("  progress=", json.dumps(p, ensure_ascii=False)[:400])
            st = p.get("status") or p.get("state")
            if str(st).lower() in ("done", "completed", "success", "finished") or p.get("progress") == 100:
                break
            time.sleep(2)
    print("DONE")


if __name__ == "__main__":
    main()
