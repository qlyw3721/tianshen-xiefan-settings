# -*- coding: utf-8 -*-
"""资料库 md 覆盖上传（COS 直传通道）——v2.52 双机同步 C 件
链路：get-upload-credential(uploadType=cos) → COS PUT → import-local-file-async
      → query-import-file-progress → rename-node
用法：python _lib_upload_md.py <本地md路径> <目标nodeId> <spaceId> <期望标题>
"""
import sys, json, time, urllib.request, os
sys.path.insert(0, "D:/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library")
from _common import http_request, unwrap_data

md_path, node_id, space_id, want_title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
size = os.path.getsize(md_path)
file_name = os.path.basename(md_path)
blob = open(md_path, 'rb').read()
assert len(blob) == size

# 1 凭证
cred = unwrap_data(http_request("POST", "/space/api/agent/v1/get-upload-credential",
    body={"fileName": file_name, "fileSize": size, "nodeBlockId": node_id, "parentId": space_id},
    timeout=15.0))
assert cred.get("uploadType") == "cos", cred.get("uploadType")
url, cos_key, task_id = cred["uploadUrl"], cred["cosKey"], cred["taskId"]
print("cred ok, cosKey", cos_key)

# 2 COS PUT
req = urllib.request.Request(url, data=blob, method="PUT",
    headers={"Content-Type": "application/octet-stream"})
with urllib.request.urlopen(req, timeout=180) as r:
    print("COS PUT", r.status)

# 3 导入（覆盖目标节点）
imp = unwrap_data(http_request("POST", "/space/api/agent/v1/import-local-file-async",
    body={"confirmKey": cos_key, "cosKey": cos_key, "taskId": task_id,
          "fileName": file_name, "fileSize": size,
          "nodeBlockId": node_id, "spaceId": space_id,
          "title": os.path.splitext(file_name)[0]},
    timeout=60.0))
print("import resp", json.dumps(imp, ensure_ascii=False)[:300])

# 4 轮询
for i in range(40):
    time.sleep(3)
    try:
        pr = unwrap_data(http_request("POST", "/space/api/agent/v1/query-import-file-progress",
            body={"taskId": task_id}, timeout=20.0))
    except Exception as e:
        print("poll err", e); continue
    st = json.dumps(pr, ensure_ascii=False)
    print("poll", i, st[:200])
    low = st.lower()
    if '"status":"done"' in low or '"progress":100' in low or '"state":"done"' in low:
        break
    if 'fail' in low or 'error' in low:
        raise SystemExit("import failed")
else:
    print("poll timeout, continue anyway")

# 5 标题对齐（若服务器未改标题）
info = unwrap_data(http_request("POST", "/space/api/agent/v1/node-info", body={"nodeId": node_id}, timeout=15.0))
node = info.get("node", info)
print("now title:", node.get("title"), "version:", node.get("version"))
if node.get("title") != want_title:
    rn = unwrap_data(http_request("POST", "/space/api/agent/v1/rename-node",
        body={"nodeId": node_id, "title": want_title}, timeout=20.0))
    print("renamed ->", json.dumps(rn, ensure_ascii=False)[:200])
    info = unwrap_data(http_request("POST", "/space/api/agent/v1/node-info", body={"nodeId": node_id}, timeout=15.0))
    node = info.get("node", info)
    print("final title:", node.get("title"), "version:", node.get("version"))
