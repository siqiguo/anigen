# 资源库模块

## 概述

资源库模块提供角色、道具、场景、动作等资源的存储和管理功能，为动画生成提供可重用的资源。

## 功能特性

- **资源类型**: 支持角色、道具、场景、动作四种资源类型
- **资源管理**: 完整的增删改查功能
- **资源搜索**: 支持关键词、标签、类型等多维度搜索
- **图片管理**: 自动管理资源图片的存储和路径
- **索引系统**: 基于JSON的轻量级索引系统

## 资源类型

### 1. 角色 (Character)
- 外观描述
- 性格描述
- 年龄、性别
- 风格
- **三视图**：前视图、侧视图、后视图
- **表情**：支持多种常见表情（happy, sad, angry, surprised, neutral, scared等）

### 2. 道具 (Prop)
- 道具类别
- 尺寸、材质
- 风格

### 3. 场景 (Scene)
- 场景类型（室内/室外等）
- 时间、天气
- 氛围、风格

### 4. 动作 (Action)
- 动作类型
- 时长、强度
- 目标对象（全身/手部/面部等）
- 风格

## 使用方法

### 基本使用

```python
from src.assets import AssetManager, ResourceType

# 创建资源管理器
manager = AssetManager(base_dir="./assets")

# 添加角色（包含三视图和表情）
character = manager.add_character(
    name="主角",
    description="勇敢的冒险者",
    appearance="年轻男性，黑色短发",
    personality="勇敢、乐观",
    age=25,
    gender="男",
    style="卡通",
    tags=["主角", "冒险者"],
    front_view="./images/character_front.jpg",  # 前视图
    side_view="./images/character_side.jpg",    # 侧视图
    back_view="./images/character_back.jpg",    # 后视图
    expressions={  # 表情字典
        "happy": "./images/character_happy.jpg",
        "sad": "./images/character_sad.jpg",
        "angry": "./images/character_angry.jpg",
        "surprised": "./images/character_surprised.jpg",
    }
)

# 添加场景
scene = manager.add_scene(
    name="森林",
    description="神秘的森林场景",
    location_type="室外",
    time_of_day="白天",
    mood="神秘",
    style="写实",
    tags=["自然", "森林"],
    image_path="./images/forest.jpg"
)

# 搜索资源
characters = manager.search_resources(
    keyword="主角",
    resource_type=ResourceType.CHARACTER
)

# 查找匹配的场景
matching_scene = manager.find_matching_scene(
    location_type="室外",
    mood="神秘"
)
```

### 资源管理

```python
# 获取资源
resource = manager.get_resource(resource_id)

# 更新资源
resource.description = "更新后的描述"
manager.update_resource(resource)

# 删除资源
manager.delete_resource(resource_id)

# 列出所有资源
all_resources = manager.list_resources()
characters_only = manager.list_resources(ResourceType.CHARACTER)

# 管理角色表情
manager.add_character_expression(
    character_id=character.id,
    expression_name="scared",
    expression_image_path="./images/character_scared.jpg"
)

# 移除表情
manager.remove_character_expression(character.id, "sad")

# 更新三视图
manager.update_character_views(
    character_id=character.id,
    front_view="./images/new_front.jpg",
    side_view="./images/new_side.jpg"
)

# 访问角色的三视图和表情
print(f"前视图: {character.front_view}")
print(f"侧视图: {character.side_view}")
print(f"后视图: {character.back_view}")
print(f"表情列表: {list(character.expressions.keys())}")
print(f"开心表情: {character.get_expression('happy')}")
```

## 目录结构

```
assets/
├── index.json              # 资源索引文件
├── images/                 # 图片存储目录
│   ├── character/         # 角色图片
│   ├── prop/              # 道具图片
│   ├── scene/             # 场景图片
│   └── action/            # 动作图片
├── character/             # 角色资源目录（预留）
├── prop/                  # 道具资源目录（预留）
├── scene/                 # 场景资源目录（预留）
└── action/                # 动作资源目录（预留）
```

## 数据格式

资源以JSON格式存储在索引文件中，每个资源包含：

- `id`: 唯一标识符
- `name`: 资源名称
- `resource_type`: 资源类型
- `description`: 详细描述
- `tags`: 标签列表
- `image_path`: 图片路径（相对路径，保留用于兼容性）
- `metadata`: 额外元数据
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 角色资源特有字段

- `appearance`: 外观描述
- `personality`: 性格描述
- `age`: 年龄
- `gender`: 性别
- `style`: 风格
- `front_view`: 前视图图片路径
- `side_view`: 侧视图图片路径
- `back_view`: 后视图图片路径
- `expressions`: 表情字典，格式为 `{"表情名称": "图片路径"}`

### 常见表情名称

建议使用以下标准表情名称：
- `happy`: 开心
- `sad`: 悲伤
- `angry`: 愤怒
- `surprised`: 惊讶
- `neutral`: 中性/平静
- `scared`: 害怕
- `excited`: 兴奋
- `confused`: 困惑
- `disgusted`: 厌恶
- `embarrassed`: 尴尬

也可以根据项目需求自定义表情名称。

## Nano Banana Prompt 生成

为了方便使用 Nano Banana AI 图像生成工具为角色生成所有必需的图片，提供了专门的 prompt 生成器。

### 快速使用

```python
from src.assets import AssetManager
from src.assets.prompt_generator import generate_character_prompts

# 创建角色
manager = AssetManager()
character = manager.add_character(
    name="主角",
    appearance="年轻男性，黑色短发，蓝色眼睛",
    style="anime"
)

# 生成所有 prompt
prompts = generate_character_prompts(character)

# 使用 prompt 调用 Nano Banana API 生成图片
# front_image = nano_banana.generate(prompts["front_view"])
# side_image = nano_banana.generate(prompts["side_view"])
# ...
```

### Prompt 生成器功能

- **自动生成三视图 prompt**：前视图、侧视图、后视图
- **自动生成表情 prompt**：支持8种标准表情（happy, sad, angry, surprised, neutral, scared, excited, confused）
- **自定义表情列表**：可以指定需要生成的表情
- **简化版 prompt**：适合支持上下文记忆的 API
- **风格一致性**：确保所有 prompt 使用相同的角色描述和风格

详细说明请参考：
- `src/assets/nano_banana_prompts.md` - 完整的 prompt 格式说明文档
- `src/assets/prompt_generator.py` - Prompt 生成器实现
- `src/assets/nano_banana_example.py` - 使用示例

## API参考

详细API文档请参考各模块的代码文档字符串。

