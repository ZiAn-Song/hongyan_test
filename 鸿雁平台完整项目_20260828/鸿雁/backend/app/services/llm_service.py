"""DeepSeek LLM 服务层（会议决策：弃用百度千帆，统一走 DeepSeek V4）。

稳定性设计：
- LLM 网络调用通过 **独立子进程**（scripts/llm_call.py）完成。
- 主服务进程完全不接触外部 HTTPS —— 规避 macOS 上 Python 进程内
  SSL 网络调用的偶发段错误（该崩溃无 Python traceback、直接杀死进程）。
- 子进程崩溃/超时/断网时 call_llm 返回 None，匹配流程自动降级规则模式，
  主服务永远存活。
"""
import json
import os
import subprocess
import sys

from app.config import settings

_SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'scripts', 'llm_call.py')


def call_llm(messages: list[dict], temperature: float = 0.3,
             max_tokens: int = 2000, json_mode: bool = False,
             timeout: int = 90) -> str | None:
    """调用 DeepSeek Chat Completions；失败返回 None（上层自动降级）。"""
    api_key = settings.DEEPSEEK_API_KEY
    if not api_key:
        return None

    req = {
        "api_key": api_key,
        "base_url": settings.DEEPSEEK_BASE_URL,
        "model": settings.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "json_mode": json_mode,
        "timeout": timeout,
    }
    try:
        proc = subprocess.run(
            [sys.executable, _SCRIPT],
            input=json.dumps(req), capture_output=True, text=True,
            timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        print("[LLM] 子进程超时，降级", flush=True)
        return None
    except Exception as e:  # noqa: BLE001
        print(f"[LLM] 子进程启动失败: {e}", flush=True)
        return None

    try:
        out = json.loads(proc.stdout)
    except (json.JSONDecodeError, TypeError):
        print(f"[LLM] 子进程异常输出: {proc.stdout[:200]} / {proc.stderr[:300]}", flush=True)
        return None
    if "content" not in out:
        print(f"[LLM] 调用失败: {out.get('error')}", flush=True)
        return None
    return out["content"]


def call_llm_json(messages: list[dict], temperature: float = 0.2,
                  max_tokens: int = 2500, timeout: int = 90) -> dict | list | None:
    """调用并解析 JSON 输出；自动抽取正文中的 JSON 块。失败返回 None。"""
    import re

    content = call_llm(messages, temperature=temperature,
                       max_tokens=max_tokens, json_mode=True, timeout=timeout)
    if not content:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        m = re.search(r"[\[{].*[\]}]", content, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                return None
    return None
