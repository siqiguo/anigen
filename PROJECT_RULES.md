# AniGen 项目规则文档

## 项目简介
AniGen是一个AI驱动的动画生成系统，旨在实现从文本剧本到完整动画的自动化生成流程。

## 系统架构

### 核心模块划分

#### 1. 剧本处理模块 (Script Module)
- **功能**: 接收、解析、分析剧本
- **输入**: 纯文本剧本
- **输出**: 结构化剧本数据（场景、角色、对话、动作描述等）
- **关键组件**:
  - 剧本解析器 (Script Parser)
  - 剧本分析器 (Script Analyzer)
  - 剧本验证器 (Script Validator)

#### 2. 分镜生成模块 (Storyboard Module)
- **功能**: 基于结构化剧本生成分镜脚本
- **输入**: 结构化剧本数据
- **输出**: 分镜脚本（包含镜头描述、画面构图、时长、转场等）
- **关键组件**:
  - 分镜规划器 (Storyboard Planner)
  - 镜头生成器 (Shot Generator)
  - 分镜优化器 (Storyboard Optimizer)

#### 3. 动画生成模块 (Animation Module)
- **功能**: 根据分镜脚本生成动画
- **输入**: 分镜脚本
- **输出**: 动画视频文件
- **关键组件**:
  - 图像生成器 (Image Generator)
  - 动画合成器 (Animation Composer)
  - 视频渲染器 (Video Renderer)

#### 4. 配置管理模块 (Config Module)
- **功能**: 管理系统配置、API密钥、模型参数等
- **关键组件**:
  - 配置加载器 (Config Loader)
  - 环境变量管理 (Environment Manager)

#### 5. 资源库模块 (Assets Module)
- **功能**: 管理角色、道具、场景、动作等可重用资源
- **输入**: 资源信息（名称、描述、图片等）
- **输出**: 资源对象和资源查询结果
- **关键组件**:
  - 资源模型 (Asset Models): 定义各种资源的数据结构
  - 资源管理器 (Asset Manager): 提供资源的增删改查功能
  - 资源存储 (Asset Storage): 管理资源的文件系统和索引

#### 6. 配置管理模块 (Config Module)
- **功能**: 管理系统配置、API密钥、模型参数等
- **关键组件**:
  - 配置加载器 (Config Loader)
  - 环境变量管理 (Environment Manager)

#### 7. 工具模块 (Utils Module)
- **功能**: 提供通用工具函数
- **关键组件**:
  - 日志工具 (Logger)
  - 文件处理工具 (File Handler)
  - 数据转换工具 (Data Converter)

## 数据流设计

```
用户输入剧本
    ↓
剧本处理模块 → 结构化剧本数据
    ↓
分镜生成模块 → 分镜脚本 (JSON/YAML)
    ↓                    ↑
资源库模块 ←─────────────┘ (提供角色、场景等资源)
    ↓
动画生成模块 → 动画视频文件
```

### 资源库模块数据流

```
资源添加/导入
    ↓
资源存储 (文件系统 + 索引)
    ↓
资源查询/匹配
    ↓
动画生成模块调用
```

## 数据格式规范

### 结构化剧本格式
```json
{
  "title": "剧本标题",
  "scenes": [
    {
      "scene_number": 1,
      "location": "场景地点",
      "time": "时间",
      "characters": ["角色1", "角色2"],
      "dialogue": [
        {
          "character": "角色1",
          "text": "对话内容",
          "emotion": "情绪"
        }
      ],
      "action": "动作描述",
      "notes": "备注"
    }
  ],
  "characters": {
    "角色1": {
      "description": "角色描述",
      "appearance": "外观描述"
    }
  }
}
```

### 分镜脚本格式
```json
{
  "storyboard": [
    {
      "shot_number": 1,
      "scene_number": 1,
      "shot_type": "镜头类型 (close-up/medium/wide)",
      "duration": 3.0,
      "description": "画面描述",
      "camera_angle": "拍摄角度",
      "characters": ["角色1"],
      "dialogue": "对话内容",
      "transition": "转场方式",
      "visual_style": "视觉风格描述"
    }
  ],
  "metadata": {
    "total_duration": 120.0,
    "total_shots": 40
  }
}
```

### 资源格式

#### 角色资源格式
```json
{
  "id": "资源唯一ID",
  "name": "角色名称",
  "resource_type": "character",
  "description": "角色详细描述",
  "appearance": "外观描述",
  "personality": "性格描述",
  "age": 25,
  "gender": "男",
  "style": "卡通",
  "tags": ["主角", "冒险者"],
  "image_path": "images/character/xxx.jpg",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### 场景资源格式
```json
{
  "id": "资源唯一ID",
  "name": "场景名称",
  "resource_type": "scene",
  "description": "场景详细描述",
  "location_type": "室外",
  "time_of_day": "白天",
  "weather": "晴朗",
  "mood": "神秘",
  "style": "写实",
  "tags": ["自然", "森林"],
  "image_path": "images/scene/xxx.jpg",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### 道具资源格式
```json
{
  "id": "资源唯一ID",
  "name": "道具名称",
  "resource_type": "prop",
  "description": "道具详细描述",
  "category": "武器",
  "size": "中等",
  "material": "金属",
  "style": "奇幻",
  "tags": ["武器", "剑"],
  "image_path": "images/prop/xxx.jpg",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### 动作资源格式
```json
{
  "id": "资源唯一ID",
  "name": "动作名称",
  "resource_type": "action",
  "description": "动作详细描述",
  "action_type": "走路",
  "duration": 2.0,
  "intensity": "中等",
  "target": "全身",
  "style": "卡通",
  "tags": ["移动", "基础动作"],
  "image_path": "images/action/xxx.jpg",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## API设计规范

### RESTful API端点设计

#### 剧本相关
- `POST /api/v1/script/parse` - 解析剧本
- `POST /api/v1/script/analyze` - 分析剧本

#### 分镜相关
- `POST /api/v1/storyboard/generate` - 生成分镜

#### 动画相关
- `POST /api/v1/animation/generate` - 生成动画

#### 资源库相关
- `POST /api/v1/assets/characters` - 添加角色资源
- `POST /api/v1/assets/props` - 添加道具资源
- `POST /api/v1/assets/scenes` - 添加场景资源
- `POST /api/v1/assets/actions` - 添加动作资源
- `GET /api/v1/assets/{resource_id}` - 获取资源详情
- `PUT /api/v1/assets/{resource_id}` - 更新资源
- `DELETE /api/v1/assets/{resource_id}` - 删除资源
- `GET /api/v1/assets` - 列出资源（支持类型、关键词、标签过滤）
- `GET /api/v1/assets/search` - 搜索资源

#### 任务相关
- `GET /api/v1/job/{job_id}/status` - 查询任务状态
- `GET /api/v1/job/{job_id}/result` - 获取结果

### 响应格式
```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "job_id": "任务ID（异步任务）"
}
```

## 配置文件结构

### config.yaml
```yaml
# API配置
apis:
  openai:
    api_key: ${OPENAI_API_KEY}
    model: "gpt-4"
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: "claude-3-opus"
  image_generation:
    provider: "stable-diffusion"  # stable-diffusion, dall-e, midjourney
    api_key: ${IMAGE_API_KEY}
  video_generation:
    provider: "runway"  # runway, pika, animatediff
    api_key: ${VIDEO_API_KEY}

# 生成参数
generation:
  storyboard:
    default_shot_duration: 3.0
    max_shots_per_scene: 10
  animation:
    fps: 24
    resolution: "1920x1080"
    output_format: "mp4"

# 资源库配置
assets:
  base_dir: "./assets"
  supported_image_formats: ["jpg", "jpeg", "png", "gif", "webp"]
  max_image_size_mb: 10
  index_file: "index.json"

# 系统配置
system:
  log_level: "INFO"
  output_dir: "./output"
  temp_dir: "./temp"
  max_concurrent_jobs: 5
```

## 错误处理规范

### 错误类型
1. **输入错误** (InputError): 用户输入格式错误或内容无效
2. **处理错误** (ProcessingError): 处理过程中的错误
3. **API错误** (APIError): 外部API调用失败
4. **系统错误** (SystemError): 系统内部错误

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "type": "InputError",
    "code": "INVALID_SCRIPT_FORMAT",
    "message": "剧本格式无效",
    "details": {}
  }
}
```

## 日志规范

### 日志级别
- DEBUG: 详细的调试信息
- INFO: 一般信息（默认）
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误

### 日志格式
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [MODULE] Message
```

## 测试规范

### 测试结构
- 单元测试: `tests/unit/`
- 集成测试: `tests/integration/`
- 测试数据: `tests/fixtures/`

### 测试覆盖率要求
- 核心模块: >= 80%
- 工具模块: >= 70%
- 整体覆盖率: >= 75%

## 开发工作流

### 分支策略
- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `fix/*`: 修复分支

### 提交规范
使用Conventional Commits格式:
- `feat: 新功能`
- `fix: 修复bug`
- `docs: 文档更新`
- `refactor: 代码重构`
- `test: 测试相关`
- `chore: 构建/工具相关`

## 性能要求

### 响应时间目标
- 剧本解析: < 5秒
- 分镜生成: < 30秒
- 动画生成: 根据时长，每10秒动画 < 2分钟

### 资源限制
- 内存使用: < 8GB (单任务)
- 临时文件: 自动清理，保留时间 < 24小时

## 安全规范

### API密钥管理
- 所有API密钥存储在环境变量中
- 配置文件不包含敏感信息
- 使用 `.env` 文件（不提交到版本控制）

### 输入验证
- 所有用户输入必须验证
- 防止注入攻击
- 文件大小限制

## 扩展性考虑

### 插件系统
- 支持自定义AI模型插件
- 支持自定义动画风格插件
- 插件接口标准化

### 多语言支持
- 代码注释和文档使用中文
- 用户界面支持中英文
- 错误消息支持多语言

## 部署要求

### 环境要求
- Python 3.10+
- Node.js 18+ (如需要前端)
- 足够的存储空间（用于生成的文件）

### 依赖管理
- Python: 使用 `requirements.txt` 或 `pyproject.toml`
- 前端: 使用 `package.json`

## 文档要求

### 必需文档
1. README.md - 项目介绍和快速开始
2. API文档 - API接口说明
3. 模块文档 - 各模块详细说明
4. 部署文档 - 部署和配置指南

### 代码文档
- 所有公共函数和类必须有文档字符串
- 复杂算法要有注释说明
- 使用类型提示提高代码可读性

