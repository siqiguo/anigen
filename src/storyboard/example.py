"""
分镜生成模块使用示例

演示如何使用分镜生成器从剧本生成分镜脚本，并优先使用资源库中的资源。
"""

from src.assets import AssetManager
from src.storyboard import StoryboardGenerator


def example_generate_storyboard():
    """示例：从剧本生成分镜脚本"""
    
    # 1. 初始化资源管理器
    asset_manager = AssetManager(base_dir="./assets")
    
    # 2. 先添加一些资源到资源库（可选，如果资源库已有资源可跳过）
    print("=== 添加资源到资源库 ===")
    character = asset_manager.add_character(
        name="主角小明",
        description="勇敢的年轻冒险者，总是充满好奇心",
        appearance="年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装",
        personality="勇敢、乐观、善良",
        style="卡通",
        tags=["主角", "冒险者"]
    )
    print(f"添加角色: {character.name}")
    
    scene = asset_manager.add_scene(
        name="神秘森林",
        description="充满神秘气息的古老森林，阳光透过树叶洒下斑驳的光影",
        location_type="室外",
        time_of_day="白天",
        weather="晴朗",
        mood="神秘",
        style="写实",
        tags=["自然", "森林", "神秘"]
    )
    print(f"添加场景: {scene.name}")
    
    # 3. 创建分镜生成器
    generator = StoryboardGenerator(
        asset_manager=asset_manager,
        default_shot_duration=3.0
    )
    
    # 4. 准备剧本数据
    script_data = {
        "title": "冒险开始",
        "scenes": [
            {
                "scene_number": 1,
                "location": "神秘森林",
                "time": "白天",
                "characters": ["主角小明"],
                "dialogue": [
                    {
                        "character": "主角小明",
                        "text": "这里是什么地方？看起来好神秘。",
                        "emotion": "惊讶"
                    },
                    {
                        "character": "主角小明",
                        "text": "我要小心探索。",
                        "emotion": "谨慎"
                    }
                ],
                "action": "主角环顾四周，小心翼翼地前进",
                "notes": "神秘、紧张"
            },
            {
                "scene_number": 2,
                "location": "森林深处",
                "time": "白天",
                "characters": ["主角小明"],
                "dialogue": [
                    {
                        "character": "主角小明",
                        "text": "前面好像有什么东西在发光！",
                        "emotion": "兴奋"
                    }
                ],
                "action": "主角快速向前跑去",
                "notes": "神秘、兴奋"
            }
        ],
        "characters": {
            "主角小明": {
                "description": "勇敢的年轻冒险者",
                "appearance": "年轻男性，黑色短发"
            }
        }
    }
    
    # 5. 生成分镜脚本（优先使用资源库资源）
    print("\n=== 生成分镜脚本（优先使用资源库资源） ===")
    storyboard = generator.generate_from_script(
        script_data,
        prefer_existing_resources=True
    )
    
    print(f"\n分镜标题: {storyboard.title}")
    print(f"总镜头数: {storyboard.total_shots}")
    print(f"总时长: {storyboard.total_duration:.1f}秒")
    
    # 6. 查看生成的分镜详情
    print("\n=== 分镜详情 ===")
    for shot in storyboard.shots:
        print(f"\n镜头 {shot.shot_number} (场景 {shot.scene_number}):")
        print(f"  类型: {shot.shot_type.value}")
        print(f"  时长: {shot.duration}秒")
        print(f"  描述: {shot.description}")
        print(f"  角色: {', '.join(shot.characters)}")
        if shot.dialogue:
            print(f"  对话: {shot.dialogue}")
        
        # 显示资源引用
        if shot.scene_resource:
            print(f"  ✓ 使用场景资源: {shot.scene_resource.resource_name}")
            print(f"    匹配度: {shot.scene_resource.match_score:.2f}")
            print(f"    匹配原因: {shot.scene_resource.match_reason}")
        
        if shot.character_resources:
            for char_ref in shot.character_resources:
                print(f"  ✓ 使用角色资源: {char_ref.resource_name}")
                print(f"    匹配度: {char_ref.match_score:.2f}")
                print(f"    匹配原因: {char_ref.match_reason}")
        
        if not shot.scene_resource and not shot.character_resources:
            print(f"  ⚠ 未匹配到资源库资源，将使用原始描述生成")
    
    # 7. 导出为JSON格式
    print("\n=== 导出分镜脚本 ===")
    storyboard_dict = storyboard.to_dict()
    print(f"分镜脚本已转换为字典格式，包含 {len(storyboard_dict['storyboard'])} 个镜头")
    
    # 可以保存到文件
    import json
    with open("storyboard_output.json", "w", encoding="utf-8") as f:
        json.dump(storyboard_dict, f, ensure_ascii=False, indent=2)
    print("分镜脚本已保存到 storyboard_output.json")
    
    return storyboard


def example_without_resources():
    """示例：不使用资源库资源生成分镜"""
    
    asset_manager = AssetManager(base_dir="./assets")
    generator = StoryboardGenerator(asset_manager)
    
    script_data = {
        "title": "简单场景",
        "scenes": [
            {
                "scene_number": 1,
                "location": "未知地点",
                "time": "夜晚",
                "characters": ["新角色"],
                "dialogue": [
                    {
                        "character": "新角色",
                        "text": "这是一个新角色，资源库中没有。",
                        "emotion": "平静"
                    }
                ],
                "action": "角色站立",
                "notes": ""
            }
        ],
        "characters": {
            "新角色": {
                "description": "一个全新的角色",
                "appearance": "未知外观"
            }
        }
    }
    
    print("\n=== 不使用资源库资源生成分镜 ===")
    storyboard = generator.generate_from_script(
        script_data,
        prefer_existing_resources=False
    )
    
    for shot in storyboard.shots:
        print(f"\n镜头 {shot.shot_number}: {shot.description}")
        if shot.scene_resource or shot.character_resources:
            print("  (使用了资源库资源)")
        else:
            print("  (未使用资源库资源，将使用原始描述)")


def main():
    """主函数"""
    print("=== 分镜生成模块使用示例 ===\n")
    
    # 示例1: 使用资源库资源生成分镜
    storyboard = example_generate_storyboard()
    
    # 示例2: 不使用资源库资源
    example_without_resources()
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()

