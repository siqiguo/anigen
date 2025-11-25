# 分镜生成模块

## 模块简介

分镜生成模块提供从结构化剧本数据生成分镜脚本的功能。核心特性是**优先使用资源库中的已有资源**，在分镜描述中明确标注资源来源，提高资源复用率和生成效率。

## 核心功能

1. **智能资源匹配**: 根据剧本描述自动从资源库中匹配最合适的角色、场景、道具、动作资源
2. **资源来源标注**: 在分镜描述中明确标注使用的资源及其来源
3. **分镜脚本生成**: 基于剧本自动生成包含镜头类型、画面描述、时长等完整信息的分镜脚本

## 模块结构

```
storyboard/
├── __init__.py          # 模块导出
├── models.py            # 数据模型（Storyboard, Shot, ResourceReference等）
├── generator.py         # 分镜生成器
├── matcher.py           # 资源匹配器
└── README.md           # 本文档
```

## 数据模型

### Storyboard（分镜脚本）

包含完整的分镜脚本信息，包括：
- `title`: 标题
- `shots`: 镜头列表
- `metadata`: 元数据
- `total_duration`: 总时长（自动计算）
- `total_shots`: 总镜头数（自动计算）

### Shot（镜头）

表示一个分镜镜头，包含：
- `shot_number`: 镜头编号
- `scene_number`: 场景编号
- `shot_type`: 镜头类型（特写/中景/全景等）
- `duration`: 时长（秒）
- `description`: 画面描述（包含资源来源标注）
- `camera_angle`: 拍摄角度
- `characters`: 角色列表
- `dialogue`: 对话内容
- `transition`: 转场方式
- `visual_style`: 视觉风格
- **资源引用字段**:
  - `character_resources`: 角色资源引用列表
  - `scene_resource`: 场景资源引用
  - `prop_resources`: 道具资源引用列表
  - `action_resources`: 动作资源引用列表

### ResourceReference（资源引用）

用于在分镜中引用资源库中的资源：
- `resource_id`: 资源ID
- `resource_type`: 资源类型
- `resource_name`: 资源名称
- `match_score`: 匹配分数（0-1）
- `match_reason`: 匹配原因说明

## 使用方法

### 基本使用

```python
from src.assets import AssetManager
from src.storyboard import StoryboardGenerator

# 初始化资源管理器
asset_manager = AssetManager(base_dir="./assets")

# 创建分镜生成器
generator = StoryboardGenerator(
    asset_manager=asset_manager,
    default_shot_duration=3.0
)

# 准备剧本数据
script_data = {
    "title": "示例剧本",
    "scenes": [
        {
            "scene_number": 1,
            "location": "神秘森林",
            "time": "白天",
            "characters": ["主角小明"],
            "dialogue": [
                {
                    "character": "主角小明",
                    "text": "这里是什么地方？",
                    "emotion": "惊讶"
                }
            ],
            "action": "主角环顾四周",
            "notes": "神秘"
        }
    ],
    "characters": {
        "主角小明": {
            "description": "勇敢的年轻冒险者",
            "appearance": "年轻男性，黑色短发"
        }
    }
}

# 生成分镜脚本（优先使用资源库资源）
storyboard = generator.generate_from_script(
    script_data,
    prefer_existing_resources=True
)

# 查看生成的分镜
for shot in storyboard.shots:
    print(f"镜头 {shot.shot_number}: {shot.description}")
    if shot.scene_resource:
        print(f"  使用场景资源: {shot.scene_resource.resource_name}")
    if shot.character_resources:
        for char_ref in shot.character_resources:
            print(f"  使用角色资源: {char_ref.resource_name}")
```

### 资源匹配

```python
from src.storyboard import ResourceMatcher

# 创建资源匹配器
matcher = ResourceMatcher(asset_manager)

# 匹配角色
character_match = matcher.match_character(
    name="主角",
    description="勇敢的冒险者",
    style="卡通"
)
if character_match:
    character, ref = character_match
    print(f"匹配到角色: {ref.resource_name} (匹配度: {ref.match_score:.2f})")

# 匹配场景
scene_match = matcher.match_scene(
    location_type="室外",
    description="神秘森林",
    mood="神秘"
)
if scene_match:
    scene, ref = scene_match
    print(f"匹配到场景: {ref.resource_name} (匹配度: {ref.match_score:.2f})")
```

## 资源匹配算法

资源匹配器使用多维度匹配算法：

### 角色匹配
- **名称相似度** (权重: 40%): 使用字符串相似度算法
- **描述相似度** (权重: 30%): 考虑关键词匹配
- **标签匹配** (权重: 20%): 标签交集比例
- **风格匹配** (权重: 10%): 风格完全匹配

### 场景匹配
- **场景类型匹配** (权重: 25%): 室内/室外等
- **氛围匹配** (权重: 25%): 情绪氛围
- **风格匹配** (权重: 20%): 视觉风格
- **时间匹配** (权重: 15%): 白天/夜晚等
- **天气匹配** (权重: 15%): 天气状况
- **描述相似度** (权重: 30%): 文本相似度

### 道具和动作匹配
- 使用名称、类别、描述等多维度匹配
- 支持批量匹配多个道具/动作

## 分镜描述格式

生成的分镜描述会自动包含资源来源标注，格式如下：

```
场景: 神秘森林（来自资源库） | 角色: 主角小明（来自资源库） | 动作: 主角环顾四周 | 对话: 这里是什么地方？（情绪: 惊讶）
```

如果资源库中没有匹配的资源，则使用原始描述：

```
场景: 神秘森林 | 角色: 主角小明 | 动作: 主角环顾四周 | 对话: 这里是什么地方？（情绪: 惊讶）
```

## 输出格式

分镜脚本可以导出为JSON格式：

```python
# 导出为字典
storyboard_dict = storyboard.to_dict()

# 从字典加载
storyboard = Storyboard.from_dict(storyboard_dict)
```

JSON格式示例：

```json
{
  "title": "示例剧本",
  "storyboard": [
    {
      "shot_number": 1,
      "scene_number": 1,
      "shot_type": "close-up",
      "duration": 3.0,
      "description": "场景: 神秘森林（来自资源库） | 角色: 主角小明（来自资源库） | ...",
      "camera_angle": "正面平视",
      "characters": ["主角小明"],
      "dialogue": "这里是什么地方？",
      "transition": "cut",
      "visual_style": "写实",
      "character_resources": [
        {
          "resource_id": "xxx",
          "resource_type": "character",
          "resource_name": "主角小明",
          "match_score": 0.85,
          "match_reason": "名称相似度: 0.90; 描述相似度: 0.75"
        }
      ],
      "scene_resource": {
        "resource_id": "yyy",
        "resource_type": "scene",
        "resource_name": "神秘森林",
        "match_score": 0.92,
        "match_reason": "场景类型匹配; 氛围匹配; 描述相似度: 0.88"
      }
    }
  ],
  "metadata": {
    "total_duration": 3.0,
    "total_shots": 1,
    "source": "script",
    "prefer_existing_resources": true
  }
}
```

## 配置选项

### StoryboardGenerator 参数

- `asset_manager`: 资源管理器实例（必需）
- `default_shot_duration`: 默认镜头时长，默认 3.0 秒
- `default_shot_type`: 默认镜头类型，默认 `ShotType.MEDIUM`

### 资源匹配参数

- `min_score`: 最小匹配分数阈值，默认 0.3（0-1之间）
- 可以通过调整阈值来控制匹配的严格程度

## 最佳实践

1. **资源库准备**: 在生成分镜前，确保资源库中有足够的角色、场景等资源
2. **匹配阈值**: 根据实际需求调整 `min_score` 参数，平衡匹配准确性和覆盖率
3. **资源标注**: 生成的分镜描述中会自动标注资源来源，便于后续动画生成时直接使用
4. **风格一致性**: 建议在资源库中保持统一的风格，便于匹配和复用

## 扩展功能

未来可以扩展的功能：
- 支持自定义匹配算法
- 支持资源优先级设置
- 支持资源组合（多个资源组合使用）
- 支持资源替换建议
- 支持分镜优化建议

