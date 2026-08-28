"""嵌入向量服务（火山方舟 doubao-embedding-vision-251215）。

与 llm_service 同样的稳定性设计：网络调用走独立子进程 scripts/embed_call.py，
主服务进程不接触外部 HTTPS；无 key / 子进程崩溃时全部降级，不影响匹配主流程。

生产 PostgreSQL + PG Vector 时，把本模块的 `search_similar` 换成
`SELECT ... ORDER BY embedding <=> query_vec LIMIT k` 即可（结构已对齐）。
"""
import json
import math
import os
import subprocess
import sys

from app.config import settings

_SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'scripts', 'embed_call.py')


def _call_ark(input_items: list[dict], timeout: int = 60) -> list[float] | None:
    api_key = settings.EMBEDDING_API_KEY
    if not api_key or api_key.startswith("填入"):
        return None
    req = {
        "api_key": api_key,
        "base_url": settings.EMBEDDING_BASE_URL,
        "model": settings.EMBEDDING_MODEL,
        "input": input_items,
        "timeout": timeout,
    }
    try:
        proc = subprocess.run([sys.executable, _SCRIPT],
                              input=json.dumps(req, ensure_ascii=False),
                              capture_output=True, text=True, timeout=timeout + 10)
    except (subprocess.TimeoutExpired, Exception) as e:  # noqa: BLE001
        print(f"[EMB] 子进程失败: {e}", flush=True)
        return None
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        with open('/tmp/emb_stderr_full.txt', 'a') as f:
            f.write('==== ' + req['input'][0]['text'][:40] + ' ====\n' + proc.stderr[-2000:] + '\n')
        return None
    if "embedding" not in out:
        print(f"[EMB] 调用失败: {out.get('error')}", flush=True)
        return None
    return out["embedding"]


def embed_text(text: str) -> list[float] | None:
    """文本 → 向量。空文本/失败返回 None。"""
    text = (text or "").strip()
    if not text:
        return None
    return _call_ark([{"type": "text", "text": text[:2000]}])


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def build_resource_text_demand(d) -> str:
    """需求 → 嵌入源文本"""
    parts = [d.title, d.pain_point, d.description, d.expected_goal, d.supply_tags]
    return " ".join(p for p in parts if p)


def build_resource_text_supply(s) -> str:
    """供给 → 嵌入源文本"""
    parts = [s.provider, s.services, s.tech_advantages, s.use_cases, s.border_fit]
    return " ".join(p for p in parts if p)


def build_resource_text_talent(t) -> str:
    """人才 → 嵌入源文本"""
    parts = [t.team, t.field, t.core_tech, t.west_scene, t.application, t.cases]
    return " ".join(p for p in parts if p)
