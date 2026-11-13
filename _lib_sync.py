#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""资料库增量重传校验脚本（配合每日自动化使用）。
- check: 计算本地两份工作稿的 sha256，与状态文件比对，输出哪些文件自上次上传后变化。
- save:  把当前两份工作稿的 sha256 写入状态文件。
状态文件: 同目录 .lib_sync_state.json
"""
import sys, os, json, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, ".lib_sync_state.json")
FILES = {
    "docx": os.path.join(BASE, "天神下凡设定集_归纳整理版_v1.2.docx"),
    "md":   os.path.join(BASE, "天神下凡设定集_归纳整理版_v1.2.md"),
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    state = load_state()
    if mode == "save":
        new = {}
        for k, p in FILES.items():
            if os.path.exists(p):
                new[k] = {"sha256": sha256(p)}
        json.dump(new, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("SAVED:", json.dumps(new, ensure_ascii=False))
        return
    # check
    result = {}
    any_changed = False
    for k, p in FILES.items():
        if not os.path.exists(p):
            result[k] = "MISSING"
            continue
        cur = sha256(p)
        old = state.get(k, {}).get("sha256")
        changed = (old != cur)
        result[k] = "CHANGED" if changed else "UNCHANGED"
        if changed:
            any_changed = True
    result["_any_changed"] = any_changed
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
