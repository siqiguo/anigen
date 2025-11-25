# 随机角色生成功能使用指南

## 功能概述

已成功实现随机角色生成功能，可以自动生成角色数据、填充表单，并生成对应的 prompt。

## 功能测试

✅ **随机角色生成器测试通过**

测试结果：
- 可以生成随机角色数据（名称、外观、性格、年龄、性别、风格、标签）
- 可以创建角色对象
- 可以生成完整的 prompt（三视图 + 8种表情）

## 使用方法

### 1. 启动服务器（需要先安装依赖）

```bash
# 安装依赖（推荐使用虚拟环境）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务器
cd server
python app.py
```

### 2. 打开前端页面

在浏览器中打开 `web/character-upload.html`

### 3. 使用随机生成功能

1. 点击页面上的 **"🎲 随机生成角色"** 按钮
2. 系统会自动：
   - 生成随机角色数据
   - 填充表单所有字段
   - 显示角色预览信息
3. 你可以：
   - **直接上传**：如果满意，点击"上传角色"
   - **修改后上传**：调整任何字段后再上传
   - **生成图片**：点击"打开 Prompt 生成器"链接，使用生成的 prompt 生成图片

## API 端点

### POST /api/characters/random

生成随机角色数据。

**请求示例：**
```bash
curl -X POST http://localhost:5000/api/characters/random \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "character": {
      "name": "小明",
      "description": "一个25岁的男性角色，勇敢、乐观、善良。",
      "appearance": "年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装，棕色皮靴，腰间挂着剑",
      "personality": "勇敢、乐观、善良",
      "age": 25,
      "gender": "男",
      "style": "anime",
      "tags": ["主角", "冒险者", "男性"]
    },
    "prompts": {
      "front_view": "Create a front view character design sheet...",
      "side_view": "...",
      "back_view": "...",
      "expression_happy": "...",
      ...
    }
  },
  "message": "随机角色生成成功"
}
```

## 随机生成的内容

- **名称**：从20个预设名称中随机选择
- **外观**：从10种预设外观模板中随机选择
- **性格**：与外观匹配的性格描述
- **年龄**：15-50岁随机
- **性别**：男/女随机
- **风格**：anime/cartoon/realistic/3D/pixar 随机
- **标签**：2-4个随机标签

## 测试脚本

运行测试脚本验证功能：

```bash
cd server
python3 test_random.py
```

## 下一步

1. **生成图片**：使用生成的 prompt 调用 Gemini API 或其他图片生成服务
2. **保存角色**：将生成的角色上传到资源库
3. **批量生成**：可以扩展功能支持批量生成多个随机角色

## 注意事项

- 随机生成的角色数据是随机的，可能需要多次生成才能得到满意的结果
- 生成的角色数据可以直接用于上传，也可以修改后再上传
- Prompt 已经自动生成，可以直接用于图片生成

