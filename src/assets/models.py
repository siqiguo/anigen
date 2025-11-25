"""
资源数据模型

定义资源库中各种资源的数据结构。
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class ResourceType(str, Enum):
    """资源类型枚举"""
    CHARACTER = "character"  # 角色
    PROP = "prop"  # 道具
    SCENE = "scene"  # 场景
    ACTION = "action"  # 动作


@dataclass
class Asset:
    """资源基类
    
    所有资源类型的基类，包含通用的资源属性。
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""  # 资源名称
    resource_type: ResourceType = ResourceType.CHARACTER
    description: str = ""  # 详细描述
    tags: List[str] = field(default_factory=list)  # 标签列表
    image_path: Optional[str] = None  # 图片文件路径
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "resource_type": self.resource_type.value,
            "description": self.description,
            "tags": self.tags,
            "image_path": self.image_path,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Asset":
        """从字典创建资源对象"""
        data = data.copy()
        data["resource_type"] = ResourceType(data["resource_type"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)


@dataclass
class Character(Asset):
    """角色资源
    
    用于动画中的角色资源，包含角色的外观、特征、三视图和表情等信息。
    """
    appearance: str = ""  # 外观描述
    personality: str = ""  # 性格描述
    age: Optional[int] = None  # 年龄
    gender: Optional[str] = None  # 性别
    style: str = ""  # 风格（如：卡通、写实、二次元等）
    # 三视图
    front_view: Optional[str] = None  # 前视图图片路径
    side_view: Optional[str] = None  # 侧视图图片路径
    back_view: Optional[str] = None  # 后视图图片路径
    # 表情字典，key为表情名称，value为图片路径
    expressions: Dict[str, str] = field(default_factory=dict)  # 表情图片路径字典
    
    def __post_init__(self):
        """初始化后处理"""
        self.resource_type = ResourceType.CHARACTER
    
    def add_expression(self, expression_name: str, image_path: str) -> None:
        """添加表情
        
        Args:
            expression_name: 表情名称（如：happy, sad, angry, surprised等）
            image_path: 表情图片路径
        """
        self.expressions[expression_name] = image_path
        self.updated_at = datetime.now()
    
    def remove_expression(self, expression_name: str) -> bool:
        """移除表情
        
        Args:
            expression_name: 表情名称
            
        Returns:
            是否成功移除
        """
        if expression_name in self.expressions:
            del self.expressions[expression_name]
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_expression(self, expression_name: str) -> Optional[str]:
        """获取表情图片路径
        
        Args:
            expression_name: 表情名称
            
        Returns:
            表情图片路径，如果不存在返回None
        """
        return self.expressions.get(expression_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        base_dict = super().to_dict()
        base_dict.update({
            "appearance": self.appearance,
            "personality": self.personality,
            "age": self.age,
            "gender": self.gender,
            "style": self.style,
            "front_view": self.front_view,
            "side_view": self.side_view,
            "back_view": self.back_view,
            "expressions": self.expressions,
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        """从字典创建角色对象"""
        asset_data = {k: v for k, v in data.items() 
                     if k not in ["appearance", "personality", "age", "gender", "style",
                                 "front_view", "side_view", "back_view", "expressions"]}
        asset = Asset.from_dict(asset_data)
        return cls(
            id=asset.id,
            name=asset.name,
            resource_type=asset.resource_type,
            description=asset.description,
            tags=asset.tags,
            image_path=asset.image_path,
            metadata=asset.metadata,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            appearance=data.get("appearance", ""),
            personality=data.get("personality", ""),
            age=data.get("age"),
            gender=data.get("gender"),
            style=data.get("style", ""),
            front_view=data.get("front_view"),
            side_view=data.get("side_view"),
            back_view=data.get("back_view"),
            expressions=data.get("expressions", {}),
        )


@dataclass
class Prop(Asset):
    """道具资源
    
    用于动画中的道具资源，如物品、工具等。
    """
    category: str = ""  # 道具类别（如：武器、家具、工具等）
    size: Optional[str] = None  # 尺寸描述
    material: Optional[str] = None  # 材质
    style: str = ""  # 风格
    
    def __post_init__(self):
        """初始化后处理"""
        self.resource_type = ResourceType.PROP
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        base_dict = super().to_dict()
        base_dict.update({
            "category": self.category,
            "size": self.size,
            "material": self.material,
            "style": self.style,
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prop":
        """从字典创建道具对象"""
        asset_data = {k: v for k, v in data.items() 
                     if k not in ["category", "size", "material", "style"]}
        asset = Asset.from_dict(asset_data)
        return cls(
            id=asset.id,
            name=asset.name,
            resource_type=asset.resource_type,
            description=asset.description,
            tags=asset.tags,
            image_path=asset.image_path,
            metadata=asset.metadata,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            category=data.get("category", ""),
            size=data.get("size"),
            material=data.get("material"),
            style=data.get("style", ""),
        )


@dataclass
class Scene(Asset):
    """场景资源
    
    用于动画中的场景资源，如地点、环境等。
    """
    location_type: str = ""  # 场景类型（如：室内、室外、城市、自然等）
    time_of_day: Optional[str] = None  # 时间（如：白天、夜晚、黄昏等）
    weather: Optional[str] = None  # 天气
    mood: str = ""  # 氛围（如：温馨、紧张、神秘等）
    style: str = ""  # 风格
    
    def __post_init__(self):
        """初始化后处理"""
        self.resource_type = ResourceType.SCENE
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        base_dict = super().to_dict()
        base_dict.update({
            "location_type": self.location_type,
            "time_of_day": self.time_of_day,
            "weather": self.weather,
            "mood": self.mood,
            "style": self.style,
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scene":
        """从字典创建场景对象"""
        asset_data = {k: v for k, v in data.items() 
                     if k not in ["location_type", "time_of_day", "weather", "mood", "style"]}
        asset = Asset.from_dict(asset_data)
        return cls(
            id=asset.id,
            name=asset.name,
            resource_type=asset.resource_type,
            description=asset.description,
            tags=asset.tags,
            image_path=asset.image_path,
            metadata=asset.metadata,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            location_type=data.get("location_type", ""),
            time_of_day=data.get("time_of_day"),
            weather=data.get("weather"),
            mood=data.get("mood", ""),
            style=data.get("style", ""),
        )


@dataclass
class Action(Asset):
    """动作资源
    
    用于动画中的动作资源，如角色动作、动画序列等。
    """
    action_type: str = ""  # 动作类型（如：走路、跑步、挥手、表情等）
    duration: Optional[float] = None  # 动作时长（秒）
    intensity: Optional[str] = None  # 强度（如：轻微、中等、强烈）
    target: Optional[str] = None  # 目标对象（如：全身、手部、面部等）
    style: str = ""  # 风格
    
    def __post_init__(self):
        """初始化后处理"""
        self.resource_type = ResourceType.ACTION
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        base_dict = super().to_dict()
        base_dict.update({
            "action_type": self.action_type,
            "duration": self.duration,
            "intensity": self.intensity,
            "target": self.target,
            "style": self.style,
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        """从字典创建动作对象"""
        asset_data = {k: v for k, v in data.items() 
                     if k not in ["action_type", "duration", "intensity", "target", "style"]}
        asset = Asset.from_dict(asset_data)
        return cls(
            id=asset.id,
            name=asset.name,
            resource_type=asset.resource_type,
            description=asset.description,
            tags=asset.tags,
            image_path=asset.image_path,
            metadata=asset.metadata,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            action_type=data.get("action_type", ""),
            duration=data.get("duration"),
            intensity=data.get("intensity"),
            target=data.get("target"),
            style=data.get("style", ""),
        )

