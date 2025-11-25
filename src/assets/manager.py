"""
资源管理器

提供资源的增删改查、搜索匹配等核心功能。
"""

from typing import List, Optional, Dict, Any
from pathlib import Path

from .models import (
    Asset,
    Character,
    Prop,
    Scene,
    Action,
    ResourceType,
)
from .storage import AssetStorage


class AssetManager:
    """资源管理器
    
    提供资源的完整管理功能，包括添加、删除、更新、查询、搜索等。
    """
    
    def __init__(self, storage: Optional[AssetStorage] = None, base_dir: str = "./assets"):
        """初始化资源管理器
        
        Args:
            storage: 资源存储对象，如果为None则创建新的
            base_dir: 资源库根目录路径
        """
        self.storage = storage or AssetStorage(base_dir)
    
    def add_character(
        self,
        name: str,
        description: str = "",
        appearance: str = "",
        personality: str = "",
        age: Optional[int] = None,
        gender: Optional[str] = None,
        style: str = "",
        tags: Optional[List[str]] = None,
        image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Character:
        """添加角色资源
        
        Args:
            name: 角色名称
            description: 角色描述
            appearance: 外观描述
            personality: 性格描述
            age: 年龄
            gender: 性别
            style: 风格
            tags: 标签列表
            image_path: 图片路径
            metadata: 额外元数据
            
        Returns:
            创建的角色对象
        """
        character = Character(
            name=name,
            description=description,
            appearance=appearance,
            personality=personality,
            age=age,
            gender=gender,
            style=style,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        if image_path:
            character.image_path = self.storage.save_image(
                image_path, character.id, ResourceType.CHARACTER
            )
        
        self.storage.add_to_index(character)
        return character
    
    def add_prop(
        self,
        name: str,
        description: str = "",
        category: str = "",
        size: Optional[str] = None,
        material: Optional[str] = None,
        style: str = "",
        tags: Optional[List[str]] = None,
        image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Prop:
        """添加道具资源
        
        Args:
            name: 道具名称
            description: 道具描述
            category: 道具类别
            size: 尺寸描述
            material: 材质
            style: 风格
            tags: 标签列表
            image_path: 图片路径
            metadata: 额外元数据
            
        Returns:
            创建的道具对象
        """
        prop = Prop(
            name=name,
            description=description,
            category=category,
            size=size,
            material=material,
            style=style,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        if image_path:
            prop.image_path = self.storage.save_image(
                image_path, prop.id, ResourceType.PROP
            )
        
        self.storage.add_to_index(prop)
        return prop
    
    def add_scene(
        self,
        name: str,
        description: str = "",
        location_type: str = "",
        time_of_day: Optional[str] = None,
        weather: Optional[str] = None,
        mood: str = "",
        style: str = "",
        tags: Optional[List[str]] = None,
        image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Scene:
        """添加场景资源
        
        Args:
            name: 场景名称
            description: 场景描述
            location_type: 场景类型
            time_of_day: 时间
            weather: 天气
            mood: 氛围
            style: 风格
            tags: 标签列表
            image_path: 图片路径
            metadata: 额外元数据
            
        Returns:
            创建的场景对象
        """
        scene = Scene(
            name=name,
            description=description,
            location_type=location_type,
            time_of_day=time_of_day,
            weather=weather,
            mood=mood,
            style=style,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        if image_path:
            scene.image_path = self.storage.save_image(
                image_path, scene.id, ResourceType.SCENE
            )
        
        self.storage.add_to_index(scene)
        return scene
    
    def add_action(
        self,
        name: str,
        description: str = "",
        action_type: str = "",
        duration: Optional[float] = None,
        intensity: Optional[str] = None,
        target: Optional[str] = None,
        style: str = "",
        tags: Optional[List[str]] = None,
        image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Action:
        """添加动作资源
        
        Args:
            name: 动作名称
            description: 动作描述
            action_type: 动作类型
            duration: 动作时长
            intensity: 强度
            target: 目标对象
            style: 风格
            tags: 标签列表
            image_path: 图片路径
            metadata: 额外元数据
            
        Returns:
            创建的动作对象
        """
        action = Action(
            name=name,
            description=description,
            action_type=action_type,
            duration=duration,
            intensity=intensity,
            target=target,
            style=style,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        if image_path:
            action.image_path = self.storage.save_image(
                image_path, action.id, ResourceType.ACTION
            )
        
        self.storage.add_to_index(action)
        return action
    
    def get_resource(self, resource_id: str) -> Optional[Asset]:
        """根据ID获取资源
        
        Args:
            resource_id: 资源ID
            
        Returns:
            资源对象，如果不存在返回None
        """
        data = self.storage.get_from_index(resource_id)
        if not data:
            return None
        
        return self._dict_to_asset(data)
    
    def update_resource(self, resource: Asset) -> Asset:
        """更新资源
        
        Args:
            resource: 资源对象
            
        Returns:
            更新后的资源对象
        """
        self.storage.update_index(resource)
        return resource
    
    def delete_resource(self, resource_id: str) -> bool:
        """删除资源
        
        Args:
            resource_id: 资源ID
            
        Returns:
            是否删除成功
        """
        resource = self.get_resource(resource_id)
        if not resource:
            return False
        
        # 删除图片文件
        if resource.image_path:
            self.storage.delete_image(resource.image_path)
        
        # 从索引中移除
        self.storage.remove_from_index(resource_id)
        return True
    
    def list_resources(self, resource_type: Optional[ResourceType] = None) -> List[Asset]:
        """列出所有资源
        
        Args:
            resource_type: 可选的资源类型过滤
            
        Returns:
            资源对象列表
        """
        resources_data = self.storage.list_resources(resource_type)
        return [self._dict_to_asset(data) for data in resources_data]
    
    def search_resources(
        self,
        keyword: Optional[str] = None,
        tags: Optional[List[str]] = None,
        resource_type: Optional[ResourceType] = None
    ) -> List[Asset]:
        """搜索资源
        
        Args:
            keyword: 关键词（搜索名称和描述）
            tags: 标签列表
            resource_type: 资源类型过滤
            
        Returns:
            匹配的资源对象列表
        """
        results_data = self.storage.search_resources(keyword, tags, resource_type)
        return [self._dict_to_asset(data) for data in results_data]
    
    def find_matching_character(
        self,
        name: Optional[str] = None,
        style: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Character]:
        """查找匹配的角色
        
        Args:
            name: 角色名称（模糊匹配）
            style: 风格
            tags: 标签列表
            
        Returns:
            匹配的角色对象，如果未找到返回None
        """
        results = self.search_resources(
            keyword=name,
            tags=tags,
            resource_type=ResourceType.CHARACTER
        )
        
        characters = [r for r in results if isinstance(r, Character)]
        
        # 风格过滤
        if style:
            characters = [c for c in characters if c.style == style]
        
        return characters[0] if characters else None
    
    def find_matching_scene(
        self,
        location_type: Optional[str] = None,
        mood: Optional[str] = None,
        style: Optional[str] = None
    ) -> Optional[Scene]:
        """查找匹配的场景
        
        Args:
            location_type: 场景类型
            mood: 氛围
            style: 风格
            
        Returns:
            匹配的场景对象，如果未找到返回None
        """
        results = self.search_resources(resource_type=ResourceType.SCENE)
        scenes = [r for r in results if isinstance(r, Scene)]
        
        # 应用过滤条件
        if location_type:
            scenes = [s for s in scenes if s.location_type == location_type]
        if mood:
            scenes = [s for s in scenes if s.mood == mood]
        if style:
            scenes = [s for s in scenes if s.style == style]
        
        return scenes[0] if scenes else None
    
    def _dict_to_asset(self, data: Dict[str, Any]) -> Asset:
        """将字典转换为资源对象
        
        Args:
            data: 资源字典数据
            
        Returns:
            资源对象
        """
        resource_type = ResourceType(data["resource_type"])
        
        if resource_type == ResourceType.CHARACTER:
            return Character.from_dict(data)
        elif resource_type == ResourceType.PROP:
            return Prop.from_dict(data)
        elif resource_type == ResourceType.SCENE:
            return Scene.from_dict(data)
        elif resource_type == ResourceType.ACTION:
            return Action.from_dict(data)
        else:
            return Asset.from_dict(data)

