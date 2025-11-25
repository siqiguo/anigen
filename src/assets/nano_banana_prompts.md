# Nano Banana 角色图片生成 Prompt 格式说明

## 概述

本文档提供了使用 Nano Banana AI 图像生成工具为角色生成所有必需图片的 prompt 格式说明。根据用户提供的角色描述，可以生成角色的三视图和多种常见表情。

## 角色图片需求

每个角色资源需要以下图片：

1. **三视图**：
   - 前视图（Front View）
   - 侧视图（Side View）
   - 后视图（Back View）

2. **常见表情**（至少包含以下）：
   - happy（开心）
   - sad（悲伤）
   - angry（愤怒）
   - surprised（惊讶）
   - neutral（中性/平静）
   - scared（害怕）
   - excited（兴奋）
   - confused（困惑）

## Prompt 格式模板

### 基础角色描述变量

在以下所有 prompt 模板中，使用 `{character_description}` 作为占位符，替换为用户提供的角色描述。

角色描述应包含：
- 外观特征（年龄、性别、发型、发色、眼睛颜色等）
- 服装描述（上衣、下装、鞋子、配饰等）
- 风格（卡通、写实、二次元等）
- 其他特征（身高、体型、特殊标记等）

### 1. 三视图生成 Prompt

#### 前视图（Front View）

```
Create a front view character design sheet illustration of: {character_description}

Requirements:
- Full body front view, character facing forward
- White or transparent background
- Consistent character design with detailed appearance
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style} (replace with actual style like "anime", "cartoon", "realistic")
```

#### 侧视图（Side View）

```
Create a side view character design sheet illustration of: {character_description}

Requirements:
- Full body side view (profile), character facing left or right
- White or transparent background
- Must match the front view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}
```

#### 后视图（Back View）

```
Create a back view character design sheet illustration of: {character_description}

Requirements:
- Full body back view, character facing away
- White or transparent background
- Must match the front and side view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}
```

### 2. 表情生成 Prompt

所有表情图片应保持角色外观一致，只改变面部表情。

#### 通用表情 Prompt 模板

```
Create a character portrait of: {character_description}

Requirements:
- Character showing {expression_name} expression ({expression_description})
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- Facial expression should be clear and expressive
- High quality, clean line art or rendered illustration
- Style: {style}
```

#### 具体表情 Prompt

**Happy（开心）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a happy, joyful, smiling expression
- Eyes should be bright and cheerful, mouth showing a genuine smile
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Sad（悲伤）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a sad, melancholic expression
- Eyes should look downcast or teary, mouth slightly downturned
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Angry（愤怒）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing an angry, furious expression
- Eyebrows furrowed, eyes narrowed or glaring, mouth showing anger
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Surprised（惊讶）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a surprised, shocked expression
- Eyes wide open, eyebrows raised, mouth open in an "O" shape
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Neutral（中性/平静）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a neutral, calm, expressionless expression
- Eyes looking straight ahead, relaxed facial features, mouth in a neutral position
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Scared（害怕）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a scared, frightened expression
- Eyes wide with fear, eyebrows raised, mouth slightly open
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Excited（兴奋）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing an excited, enthusiastic expression
- Eyes bright and wide, eyebrows raised, mouth open in a big smile or cheer
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

**Confused（困惑）**
```
Create a character portrait of: {character_description}

Requirements:
- Character showing a confused, puzzled expression
- Eyes looking slightly off to the side, one eyebrow raised, mouth slightly open
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- High quality, clean line art or rendered illustration
- Style: {style}
```

## 完整生成流程

### 步骤 1：准备角色描述

收集完整的角色信息：
- 从 `Character` 对象获取：`appearance`, `personality`, `age`, `gender`, `style`
- 组合成完整的角色描述字符串

### 步骤 2：生成三视图

按顺序生成：
1. 前视图（使用前视图 prompt）
2. 侧视图（使用侧视图 prompt，确保引用前视图保持一致）
3. 后视图（使用后视图 prompt，确保引用前视图和侧视图保持一致）

### 步骤 3：生成表情

为每个需要的表情生成图片：
- 使用对应的表情 prompt
- 确保所有表情图片中的角色外观与三视图保持一致

### 步骤 4：保存图片

将生成的图片保存到对应的路径：
- 三视图：`{character_id}_front.jpg`, `{character_id}_side.jpg`, `{character_id}_back.jpg`
- 表情：`{character_id}_expression_{expression_name}.jpg`

## Python 实现示例

```python
from src.assets import AssetManager, Character

def generate_character_prompts(character: Character) -> Dict[str, str]:
    """根据角色对象生成所有图片的 prompt
    
    Args:
        character: 角色对象
        
    Returns:
        包含所有 prompt 的字典，key 为图片类型，value 为 prompt 文本
    """
    # 构建完整的角色描述
    character_description = f"{character.appearance}"
    if character.age:
        character_description += f", {character.age} years old"
    if character.gender:
        character_description += f", {character.gender}"
    if character.style:
        character_description += f", {character.style} style"
    
    prompts = {}
    
    # 三视图 prompts
    style = character.style or "anime"
    
    prompts["front_view"] = f"""Create a front view character design sheet illustration of: {character_description}

Requirements:
- Full body front view, character facing forward
- White or transparent background
- Consistent character design with detailed appearance
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    prompts["side_view"] = f"""Create a side view character design sheet illustration of: {character_description}

Requirements:
- Full body side view (profile), character facing left or right
- White or transparent background
- Must match the front view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    prompts["back_view"] = f"""Create a back view character design sheet illustration of: {character_description}

Requirements:
- Full body back view, character facing away
- White or transparent background
- Must match the front and side view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    # 表情 prompts
    expression_templates = {
        "happy": "happy, joyful, smiling expression. Eyes should be bright and cheerful, mouth showing a genuine smile",
        "sad": "sad, melancholic expression. Eyes should look downcast or teary, mouth slightly downturned",
        "angry": "angry, furious expression. Eyebrows furrowed, eyes narrowed or glaring, mouth showing anger",
        "surprised": "surprised, shocked expression. Eyes wide open, eyebrows raised, mouth open in an 'O' shape",
        "neutral": "neutral, calm, expressionless expression. Eyes looking straight ahead, relaxed facial features, mouth in a neutral position",
        "scared": "scared, frightened expression. Eyes wide with fear, eyebrows raised, mouth slightly open",
        "excited": "excited, enthusiastic expression. Eyes bright and wide, eyebrows raised, mouth open in a big smile or cheer",
        "confused": "confused, puzzled expression. Eyes looking slightly off to the side, one eyebrow raised, mouth slightly open",
    }
    
    for expr_name, expr_desc in expression_templates.items():
        prompts[f"expression_{expr_name}"] = f"""Create a character portrait of: {character_description}

Requirements:
- Character showing a {expr_desc}
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- Facial expression should be clear and expressive
- High quality, clean line art or rendered illustration
- Style: {style}"""
    
    return prompts


def generate_all_character_images(character: Character, nano_banana_api) -> None:
    """使用 nano banana 生成角色的所有图片
    
    Args:
        character: 角色对象
        nano_banana_api: nano banana API 客户端
    """
    prompts = generate_character_prompts(character)
    
    # 生成三视图
    front_image = nano_banana_api.generate(prompts["front_view"])
    side_image = nano_banana_api.generate(prompts["side_view"])
    back_image = nano_banana_api.generate(prompts["back_view"])
    
    # 生成表情
    expression_images = {}
    for expr_name in ["happy", "sad", "angry", "surprised", "neutral", "scared", "excited", "confused"]:
        prompt_key = f"expression_{expr_name}"
        if prompt_key in prompts:
            image = nano_banana_api.generate(prompts[prompt_key])
            expression_images[expr_name] = image
    
    # 保存图片并更新角色
    manager = AssetManager()
    
    # 保存三视图
    manager.update_character_views(
        character_id=character.id,
        front_view=front_image,
        side_view=side_image,
        back_view=back_image
    )
    
    # 保存表情
    for expr_name, image_path in expression_images.items():
        manager.add_character_expression(
            character_id=character.id,
            expression_name=expr_name,
            expression_image_path=image_path
        )
```

## 注意事项

1. **一致性要求**：
   - 在所有 prompt 中强调角色外观的一致性
   - 三视图之间必须完全匹配
   - 表情图片中的角色外观必须与三视图一致

2. **背景设置**：
   - 统一使用白色或透明背景，便于后续处理

3. **风格统一**：
   - 确保所有图片使用相同的艺术风格
   - 在 prompt 中明确指定风格类型

4. **质量要求**：
   - 要求高分辨率、清晰的图片
   - 适合用于动画制作

5. **角色描述优化**：
   - 提供详细的外观描述
   - 包含服装、配饰等细节
   - 明确年龄、性别等基本信息

## 快速参考

### 最小化 Prompt（仅角色描述）

如果 nano banana 支持上下文记忆，可以使用简化版本：

**三视图：**
```
Front view: {character_description}, white background
Side view: {character_description}, white background, match front view
Back view: {character_description}, white background, match front and side views
```

**表情：**
```
{character_description}, {expression_name} expression, white background, match character design
```

### 完整 Prompt（推荐）

使用本文档提供的完整 prompt 模板，确保生成高质量的、一致的图片。

