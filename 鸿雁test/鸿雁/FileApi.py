from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os
import re

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 确保data目录存在
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# 获取文件完整路径
def get_file_path(filename):
    """获取安全的文件路径"""
    # 简单安全检查，移除路径字符
    safe_name = filename.replace('../', '').replace('..\\', '')
    return os.path.join(DATA_DIR, safe_name + '.json')


# 1. 读取JSON文件接口
@app.route('/api/read', methods=['POST'])
def read_json_file():
    """读取JSON文件内容"""
    try:
        # 获取请求参数
        data = request.get_json()

        if not data or 'filename' not in data:
            return jsonify({
                "code": 400,
                "message": "参数错误",
                "data": None
            }), 400

        filename = data['filename']
        filepath = get_file_path(filename)

        # 检查文件是否存在
        if not os.path.exists(filepath):
            return jsonify({
                "code": 404,
                "message": f"文件 {filename}.json 不存在",
                "data": None
            }), 404

        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)

        return jsonify({
            "code": 200,
            "message": "读取成功",
            "data": content
        })

    except json.JSONDecodeError:
        return jsonify({
            "code": 500,
            "message": "文件内容不是有效的JSON格式",
            "data": None
        }), 500
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"读取文件失败: {str(e)}",
            "data": None
        }), 500


# 2. 写入JSON文件接口
@app.route('/api/write', methods=['POST'])
def write_json_file():
    """写入JSON文件（覆盖）"""
    try:
        # 获取请求参数
        data = request.get_json()

        if not data:
            return jsonify({
                "code": 400,
                "message": "请求体为空",
                "data": None
            }), 400

        if 'filename' not in data:
            return jsonify({
                "code": 400,
                "message": "缺少文件名参数",
                "data": None
            }), 400

        if 'content' not in data:
            return jsonify({
                "code": 400,
                "message": "缺少文件内容参数",
                "data": None
            }), 400

        filename = data['filename']
        content = data['content']
        filepath = get_file_path(filename)

        # 写入文件（覆盖模式）
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        # 获取文件大小
        file_size = os.path.getsize(filepath)

        return jsonify({
            "code": 200,
            "message": "文件保存成功",
            "data": {
                "filename": filename + '.json',
                "path": filepath,
                "size": file_size,
                "content": content
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"写入文件失败: {str(e)}",
            "data": None
        }), 500


# 3. 列出所有JSON文件接口
@app.route('/api/list', methods=['GET'])
def list_json_files():
    """列出所有JSON文件"""
    try:
        files = []
        if os.path.exists(DATA_DIR):
            for file in os.listdir(DATA_DIR):
                if file.endswith('.json'):
                    filepath = os.path.join(DATA_DIR, file)
                    file_size = os.path.getsize(filepath)
                    file_mtime = os.path.getmtime(filepath)

                    files.append({
                        "name": file,
                        "size": file_size,
                        "modified": file_mtime
                    })

        return jsonify({
            "code": 200,
            "message": "获取文件列表成功",
            "data": {
                "files": files,
                "count": len(files)
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取文件列表失败: {str(e)}",
            "data": None
        }), 500


# 4. 删除JSON文件接口
@app.route('/api/delete', methods=['POST'])
def delete_json_file():
    """删除JSON文件"""
    try:
        data = request.get_json()

        if not data or 'filename' not in data:
            return jsonify({
                "code": 400,
                "message": "缺少文件名参数",
                "data": None
            }), 400

        filename = data['filename']
        filepath = get_file_path(filename)

        # 检查文件是否存在
        if not os.path.exists(filepath):
            return jsonify({
                "code": 404,
                "message": f"文件 {filename}.json 不存在",
                "data": None
            }), 404

        # 删除文件
        os.remove(filepath)

        return jsonify({
            "code": 200,
            "message": "文件删除成功",
            "data": {
                "filename": filename + '.json'
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"删除文件失败: {str(e)}",
            "data": None
        }), 500


# 5. 检查文件是否存在接口
@app.route('/api/exists', methods=['POST'])
def check_file_exists():
    """检查文件是否存在"""
    try:
        data = request.get_json()

        if not data or 'filename' not in data:
            return jsonify({
                "code": 400,
                "message": "缺少文件名参数",
                "data": None
            }), 400

        filename = data['filename']
        filepath = get_file_path(filename)

        exists = os.path.exists(filepath)

        return jsonify({
            "code": 200,
            "message": "检查完成",
            "data": {
                "filename": filename + '.json',
                "exists": exists
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"检查文件失败: {str(e)}",
            "data": None
        }), 500





@app.route('/api/task', methods=['POST'])
def baidu_api_task():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({
            "code": 400,
            "message": "缺少query参数",
            "data": None
        }), 400

    query = data['query']

    os.environ[
        "APPBUILDER_TOKEN"] = 'Bearer bce-v3/ALTAK-KoSvRYnNpqd8ASf0DXXDb/a40b6fe4b51c881160ec944b4a9f47555e7e615b'
    app_id = '7021ffd1-a0c4-4172-94bf-a4c69f4e2b78'

    # 初始化智能体
    client = appbuilder.AppBuilderClient(app_id)

    # 创建会话
    conversation_id = client.create_conversation()

    # 运行对话（启用流式）
    message = client.run(conversation_id, query, file_ids=[], stream=True)

    def serialize_object(obj):
        """递归序列化对象为可JSON序列化的字典"""
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, dict):
            return {k: serialize_object(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [serialize_object(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # 如果是对象，尝试获取其属性字典
            return {k: serialize_object(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
        elif hasattr(obj, '__slots__'):
            # 如果对象使用__slots__
            return {slot: serialize_object(getattr(obj, slot, None)) for slot in obj.__slots__ if hasattr(obj, slot)}
        else:
            # 其他情况，转换为字符串
            return str(obj)

    def generate():
        """生成器函数，用于流式返回数据"""
        try:
            answer_accumulator = ""

            # 每次迭代返回AppBuilderClientAnswer结构
            for content in message.content:
                if hasattr(content, 'answer') and content.answer:
                    # print(content.answer)


                    answer = re.sub(r'\^(\[\d+\])+\^', '', content.answer)
                    print( "aaaa:"+answer)
                    answer_accumulator += answer

                    # 返回当前片段的答案
                    yield f"data: {json.dumps({'type': 'text', 'data': answer, 'accumulated': answer_accumulator})}\n\n"

                # 处理其他类型的事件
                if hasattr(content, 'events') and content.events:
                    for event in content.events:
                        content_type = event.content_type
                        detail = event.detail

                        # 根据content类型对事件详情进行解析并返回
                        if content_type == "code":
                            code_detail = data_class.CodeDetail(**detail)
                            yield f"data: {json.dumps({'type': 'code', 'data': code_detail.code})}\n\n"

                        elif content_type == "text":
                            text_detail = data_class.TextDetail(**detail)

                            yield f"data: {json.dumps({'type': 'text_detail', 'data': text_detail.text})}\n\n"

                        elif content_type == "image":
                            image_detail = data_class.ImageDetail(**detail)
                            yield f"data: {json.dumps({'type': 'image', 'data': image_detail.url})}\n\n"

                        elif content_type == "rag":
                            rag_detail = data_class.RAGDetail(**detail)
                            if len(rag_detail.references) > 0:
                                # 使用序列化函数处理references
                                serialized_references = serialize_object(rag_detail.references)
                                yield f"data: {json.dumps({'type': 'rag', 'data': serialized_references})}\n\n"

                        elif content_type == "function_call":
                            function_call_detail = data_class.FunctionCallDetail(**detail)
                            # 使用序列化函数处理
                            serialized_detail = serialize_object(function_call_detail)
                            yield f"data: {json.dumps({'type': 'function_call', 'data': serialized_detail})}\n\n"

                        elif content_type == "audio":
                            audio_detail = data_class.AudioDetail(**detail)
                            # 使用序列化函数处理
                            serialized_detail = serialize_object(audio_detail)
                            yield f"data: {json.dumps({'type': 'audio', 'data': serialized_detail})}\n\n"

                        elif content_type == "video":
                            video_detail = data_class.VideoDetail(**detail)
                            # 使用序列化函数处理
                            serialized_detail = serialize_object(video_detail)
                            yield f"data: {json.dumps({'type': 'video', 'data': serialized_detail})}\n\n"

                        elif content_type == "status":
                            status_detail = data_class.StatusDetail(**detail)
                            # 使用序列化函数处理
                            serialized_detail = serialize_object(status_detail)
                            yield f"data: {json.dumps({'type': 'status', 'data': serialized_detail})}\n\n"

                        else:
                            default_detail = data_class.DefaultDetail(**detail)
                            # 使用序列化函数处理
                            serialized_detail = serialize_object(default_detail)
                            yield f"data: {json.dumps({'type': 'default', 'data': serialized_detail})}\n\n"

            # 流结束标志
            yield f"data: {json.dumps({'type': 'done', 'message': 'Stream completed', 'final_answer': answer_accumulator})}\n\n"

        except Exception as e:
            # 错误处理
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error in stream generation: {error_traceback}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'traceback': error_traceback})}\n\n"

    # 返回流式响应
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )



if __name__ == '__main__':
    print("启动JSON文件管理API...")
    print("访问地址: http://localhost:5000")
    print("API接口:")
    print("  POST /api/read    - 读取JSON文件")
    print("  POST /api/write   - 写入JSON文件")
    print("  GET  /api/list    - 列出所有文件")
    print("  POST /api/delete  - 删除JSON文件")
    print("  POST /api/exists  - 检查文件是否存在")
    print("  POST /api/task    - 问答")

    app.run(debug=True, host='0.0.0.0', port=5000)