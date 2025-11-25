#!/usr/bin/env python3
"""
测试随机角色生成功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from server.character_generator import RandomCharacterGenerator
from src.assets.prompt_generator import NanoBananaPromptGenerator
from src.assets.models import Character
import json

def test_random_character():
    """测试随机角色生成"""
    print("=" * 60)
    print("测试随机角色生成功能")
    print("=" * 60)
    
    # 创建生成器
    char_gen = RandomCharacterGenerator()
    prompt_gen = NanoBananaPromptGenerator()
    
    # 生成随机角色
    print("\n1. 生成随机角色数据...")
    random_data = char_gen.generate_random_character()
    print(json.dumps(random_data, indent=2, ensure_ascii=False))
    
    # 创建角色对象
    print("\n2. 创建角色对象...")
    character = Character(
        name=random_data["name"],
        description=random_data["description"],
        appearance=random_data["appearance"],
        personality=random_data["personality"],
        age=random_data["age"],
        gender=random_data["gender"],
        style=random_data["style"],
        tags=random_data["tags"],
    )
    print(f"角色ID: {character.id}")
    print(f"角色名称: {character.name}")
    
    # 生成 prompt
    print("\n3. 生成 Prompt...")
    prompts = prompt_gen.generate_all_prompts(character)
    print(f"生成了 {len(prompts)} 个 prompt:")
    print(f"  - 三视图: 3个")
    print(f"  - 表情: {len(prompts) - 3}个")
    
    # 显示前视图 prompt 的前100个字符
    if "front_view" in prompts:
        front_prompt = prompts["front_view"]
        print(f"\n前视图 Prompt 预览（前200字符）:")
        print(front_prompt[:200] + "...")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_random_character()

