"""
AniGen 资源管理 API 服务器

提供角色资源上传、管理等功能。
"""

import os
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.assets import AssetManager, Character, ResourceType
from server.character_generator import RandomCharacterGenerator
from src.assets.prompt_generator import NanoBananaPromptGenerator
from src.script import ScriptParser
from src.storyboard import StoryboardGenerator

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = Path(__file__).parent.parent / "assets" / "images" / "character"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# 初始化资源管理器
ASSETS_DIR = Path(__file__).parent.parent / "assets"
asset_manager = AssetManager(base_dir=str(ASSETS_DIR))

# 初始化生成器
character_generator = RandomCharacterGenerator()
prompt_generator = NanoBananaPromptGenerator()
script_parser = ScriptParser()
storyboard_generator = StoryboardGenerator(asset_manager)


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """首页"""
    return jsonify({
        "message": "AniGen 资源管理 API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/characters": "上传角色资源",
            "GET /api/characters": "获取角色列表",
            "GET /api/characters/<id>": "获取角色详情",
            "PUT /api/characters/<id>": "更新角色",
            "DELETE /api/characters/<id>": "删除角色",
            "GET /api/images/<path>": "获取图片",
            "POST /api/storyboard/generate": "生成分镜脚本",
            "POST /api/script/parse": "解析剧本",
        }
    })


@app.route("/api/characters", methods=["POST"])
def create_character():
    """创建角色资源
    
    支持表单数据和 JSON 数据
    """
    try:
        # 获取表单数据
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        appearance = request.form.get("appearance", "").strip()
        personality = request.form.get("personality", "").strip()
        age = request.form.get("age")
        gender = request.form.get("gender", "").strip()
        style = request.form.get("style", "").strip()
        tags_str = request.form.get("tags", "").strip()
        
        # 验证必填字段
        if not name:
            return jsonify({"success": False, "error": "角色名称不能为空"}), 400
        
        if not appearance:
            return jsonify({"success": False, "error": "外观描述不能为空"}), 400
        
        # 解析标签
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
        
        # 解析年龄
        age_int = None
        if age:
            try:
                age_int = int(age)
            except ValueError:
                return jsonify({"success": False, "error": "年龄必须是数字"}), 400
        
        # 处理图片上传（新格式：支持动态标签）
        images = {}
        
        # 收集所有图片（新格式：image_file_0, image_label_0 等）
        image_index = 0
        while True:
            file_key = f"image_file_{image_index}"
            label_key = f"image_label_{image_index}"
            
            if file_key not in request.files:
                break
            
            file = request.files[file_key]
            label = request.form.get(label_key, "").strip()
            
            if file and file.filename and allowed_file(file.filename) and label:
                # 生成唯一文件名
                ext = Path(file.filename).suffix.lower()
                unique_filename = f"{uuid.uuid4()}{ext}"
                filepath = UPLOAD_FOLDER / unique_filename
                file.save(filepath)
                images[label] = str(filepath.relative_to(ASSETS_DIR))
            
            image_index += 1
        
        # 向后兼容：处理旧格式的三视图和表情
        if not images:
            front_view = None
            side_view = None
            back_view = None
            expressions = {}
            
            # 三视图
            if "front_view" in request.files:
                file = request.files["front_view"]
                if file and file.filename and allowed_file(file.filename):
                    ext = Path(file.filename).suffix.lower()
                    unique_filename = f"{uuid.uuid4()}{ext}"
                    filepath = UPLOAD_FOLDER / unique_filename
                    file.save(filepath)
                    images["front_view"] = str(filepath.relative_to(ASSETS_DIR))
            
            if "side_view" in request.files:
                file = request.files["side_view"]
                if file and file.filename and allowed_file(file.filename):
                    ext = Path(file.filename).suffix.lower()
                    unique_filename = f"{uuid.uuid4()}{ext}"
                    filepath = UPLOAD_FOLDER / unique_filename
                    file.save(filepath)
                    images["side_view"] = str(filepath.relative_to(ASSETS_DIR))
            
            if "back_view" in request.files:
                file = request.files["back_view"]
                if file and file.filename and allowed_file(file.filename):
                    ext = Path(file.filename).suffix.lower()
                    unique_filename = f"{uuid.uuid4()}{ext}"
                    filepath = UPLOAD_FOLDER / unique_filename
                    file.save(filepath)
                    images["back_view"] = str(filepath.relative_to(ASSETS_DIR))
            
            # 表情图片
            for key in request.files:
                if key.startswith("expression_"):
                    expr_name = key.replace("expression_", "")
                    file = request.files[key]
                    if file and file.filename and allowed_file(file.filename):
                        ext = Path(file.filename).suffix.lower()
                        unique_filename = f"{uuid.uuid4()}{ext}"
                        filepath = UPLOAD_FOLDER / unique_filename
                        file.save(filepath)
                        images[f"expression_{expr_name}"] = str(filepath.relative_to(ASSETS_DIR))
        
        # 创建角色（使用asset_manager，但需要手动设置images）
        character = asset_manager.add_character(
            name=name,
            description=description,
            appearance=appearance,
            personality=personality,
            age=age_int,
            gender=gender if gender else None,
            style=style,
            tags=tags,
        )
        
        # 添加图片
        for label, image_path in images.items():
            character.add_image(label, image_path)
        
        # 更新索引
        asset_manager.update_resource(character)
        
        return jsonify({
            "success": True,
            "data": character.to_dict(),
            "message": "角色创建成功"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/characters", methods=["GET"])
def list_characters():
    """获取角色列表
    
    查询参数:
    - keyword: 关键词搜索
    - tags: 标签过滤（逗号分隔）
    - style: 风格过滤
    """
    try:
        keyword = request.args.get("keyword", "").strip()
        tags_str = request.args.get("tags", "").strip()
        style = request.args.get("style", "").strip()
        
        # 解析标签
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else None
        
        # 搜索角色
        if keyword or tags or style:
            characters = asset_manager.search_resources(
                keyword=keyword if keyword else None,
                tags=tags,
                resource_type=ResourceType.CHARACTER
            )
            # 过滤风格
            if style:
                characters = [c for c in characters if isinstance(c, Character) and c.style == style]
        else:
            characters = asset_manager.list_resources(ResourceType.CHARACTER)
        
        # 转换为字典列表
        characters_data = [c.to_dict() for c in characters if isinstance(c, Character)]
        
        return jsonify({
            "success": True,
            "data": characters_data,
            "count": len(characters_data)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/characters/<character_id>", methods=["GET"])
def get_character(character_id: str):
    """获取角色详情"""
    try:
        character = asset_manager.get_resource(character_id)
        
        if not character or not isinstance(character, Character):
            return jsonify({
                "success": False,
                "error": "角色不存在"
            }), 404
        
        return jsonify({
            "success": True,
            "data": character.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/characters/<character_id>", methods=["PUT"])
def update_character(character_id: str):
    """更新角色"""
    try:
        character = asset_manager.get_resource(character_id)
        
        if not character or not isinstance(character, Character):
            return jsonify({
                "success": False,
                "error": "角色不存在"
            }), 404
        
        # 获取 JSON 数据
        data = request.get_json() or {}
        
        # 更新字段
        if "name" in data:
            character.name = data["name"]
        if "description" in data:
            character.description = data["description"]
        if "appearance" in data:
            character.appearance = data["appearance"]
        if "personality" in data:
            character.personality = data["personality"]
        if "age" in data:
            character.age = data["age"]
        if "gender" in data:
            character.gender = data["gender"]
        if "style" in data:
            character.style = data["style"]
        if "tags" in data:
            character.tags = data["tags"]
        
        # 更新资源
        asset_manager.update_resource(character)
        
        return jsonify({
            "success": True,
            "data": character.to_dict(),
            "message": "角色更新成功"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/characters/<character_id>", methods=["DELETE"])
def delete_character(character_id: str):
    """删除角色"""
    try:
        success = asset_manager.delete_resource(character_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": "角色不存在"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "角色删除成功"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/images/<path:image_path>")
def get_image(image_path: str):
    """获取图片文件"""
    try:
        # 安全检查：确保路径在 assets 目录内
        full_path = ASSETS_DIR / image_path
        if not str(full_path).startswith(str(ASSETS_DIR)):
            return jsonify({"success": False, "error": "无效的图片路径"}), 400
        
        if not full_path.exists():
            return jsonify({"success": False, "error": "图片不存在"}), 404
        
        return send_from_directory(
            str(full_path.parent),
            full_path.name
        )
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/characters/random", methods=["POST"])
def generate_random_character():
    """生成随机角色
    
    请求体（可选）:
    - generate_image: 是否生成图片（需要 api_key）
    - api_key: Gemini API Key（如果 generate_image 为 true）
    """
    try:
        data = request.get_json() or {}
        generate_image = data.get("generate_image", False)
        api_key = data.get("api_key", "").strip()
        
        # 生成随机角色数据
        random_data = character_generator.generate_random_character()
        
        # 创建角色对象（用于生成 prompt）
        character = Character(
            name=random_data["name"],
            description=random_data["description"],
            appearance=random_data["appearance"],
            personality=random_data["personality"],
            age=random_data["age"],
            gender=random_data["gender"],
            style=random_data["style"],
            tags=random_data["tags"],
        )
        
        # 生成 prompt
        prompts = prompt_generator.generate_all_prompts(character)
        
        # 格式化 prompts（prompt_generator 返回的是字符串字典）
        formatted_prompts = {}
        for key, prompt_text in prompts.items():
            if isinstance(prompt_text, str):
                formatted_prompts[key] = prompt_text
            elif hasattr(prompt_text, 'prompt'):
                formatted_prompts[key] = prompt_text.prompt
            else:
                formatted_prompts[key] = str(prompt_text)
        
        result = {
            "character": random_data,
            "prompts": formatted_prompts
        }
        
        # 如果需要生成图片
        if generate_image and api_key:
            result["images"] = {}
            result["message"] = "注意：图片生成功能需要在前端调用 Gemini API"
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "随机角色生成成功"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/script/parse", methods=["POST"])
def parse_script():
    """解析剧本文本
    
    请求体（JSON）:
    {
        "script_text": "剧本文本内容",
        "title": "剧本标题（可选）"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "请求体不能为空"}), 400
        
        script_text = data.get("script_text", "").strip()
        if not script_text:
            return jsonify({"success": False, "error": "剧本文本不能为空"}), 400
        
        title = data.get("title")
        
        # 解析剧本
        script_data = script_parser.parse(script_text, title)
        
        return jsonify({
            "success": True,
            "data": script_data,
            "message": "剧本解析成功"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/storyboard/generate", methods=["POST"])
def generate_storyboard():
    """生成分镜脚本
    
    请求体（JSON）:
    {
        "script_data": {
            "title": "剧本标题",
            "scenes": [...],
            "characters": {...}
        },
        "prefer_existing_resources": true  // 是否优先使用资源库资源
    }
    
    或者直接提供剧本文本:
    {
        "script_text": "剧本文本内容",
        "title": "剧本标题（可选）",
        "prefer_existing_resources": true
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "请求体不能为空"}), 400
        
        prefer_existing_resources = data.get("prefer_existing_resources", True)
        
        # 如果提供了script_text，先解析剧本
        if "script_text" in data:
            script_text = data.get("script_text", "").strip()
            if not script_text:
                return jsonify({"success": False, "error": "剧本文本不能为空"}), 400
            
            title = data.get("title")
            script_data = script_parser.parse(script_text, title)
        elif "script_data" in data:
            script_data = data["script_data"]
        else:
            return jsonify({"success": False, "error": "必须提供script_text或script_data"}), 400
        
        # 生成分镜脚本
        storyboard = storyboard_generator.generate_from_script(
            script_data,
            prefer_existing_resources=prefer_existing_resources
        )
        
        # 转换为字典格式
        storyboard_dict = storyboard.to_dict()
        
        return jsonify({
            "success": True,
            "data": storyboard_dict,
            "message": "分镜脚本生成成功"
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route("/api/resources/list", methods=["GET"])
def list_resources():
    """获取资源库中的资源列表
    
    查询参数:
    - resource_type: 资源类型（character, scene, prop, action）
    - keyword: 关键词搜索
    """
    try:
        resource_type_str = request.args.get("resource_type")
        keyword = request.args.get("keyword", "").strip()
        
        resource_type = None
        if resource_type_str:
            try:
                resource_type = ResourceType(resource_type_str)
            except ValueError:
                return jsonify({"success": False, "error": f"无效的资源类型: {resource_type_str}"}), 400
        
        # 获取资源列表
        if keyword:
            resources = asset_manager.search_resources(
                keyword=keyword,
                resource_type=resource_type
            )
        else:
            resources = asset_manager.list_resources(resource_type)
        
        # 转换为字典
        resources_data = [r.to_dict() for r in resources]
        
        return jsonify({
            "success": True,
            "data": resources_data,
            "count": len(resources_data)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))  # 默认使用 5001 端口，避免与 AirPlay 冲突
    print(f"启动服务器...")
    print(f"资源目录: {ASSETS_DIR}")
    print(f"上传目录: {UPLOAD_FOLDER}")
    print(f"访问地址: http://localhost:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)

