"""独立子进程调用 DeepSeek：主服务通过 subprocess 调用本脚本，
网络层任何崩溃只影响本子进程，主服务自动降级规则模式。"""
import sys
import json


def main():
    req = json.loads(sys.stdin.read())
    import http.client
    import ssl
    body = {
        "model": req["model"],
        "messages": req["messages"],
        "temperature": req.get("temperature", 0.3),
        "max_tokens": req.get("max_tokens", 2000),
    }
    if req.get("json_mode"):
        body["response_format"] = {"type": "json_object"}
    base = req["base_url"].rstrip("/")
    if "://" in base:
        _, rest = base.split("://", 1)
    else:
        rest = base
    host = rest.split("/")[0]
    path = "/" + rest.split("/", 1)[1] if "/" in rest else ""
    path += "/chat/completions"

    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(host, timeout=req.get("timeout", 60), context=ctx)
    conn.request("POST", path, body=json.dumps(body), headers={
        "Authorization": f"Bearer {req['api_key']}",
        "Content-Type": "application/json",
    })
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    if resp.status != 200:
        print(json.dumps({"error": f"HTTP {resp.status}", "raw": raw[:300]}))
        sys.exit(1)
    content = json.loads(raw)["choices"][0]["message"]["content"]
    print(json.dumps({"content": content}, ensure_ascii=False))


if __name__ == "__main__":
    main()
