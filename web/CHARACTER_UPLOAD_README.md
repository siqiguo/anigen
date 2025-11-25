# 角色资源上传页面使用说明

## 功能概述

这是一个完整的角色资源管理系统，包括：
- 前端上传界面
- 后端 API 服务器
- 角色数据存储（使用 JSON 文件，可扩展为 SQLite）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务器

```bash
# 方式1：使用启动脚本
./server/start.sh

# 方式2：直接运行
cd server
python app.py
```

服务器将在 `http://localhost:5000` 启动。

### 3. 打开前端页面

在浏览器中打开 `web/character-upload.html`

## 使用流程

### 上传角色

1. 填写角色基本信息：
   - 角色名称（必填）
   - 外观描述（必填）
   - 其他可选信息（年龄、性别、风格等）

2. 上传三视图图片：
   - 前视图
   - 侧视图
   - 后视图

3. 上传表情图片（可选）：
   - 开心、悲伤、愤怒等8种标准表情

4. 点击"上传角色"按钮

### 查看角色列表

1. 点击"角色列表"标签页
2. 可以搜索和筛选角色
3. 查看角色详情或删除角色

## 数据存储说明

当前使用 JSON 文件存储（`assets/index.json`），这是轻量级的存储方案，适合：
- 小型项目
- 快速开发
- 不需要复杂查询的场景

### 未来扩展为 SQLite

如果需要使用 SQLite 数据库，可以：

1. 创建数据库适配器
2. 修改 `AssetManager` 使用数据库
3. 保持 API 接口不变

示例 SQLite 表结构：
```sql
CREATE TABLE characters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    appearance TEXT,
    personality TEXT,
    age INTEGER,
    gender TEXT,
    style TEXT,
    tags TEXT,
    front_view TEXT,
    side_view TEXT,
    back_view TEXT,
    expressions TEXT,
    created_at TEXT,
    updated_at TEXT
);
```

## API 端点

详细 API 文档请参考 `server/README.md`

## 注意事项

1. **文件大小限制**：单个图片文件最大 10MB
2. **支持格式**：png, jpg, jpeg, gif, webp
3. **服务器地址**：默认 `http://localhost:5000`，如需修改请编辑 `web/character-upload.js` 中的 `API_BASE_URL`
4. **CORS**：已配置允许跨域请求

## 故障排除

### 无法连接服务器

- 检查后端服务器是否正在运行
- 检查端口 5000 是否被占用
- 检查防火墙设置

### 文件上传失败

- 检查文件大小是否超过 10MB
- 检查文件格式是否支持
- 检查 `assets/images/character/` 目录权限

### 数据未保存

- 检查 `assets/` 目录权限
- 检查 `assets/index.json` 文件是否可写

