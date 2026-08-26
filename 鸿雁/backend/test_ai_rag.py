import httpx
import time

BASE = "http://127.0.0.1:8000"
c = httpx.Client(timeout=30)

# --- 登录 ---
print("=== 登录 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "202320211001",
    "password": "test123456",
    "user_type": "personal",
})
token = r.json()["access_token"]
auth = {"Authorization": f"Bearer {token}"}
print(f"  OK: {r.json()['name']}")

# --- RAG 索引 ---
print("\n=== 1. 触发 RAG 索引 ===")
r = c.post(f"{BASE}/api/ai/index", headers=auth)
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  Indexed: {data.get('indexed')} chunks")
print(f"  Sources: {data.get('sources')}")

# --- 搜索 ---
print("\n=== 2. 搜索 '乡村振兴' ===")
r = c.get(f"{BASE}/api/ai/search?q=乡村振兴", headers=auth)
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  Query: {data.get('query')}")
print(f"  Results: {len(data.get('results', []))}")
for i, result in enumerate(data.get("results", [])[:3], 1):
    content_preview = result["content"][:80].replace("\n", " ")
    print(f"  [{i}] source={result['source_type']}, score={result['score']}")
    print(f"      content: {content_preview}...")

print("\n=== 3. 搜索 '社会实践' ===")
r = c.get(f"{BASE}/api/ai/search?q=社会实践", headers=auth)
data = r.json()
print(f"  Results: {len(data.get('results', []))}")

print("\n=== 4. 搜索 '新疆喀什' ===")
r = c.get(f"{BASE}/api/ai/search?q=新疆喀什", headers=auth)
data = r.json()
print(f"  Results: {len(data.get('results', []))}")
for result in data.get("results", [])[:2]:
    content_preview = result["content"][:80].replace("\n", " ")
    print(f"  [{result['source_type']}] score={result['score']}: {content_preview}...")

# --- AI 聊天（SSE 流式）---
print("\n=== 5. AI 聊天（流式）===")
print("  发送消息: 你好，介绍一下鸿雁平台")
print("  等待流式响应...")

try:
    with c.stream("POST", f"{BASE}/api/ai/chat", headers=auth, json={
        "message": "你好，介绍一下鸿雁平台",
        "use_rag": False,
    }) as resp:
        print(f"  Status: {resp.status_code}")
        received = 0
        for line in resp.iter_lines():
            if line.startswith("data:"):
                data = line[5:].strip()
                if data == "[DONE]":
                    print("\n  [流式结束]")
                    break
                elif data.startswith("[ERROR]"):
                    print(f"\n  [错误] {data[7:]}")
                    break
                else:
                    print(data, end="", flush=True)
                    received += 1
        if received == 0:
            print("  (未收到任何响应内容)")
except Exception as e:
    print(f"  请求失败: {e}")

# --- AI 聊天 + RAG ---
print("\n\n=== 6. AI 聊天 + RAG 上下文增强 ===")
print("  发送消息: 有哪些团队在做乡村振兴？")
print("  等待流式响应...")

try:
    with c.stream("POST", f"{BASE}/api/ai/chat", headers=auth, json={
        "message": "有哪些团队在做乡村振兴？",
        "use_rag": True,
    }) as resp:
        print(f"  Status: {resp.status_code}")
        received = 0
        for line in resp.iter_lines():
            if line.startswith("data:"):
                data = line[5:].strip()
                if data == "[DONE]":
                    print("\n  [流式结束]")
                    break
                elif data.startswith("[ERROR]"):
                    print(f"\n  [错误] {data[7:]}")
                    break
                else:
                    print(data, end="", flush=True)
                    received += 1
        if received == 0:
            print("  (未收到任何响应内容)")
except Exception as e:
    print(f"  请求失败: {e}")

c.close()
print("\n\n=== All AI + RAG tests completed! ===")
