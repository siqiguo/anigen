# AniGen 资源管理 API 服务器

提供角色资源上传、管理等功能的后端 API 服务器。

## 功能特性

- ✅ RESTful API 设计
- ✅ 角色资源上传（包括三视图和表情）
- ✅ 角色列表查询和搜索
- ✅ 角色详情查看
- ✅ 角色更新和删除
- ✅ 图片文件服务
- ✅ CORS 支持（允许前端跨域访问）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务器

```bash
cd server
python app.py
```

服务器将在 `http://localhost:5000` 启动。

## API 端点

### 1. 创建角色

**POST** `/api/characters`

支持表单数据（multipart/form-data）上传，包含：
- `name`: 角色名称（必填）
- `description`: 角色描述
- `appearance`: 外观描述（必填）
- `personality`: 性格描述
- `age`: 年龄
- `gender`: 性别
- `style`: 风格
- `tags`: 标签（逗号分隔）
- `front_view`: 前视图图片文件
- `side_view`: 侧视图图片文件
- `back_view`: 后视图图片文件
- `expression_*`: 表情图片文件（如 `expression_happy`）

**响应示例：**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "主角小明",
    ...
  },
  "message": "角色创建成功"
}
```

### 2. 获取角色列表

**GET** `/api/characters`

**查询参数：**
- `keyword`: 关键词搜索
- `tags`: 标签过滤（逗号分隔）
- `style`: 风格过滤

**响应示例：**
```json
{
  "success": true,
  "data": [...],
  "count": 10
}
```

### 3. 获取角色详情

**GET** `/api/characters/<character_id>`

### 4. 更新角色

**PUT** `/api/characters/<character_id>`

**请求体（JSON）：**
```json
{
  "name": "新名称",
  "description": "新描述",
  ...
}
```

### 5. 删除角色

**DELETE** `/api/characters/<character_id>`

### 6. 获取图片

**GET** `/api/images/<image_path>`

返回图片文件。

## 数据存储

角色数据存储在 `assets/index.json` 文件中（使用现有的 AssetManager）。

图片文件存储在 `assets/images/character/` 目录下。

## 错误处理

所有错误响应格式：
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 开发说明

- 使用 Flask 作为 Web 框架
- 使用 flask-cors 处理跨域请求
- 集成现有的 `src/assets` 模块
- 文件上传大小限制：10MB
- 支持的图片格式：png, jpg, jpeg, gif, webp

