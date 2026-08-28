"""独立子进程调用火山方舟嵌入 API（同 llm_call.py 的隔离设计）。"""
import sys
import json


def main():
    req = json.loads(sys.stdin.read())
    import http.client
    import ssl

    body = {"model": req["model"], "input": req["input"]}
    base = req["base_url"].rstrip("/")
    if "://" in base:
        _, rest = base.split("://", 1)
    else:
        rest = base
    host = rest.split("/")[0]
    path = "/" + rest.split("/", 1)[1] if "/" in rest else ""
    path += "/embeddings/multimodal"

    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(host, timeout=req.get("timeout", 60), context=ctx)
    conn.request("POST", path, body=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                 headers={"Authorization": f"Bearer {req['api_key']}",
                          "Content-Type": "application/json"})
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    if resp.status != 200:
        print(json.dumps({"error": f"HTTP {resp.status}", "raw": raw[:300]}, ensure_ascii=False))
        sys.exit(1)
    data = json.loads(raw)
    # 兼容三种返回结构：
    # 火山方舟 multimodal: {"data":{"embedding":[...]}}
    # OpenAI 风格:         {"data":[{"embedding":[...]}]}
    # 裸返回:              {"embedding":[...]}
    d = data.get("data")
    if isinstance(d, dict):
        emb = d.get("embedding")
    elif isinstance(d, list) and d:
        emb = d[0].get("embedding")
    else:
        emb = data.get("embedding")
    if not emb:
        print(json.dumps({"error": "no embedding in response", "raw": raw[:300]}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps({"embedding": emb}, ensure_ascii=False))


if __name__ == "__main__":
    main()
