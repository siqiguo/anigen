# 剧本到分镜生成流程 - 快速参考

## 流程图位置

- **详细流程图（Mermaid）**: `docs/STORYBOARD_FLOW.md`
- **ASCII流程图**: `docs/STORYBOARD_FLOW_DETAILED.md`
- **本文档**: 快速参考

## 核心流程概览

```
用户输入剧本
    ↓
Web界面验证
    ↓
API请求 → Flask服务器
    ↓
剧本解析 (ScriptParser)
    ├─ 提取标题
    ├─ 解析场景
    └─ 提取角色
    ↓
资源匹配 (ResourceMatcher) [可选]
    ├─ 匹配角色
    ├─ 匹配场景
    ├─ 匹配道具
    └─ 匹配动作
    ↓
分镜生成 (StoryboardGenerator)
    ├─ 遍历场景
    ├─ 生成镜头
    └─ 添加资源引用
    ↓
结果返回
    ↓
前端展示
```

## 关键模块

### 1. ScriptParser (剧本解析)
- **位置**: `src/script/parser.py`
- **功能**: 将文本剧本解析为结构化数据
- **输入**: 纯文本剧本
- **输出**: 结构化剧本数据 (JSON)

### 2. ResourceMatcher (资源匹配)
- **位置**: `src/storyboard/matcher.py`
- **功能**: 从资源库中匹配已有资源
- **输入**: 角色/场景/道具/动作描述
- **输出**: 资源引用列表

### 3. StoryboardGenerator (分镜生成)
- **位置**: `src/storyboard/generator.py`
- **功能**: 基于剧本生成分镜脚本
- **输入**: 结构化剧本数据
- **输出**: 分镜脚本对象

## API端点

### POST /api/storyboard/generate
生成分镜脚本

**请求**:
```json
{
  "script_text": "剧本文本",
  "title": "剧本标题（可选）",
  "prefer_existing_resources": true
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "title": "...",
    "storyboard": [...],
    "metadata": {...}
  }
}
```

## 数据流转

```
纯文本剧本
  ↓ ScriptParser.parse()
结构化剧本数据
  ↓ ResourceMatcher.match_*()
资源引用列表
  ↓ StoryboardGenerator.generate_from_script()
分镜脚本对象
  ↓ Storyboard.to_dict()
分镜脚本字典
  ↓ JSON响应
前端展示
```

## 资源匹配算法

### 角色匹配
- 名称相似度 × 0.4
- 描述相似度 × 0.3
- 标签匹配度 × 0.2
- 风格匹配 × 0.1

### 场景匹配
- 场景类型 × 0.25
- 氛围 × 0.25
- 风格 × 0.20
- 时间 × 0.15
- 天气 × 0.15
- 描述相似度 × 0.30

## 关键文件

- **服务器**: `server/app.py`
- **前端页面**: `web/storyboard-generator.html`
- **前端脚本**: `web/storyboard-generator.js`
- **剧本解析**: `src/script/parser.py`
- **分镜生成**: `src/storyboard/generator.py`
- **资源匹配**: `src/storyboard/matcher.py`

## 使用示例

```python
from src.assets import AssetManager
from src.script import ScriptParser
from src.storyboard import StoryboardGenerator

# 初始化
asset_manager = AssetManager()
parser = ScriptParser()
generator = StoryboardGenerator(asset_manager)

# 解析剧本
script_data = parser.parse(script_text)

# 生成分镜
storyboard = generator.generate_from_script(
    script_data,
    prefer_existing_resources=True
)
```

## 性能指标

- 剧本解析: < 1秒
- 资源匹配: < 2秒
- 分镜生成: < 3秒
- 总响应时间: < 5秒

