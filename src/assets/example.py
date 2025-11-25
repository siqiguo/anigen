"""
资源库模块使用示例

演示如何使用资源库模块进行资源的增删改查操作。
"""

from src.assets import AssetManager, ResourceType


def example_add_resources():
    """示例：添加各种资源"""
    # 创建资源管理器
    manager = AssetManager(base_dir="./assets")
    
    # 添加角色（包含三视图和表情）
    character = manager.add_character(
        name="主角小明",
        description="勇敢的年轻冒险者，总是充满好奇心",
        appearance="年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装",
        personality="勇敢、乐观、善良",
        age=25,
        gender="男",
        style="卡通",
        tags=["主角", "冒险者", "男性"],
        # 三视图
        # front_view="./example_images/character_front.jpg",
        # side_view="./example_images/character_side.jpg",
        # back_view="./example_images/character_back.jpg",
        # 表情
        # expressions={
        #     "happy": "./example_images/character_happy.jpg",
        #     "sad": "./example_images/character_sad.jpg",
        #     "angry": "./example_images/character_angry.jpg",
        #     "surprised": "./example_images/character_surprised.jpg",
        # }
    )
    print(f"添加角色: {character.name} (ID: {character.id})")
    if character.front_view:
        print(f"  前视图: {character.front_view}")
    if character.side_view:
        print(f"  侧视图: {character.side_view}")
    if character.back_view:
        print(f"  后视图: {character.back_view}")
    if character.expressions:
        print(f"  表情: {list(character.expressions.keys())}")
    
    # 添加场景
    scene = manager.add_scene(
        name="神秘森林",
        description="充满神秘气息的古老森林，阳光透过树叶洒下斑驳的光影",
        location_type="室外",
        time_of_day="白天",
        weather="晴朗",
        mood="神秘",
        style="写实",
        tags=["自然", "森林", "神秘"],
        # image_path="./example_images/forest.jpg"
    )
    print(f"添加场景: {scene.name} (ID: {scene.id})")
    
    # 添加道具
    prop = manager.add_prop(
        name="魔法剑",
        description="一把闪烁着蓝色光芒的魔法剑，剑身上刻有古老的符文",
        category="武器",
        size="中等",
        material="魔法金属",
        style="奇幻",
        tags=["武器", "魔法", "剑"],
        # image_path="./example_images/sword.jpg"
    )
    print(f"添加道具: {prop.name} (ID: {prop.id})")
    
    # 添加动作
    action = manager.add_action(
        name="走路",
        description="角色正常走路的动作",
        action_type="移动",
        duration=2.0,
        intensity="中等",
        target="全身",
        style="卡通",
        tags=["移动", "基础动作", "走路"],
        # image_path="./example_images/walk.jpg"
    )
    print(f"添加动作: {action.name} (ID: {action.id})")
    
    return manager


def example_search_resources(manager: AssetManager):
    """示例：搜索资源"""
    print("\n=== 搜索资源示例 ===")
    
    # 按关键词搜索
    results = manager.search_resources(keyword="主角")
    print(f"关键词'主角'搜索结果: {len(results)}个")
    for resource in results:
        print(f"  - {resource.name} ({resource.resource_type.value})")
    
    # 按类型搜索
    characters = manager.list_resources(ResourceType.CHARACTER)
    print(f"\n所有角色资源: {len(characters)}个")
    for char in characters:
        print(f"  - {char.name}: {char.description[:30]}...")
    
    # 按标签搜索
    results = manager.search_resources(tags=["自然"])
    print(f"\n标签'自然'搜索结果: {len(results)}个")
    for resource in results:
        print(f"  - {resource.name}")


def example_find_matching(manager: AssetManager):
    """示例：查找匹配的资源"""
    print("\n=== 查找匹配资源示例 ===")
    
    # 查找匹配的角色
    character = manager.find_matching_character(
        name="主角",
        style="卡通"
    )
    if character:
        print(f"找到匹配角色: {character.name}")
        print(f"  外观: {character.appearance}")
        print(f"  性格: {character.personality}")
    
    # 查找匹配的场景
    scene = manager.find_matching_scene(
        location_type="室外",
        mood="神秘"
    )
    if scene:
        print(f"\n找到匹配场景: {scene.name}")
        print(f"  类型: {scene.location_type}")
        print(f"  氛围: {scene.mood}")


def example_update_delete(manager: AssetManager):
    """示例：更新和删除资源"""
    print("\n=== 更新和删除资源示例 ===")
    
    # 获取资源
    resources = manager.list_resources()
    if resources:
        resource = resources[0]
        print(f"原始资源: {resource.name}")
        print(f"  描述: {resource.description}")
        
        # 更新资源
        resource.description = "更新后的描述信息"
        manager.update_resource(resource)
        print(f"\n更新后的资源: {resource.name}")
        print(f"  描述: {resource.description}")
        
        # 删除资源（注释掉，避免删除示例数据）
        # manager.delete_resource(resource.id)
        # print(f"\n已删除资源: {resource.name}")


def main():
    """主函数"""
    print("=== 资源库模块使用示例 ===\n")
    
    # 添加资源
    manager = example_add_resources()
    
    # 搜索资源
    example_search_resources(manager)
    
    # 查找匹配资源
    example_find_matching(manager)
    
    # 更新和删除资源
    example_update_delete(manager)
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()

