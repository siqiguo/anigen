"""
Nano Banana Prompt 生成器使用示例

演示如何使用 prompt 生成器为角色生成所有图片的 prompt。
"""

from src.assets import AssetManager
from src.assets.prompt_generator import (
    NanoBananaPromptGenerator,
    generate_character_prompts
)


def example_generate_prompts():
    """示例：为角色生成所有 prompt"""
    print("=== Nano Banana Prompt 生成示例 ===\n")
    
    # 创建资源管理器
    manager = AssetManager(base_dir="./assets")
    
    # 创建一个角色（不包含图片）
    character = manager.add_character(
        name="主角小明",
        description="勇敢的年轻冒险者，总是充满好奇心",
        appearance="年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装，棕色皮靴，腰间挂着剑",
        personality="勇敢、乐观、善良",
        age=25,
        gender="男",
        style="卡通",
        tags=["主角", "冒险者", "男性"],
    )
    
    print(f"角色: {character.name}")
    print(f"描述: {character.appearance}\n")
    
    # 方法1：使用便捷函数生成所有 prompt
    print("--- 方法1：使用便捷函数 ---")
    prompts = generate_character_prompts(character)
    
    print(f"生成了 {len(prompts)} 个 prompt：")
    for key, prompt in prompts.items():
        print(f"\n[{key}]")
        print(prompt[:100] + "..." if len(prompt) > 100 else prompt)
    
    # 方法2：使用生成器类，更灵活
    print("\n\n--- 方法2：使用生成器类 ---")
    generator = NanoBananaPromptGenerator(style="卡通")
    
    # 生成三视图
    front_prompt = generator.generate_front_view_prompt(character)
    print("\n[前视图 Prompt]")
    print(front_prompt)
    
    # 生成特定表情
    happy_prompt = generator.generate_expression_prompt(character, "happy")
    print("\n[开心表情 Prompt]")
    print(happy_prompt)
    
    # 生成所有标准表情
    print("\n[所有标准表情]")
    for expr in generator.STANDARD_EXPRESSIONS:
        prompt = generator.generate_expression_prompt(character, expr)
        print(f"\n{expr}: {prompt[:80]}...")
    
    # 方法3：生成简化版 prompt（适合支持上下文记忆的 API）
    print("\n\n--- 方法3：简化版 Prompt ---")
    compact_prompts = generate_character_prompts(character, compact=True)
    
    print("简化版 prompt（适合支持上下文记忆的 API）：")
    for key, prompt in compact_prompts.items():
        print(f"\n[{key}]")
        print(prompt)
    
    return character, prompts


def example_custom_expressions():
    """示例：生成自定义表情列表的 prompt"""
    print("\n\n=== 自定义表情列表示例 ===\n")
    
    manager = AssetManager(base_dir="./assets")
    
    character = manager.add_character(
        name="神秘角色",
        appearance="年轻女性，银色长发，紫色眼睛，穿着魔法师袍",
        style="二次元",
    )
    
    # 只生成部分表情
    custom_expressions = ["happy", "sad", "angry", "surprised"]
    prompts = generate_character_prompts(character, expressions=custom_expressions)
    
    print(f"角色: {character.name}")
    print(f"生成的表情: {custom_expressions}")
    print(f"\n共生成 {len(prompts)} 个 prompt（3个视图 + {len(custom_expressions)}个表情）")
    
    return character, prompts


def example_prompt_format_for_api():
    """示例：格式化 prompt 用于 API 调用"""
    print("\n\n=== API 调用格式示例 ===\n")
    
    manager = AssetManager(base_dir="./assets")
    
    character = manager.add_character(
        name="测试角色",
        appearance="年轻男性，黑色短发，蓝色眼睛",
        style="anime",
    )
    
    generator = NanoBananaPromptGenerator()
    prompts = generator.generate_all_prompts(character)
    
    # 模拟 API 调用格式
    print("模拟 Nano Banana API 调用：\n")
    
    # 三视图
    print("1. 生成三视图：")
    for view_type in ["front_view", "side_view", "back_view"]:
        print(f"\n   {view_type}:")
        print(f"   POST /api/generate")
        print(f"   Body: {{'prompt': '{prompts[view_type][:50]}...'}}")
    
    # 表情
    print("\n2. 生成表情：")
    expression_prompts = {
        k: v for k, v in prompts.items() 
        if k.startswith("expression_")
    }
    for expr_key, prompt in expression_prompts.items():
        expr_name = expr_key.replace("expression_", "")
        print(f"\n   {expr_name}:")
        print(f"   POST /api/generate")
        print(f"   Body: {{'prompt': '{prompt[:50]}...'}}")
    
    return prompts


def example_integration_workflow():
    """示例：完整的集成工作流程"""
    print("\n\n=== 完整工作流程示例 ===\n")
    
    manager = AssetManager(base_dir="./assets")
    
    # 步骤1：创建角色（只有描述，没有图片）
    character = manager.add_character(
        name="新角色",
        description="一个全新的角色",
        appearance="年轻男性，黑色短发，蓝色眼睛，穿着现代服装",
        style="anime",
    )
    
    print(f"步骤1：创建角色 - {character.name} (ID: {character.id})")
    
    # 步骤2：生成所有 prompt
    generator = NanoBananaPromptGenerator()
    prompts = generator.generate_all_prompts(character)
    
    print(f"\n步骤2：生成 {len(prompts)} 个 prompt")
    print(f"  - 三视图: 3个")
    print(f"  - 表情: {len(prompts) - 3}个")
    
    # 步骤3：模拟调用 Nano Banana API 生成图片
    print("\n步骤3：调用 Nano Banana API 生成图片（模拟）")
    print("  注意：这里需要实际的 Nano Banana API 客户端")
    print("  示例代码：")
    print("""
    # 伪代码示例
    nano_banana = NanoBananaClient(api_key="your_api_key")
    
    # 生成三视图
    front_image = nano_banana.generate(prompts["front_view"])
    side_image = nano_banana.generate(prompts["side_view"])
    back_image = nano_banana.generate(prompts["back_view"])
    
    # 生成表情
    expressions = {}
    for key, prompt in prompts.items():
        if key.startswith("expression_"):
            expr_name = key.replace("expression_", "")
            expressions[expr_name] = nano_banana.generate(prompt)
    
    # 步骤4：保存图片到角色资源
    manager.update_character_views(
        character_id=character.id,
        front_view=front_image,
        side_view=side_image,
        back_view=back_image
    )
    
    for expr_name, image_path in expressions.items():
        manager.add_character_expression(
            character_id=character.id,
            expression_name=expr_name,
            expression_image_path=image_path
        )
    """)
    
    print("\n步骤4：图片已保存到角色资源")
    print(f"  角色现在包含：")
    print(f"  - 三视图: {bool(character.front_view)}")
    print(f"  - 表情数量: {len(character.expressions)}")


def main():
    """主函数"""
    # 基本使用示例
    character, prompts = example_generate_prompts()
    
    # 自定义表情示例
    example_custom_expressions()
    
    # API 调用格式示例
    example_prompt_format_for_api()
    
    # 完整工作流程示例
    example_integration_workflow()
    
    print("\n\n=== 示例完成 ===")
    print("\n提示：")
    print("1. 使用 generate_character_prompts() 快速生成所有 prompt")
    print("2. 使用 NanoBananaPromptGenerator 类进行更精细的控制")
    print("3. 使用 compact=True 生成简化版 prompt（适合支持上下文记忆的 API）")
    print("4. 将生成的 prompt 传递给 Nano Banana API 生成图片")
    print("5. 使用 AssetManager 保存生成的图片到角色资源")


if __name__ == "__main__":
    main()

