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

# 添加角色
character = manager.add_character(
    name="主角",
    description="勇敢的冒险者",
    appearance="年轻男性，黑色短发",
    personality="勇敢、乐观",
    age=25,
    gender="男",
    style="卡通",
    tags=["主角", "冒险者"],
    image_path="./images/character.jpg"
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
- `image_path`: 图片路径（相对路径）
- `metadata`: 额外元数据
- `created_at`: 创建时间
- `updated_at`: 更新时间

以及各资源类型特有的字段。

## API参考

详细API文档请参考各模块的代码文档字符串。

