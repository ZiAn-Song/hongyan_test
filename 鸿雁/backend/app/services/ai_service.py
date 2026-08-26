import ast
import json

import httpx

from app.config import settings

APPBUILDER_BASE = "https://qianfan.baidubce.com/v2/app"


def _parse_event(data: str):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(data)
        except (ValueError, SyntaxError):
            return None


def _extract_from_event(chunk):
    if not isinstance(chunk, dict):
        return [], None

    answer = chunk.get("answer", "")
    if answer:
        return [answer], None

    content = chunk.get("content", [])
    events = content if isinstance(content, list) else [content]

    texts = []
    for event in events:
        if not isinstance(event, dict):
            continue

        event_status = event.get("event_status", "")
        event_code = event.get("event_code", 0)
        content_type = event.get("content_type", "")

        if event_status == "error" or event_code >= 400:
            error = event.get("event_message", "AI 服务错误")
            return [], error

        if content_type == "text":
            outputs = event.get("outputs", {})
            text = outputs.get("text", "")
            if isinstance(text, str) and text:
                texts.append(text)

    return texts, None


async def stream_ai_chat(message: str, context: str = ""):
    headers = {
        "Authorization": settings.APPBUILDER_TOKEN,
        "Content-Type": "application/json",
    }

    query = message
    if context:
        query = f"参考资料：\n{context}\n\n用户问题：{message}"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            conv_resp = await client.post(
                f"{APPBUILDER_BASE}/conversation",
                headers=headers,
                json={"app_id": settings.APPBUILDER_APP_ID},
            )

            if conv_resp.status_code != 200:
                error_msg = "创建会话失败"
                try:
                    err_data = conv_resp.json()
                    error_msg = err_data.get("error_msg", err_data.get("message", error_msg))
                except Exception:
                    pass
                yield f"data: [ERROR] {error_msg}\n\n"
                yield "data: [DONE]\n\n"
                return

            conversation_id = conv_resp.json().get("conversation_id")
            if not conversation_id:
                yield "data: [ERROR] 未获取到会话ID\n\n"
                yield "data: [DONE]\n\n"
                return

            async with client.stream(
                "POST",
                f"{APPBUILDER_BASE}/conversation/runs",
                headers=headers,
                json={
                    "app_id": settings.APPBUILDER_APP_ID,
                    "conversation_id": conversation_id,
                    "query": query,
                    "stream": True,
                    "response_mode": "streaming",
                },
            ) as resp:
                if resp.status_code != 200:
                    yield f"data: [ERROR] 对话请求失败 (HTTP {resp.status_code})\n\n"
                    yield "data: [DONE]\n\n"
                    return

                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue

                    data = line[5:].strip()
                    if not data or data == "[DONE]":
                        continue

                    chunk = _parse_event(data)
                    if chunk is None:
                        continue

                    texts, error = _extract_from_event(chunk)
                    if error:
                        yield f"data: [ERROR] {error}\n\n"
                        yield "data: [DONE]\n\n"
                        return

                    for text in texts:
                        yield f"data: {text}\n\n"

    except httpx.ConnectError:
        yield "data: [ERROR] 无法连接到 AI 服务\n\n"
    except httpx.TimeoutException:
        yield "data: [ERROR] AI 服务响应超时\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"

    yield "data: [DONE]\n\n"
