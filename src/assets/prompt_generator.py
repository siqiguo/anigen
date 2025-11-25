"""
Nano Banana Prompt 生成器

根据角色描述自动生成用于 Nano Banana AI 图像生成的 prompt。
"""

from typing import Dict, List, Optional
from .models import Character


class NanoBananaPromptGenerator:
    """Nano Banana Prompt 生成器
    
    根据角色对象生成用于图像生成的 prompt。
    """
    
    # 标准表情列表
    STANDARD_EXPRESSIONS = [
        "happy",
        "sad",
        "angry",
        "surprised",
        "neutral",
        "scared",
        "excited",
        "confused",
    ]
    
    # 表情描述映射
    EXPRESSION_DESCRIPTIONS = {
        "happy": "happy, joyful, smiling expression. Eyes should be bright and cheerful, mouth showing a genuine smile",
        "sad": "sad, melancholic expression. Eyes should look downcast or teary, mouth slightly downturned",
        "angry": "angry, furious expression. Eyebrows furrowed, eyes narrowed or glaring, mouth showing anger",
        "surprised": "surprised, shocked expression. Eyes wide open, eyebrows raised, mouth open in an 'O' shape",
        "neutral": "neutral, calm, expressionless expression. Eyes looking straight ahead, relaxed facial features, mouth in a neutral position",
        "scared": "scared, frightened expression. Eyes wide with fear, eyebrows raised, mouth slightly open",
        "excited": "excited, enthusiastic expression. Eyes bright and wide, eyebrows raised, mouth open in a big smile or cheer",
        "confused": "confused, puzzled expression. Eyes looking slightly off to the side, one eyebrow raised, mouth slightly open",
    }
    
    def __init__(self, style: Optional[str] = None):
        """初始化 prompt 生成器
        
        Args:
            style: 默认风格（如：anime, cartoon, realistic），如果角色对象中没有指定则使用此值
        """
        self.default_style = style or "anime"
    
    def build_character_description(self, character: Character) -> str:
        """构建完整的角色描述字符串
        
        Args:
            character: 角色对象
            
        Returns:
            完整的角色描述字符串
        """
        parts = []
        
        # 基本信息
        if character.appearance:
            parts.append(character.appearance)
        
        if character.age:
            parts.append(f"{character.age} years old")
        
        if character.gender:
            parts.append(character.gender)
        
        # 风格
        style = character.style or self.default_style
        if style:
            parts.append(f"{style} style")
        
        return ", ".join(parts)
    
    def generate_front_view_prompt(self, character: Character) -> str:
        """生成前视图 prompt
        
        Args:
            character: 角色对象
            
        Returns:
            前视图 prompt 文本
        """
        description = self.build_character_description(character)
        style = character.style or self.default_style
        
        return f"""Create a front view character design sheet illustration of: {description}

Requirements:
- Full body front view, character facing forward
- White or transparent background
- Consistent character design with detailed appearance
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    def generate_side_view_prompt(self, character: Character) -> str:
        """生成侧视图 prompt
        
        Args:
            character: 角色对象
            
        Returns:
            侧视图 prompt 文本
        """
        description = self.build_character_description(character)
        style = character.style or self.default_style
        
        return f"""Create a side view character design sheet illustration of: {description}

Requirements:
- Full body side view (profile), character facing left or right
- White or transparent background
- Must match the front view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    def generate_back_view_prompt(self, character: Character) -> str:
        """生成后视图 prompt
        
        Args:
            character: 角色对象
            
        Returns:
            后视图 prompt 文本
        """
        description = self.build_character_description(character)
        style = character.style or self.default_style
        
        return f"""Create a back view character design sheet illustration of: {description}

Requirements:
- Full body back view, character facing away
- White or transparent background
- Must match the front and side view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: {style}"""
    
    def generate_expression_prompt(
        self, 
        character: Character, 
        expression_name: str
    ) -> str:
        """生成表情 prompt
        
        Args:
            character: 角色对象
            expression_name: 表情名称（如：happy, sad, angry等）
            
        Returns:
            表情 prompt 文本
        """
        description = self.build_character_description(character)
        style = character.style or self.default_style
        
        if expression_name not in self.EXPRESSION_DESCRIPTIONS:
            raise ValueError(
                f"Unknown expression: {expression_name}. "
                f"Available expressions: {', '.join(self.EXPRESSION_DESCRIPTIONS.keys())}"
            )
        
        expression_desc = self.EXPRESSION_DESCRIPTIONS[expression_name]
        
        return f"""Create a character portrait of: {description}

Requirements:
- Character showing a {expression_desc}
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- Facial expression should be clear and expressive
- High quality, clean line art or rendered illustration
- Style: {style}"""
    
    def generate_all_prompts(
        self, 
        character: Character,
        expressions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """生成角色的所有 prompt
        
        Args:
            character: 角色对象
            expressions: 要生成的表情列表，如果为None则使用标准表情列表
            
        Returns:
            包含所有 prompt 的字典，key 为图片类型，value 为 prompt 文本
            key 格式：
            - "front_view": 前视图
            - "side_view": 侧视图
            - "back_view": 后视图
            - "expression_{name}": 表情（如 "expression_happy"）
        """
        prompts = {}
        
        # 三视图
        prompts["front_view"] = self.generate_front_view_prompt(character)
        prompts["side_view"] = self.generate_side_view_prompt(character)
        prompts["back_view"] = self.generate_back_view_prompt(character)
        
        # 表情
        expression_list = expressions or self.STANDARD_EXPRESSIONS
        for expr_name in expression_list:
            try:
                prompts[f"expression_{expr_name}"] = self.generate_expression_prompt(
                    character, expr_name
                )
            except ValueError:
                # 跳过不支持的表情
                continue
        
        return prompts
    
    def generate_compact_prompt(
        self,
        character: Character,
        view_type: str,
        expression_name: Optional[str] = None
    ) -> str:
        """生成简化版 prompt（适合支持上下文记忆的 API）
        
        Args:
            character: 角色对象
            view_type: 视图类型（"front", "side", "back", "expression"）
            expression_name: 表情名称（仅在 view_type 为 "expression" 时需要）
            
        Returns:
            简化的 prompt 文本
        """
        description = self.build_character_description(character)
        style = character.style or self.default_style
        
        if view_type == "front":
            return f"{description}, front view, full body, white background, {style} style"
        elif view_type == "side":
            return f"{description}, side view, full body, white background, match front view, {style} style"
        elif view_type == "back":
            return f"{description}, back view, full body, white background, match front and side views, {style} style"
        elif view_type == "expression":
            if not expression_name:
                raise ValueError("expression_name is required when view_type is 'expression'")
            if expression_name not in self.EXPRESSION_DESCRIPTIONS:
                raise ValueError(f"Unknown expression: {expression_name}")
            return f"{description}, {expression_name} expression, portrait, white background, match character design, {style} style"
        else:
            raise ValueError(
                f"Unknown view_type: {view_type}. "
                f"Available types: front, side, back, expression"
            )


def generate_character_prompts(
    character: Character,
    expressions: Optional[List[str]] = None,
    compact: bool = False
) -> Dict[str, str]:
    """便捷函数：生成角色的所有 prompt
    
    Args:
        character: 角色对象
        expressions: 要生成的表情列表，如果为None则使用标准表情列表
        compact: 是否使用简化版 prompt
        
    Returns:
        包含所有 prompt 的字典
    """
    generator = NanoBananaPromptGenerator()
    
    if compact:
        prompts = {}
        prompts["front_view"] = generator.generate_compact_prompt(character, "front")
        prompts["side_view"] = generator.generate_compact_prompt(character, "side")
        prompts["back_view"] = generator.generate_compact_prompt(character, "back")
        
        expression_list = expressions or generator.STANDARD_EXPRESSIONS
        for expr_name in expression_list:
            try:
                prompts[f"expression_{expr_name}"] = generator.generate_compact_prompt(
                    character, "expression", expr_name
                )
            except ValueError:
                continue
        
        return prompts
    else:
        return generator.generate_all_prompts(character, expressions)

