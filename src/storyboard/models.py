"""
分镜数据模型

定义分镜脚本的数据结构，包括镜头、资源引用等。
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


class ShotType(str, Enum):
    """镜头类型枚举"""
    CLOSE_UP = "close-up"  # 特写
    MEDIUM = "medium"  # 中景
    WIDE = "wide"  # 全景
    EXTREME_CLOSE_UP = "extreme-close-up"  # 大特写
    EXTREME_WIDE = "extreme-wide"  # 大全景
    OVER_THE_SHOULDER = "over-the-shoulder"  # 过肩镜头
    POINT_OF_VIEW = "point-of-view"  # 主观镜头


class TransitionType(str, Enum):
    """转场类型枚举"""
    CUT = "cut"  # 切
    FADE_IN = "fade-in"  # 淡入
    FADE_OUT = "fade-out"  # 淡出
    DISSOLVE = "dissolve"  # 叠化
    WIPE = "wipe"  # 划
    NONE = "none"  # 无转场


@dataclass
class ResourceReference:
    """资源引用
    
    用于在分镜中引用资源库中的资源，标明资源来源。
    """
    resource_id: str  # 资源ID
    resource_type: str  # 资源类型（character, scene, prop, action）
    resource_name: str  # 资源名称
    match_score: Optional[float] = None  # 匹配分数（0-1，表示匹配度）
    match_reason: Optional[str] = None  # 匹配原因说明
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "resource_name": self.resource_name,
            "match_score": self.match_score,
            "match_reason": self.match_reason,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResourceReference":
        """从字典创建资源引用对象"""
        return cls(
            resource_id=data["resource_id"],
            resource_type=data["resource_type"],
            resource_name=data["resource_name"],
            match_score=data.get("match_score"),
            match_reason=data.get("match_reason"),
        )


@dataclass
class Shot:
    """分镜镜头
    
    表示一个分镜镜头，包含画面描述、资源引用等信息。
    """
    shot_number: int  # 镜头编号
    scene_number: int  # 场景编号
    shot_type: ShotType  # 镜头类型
    duration: float  # 时长（秒）
    description: str  # 画面描述
    camera_angle: Optional[str] = None  # 拍摄角度
    characters: List[str] = field(default_factory=list)  # 角色列表
    dialogue: Optional[str] = None  # 对话内容
    transition: TransitionType = TransitionType.CUT  # 转场方式
    visual_style: Optional[str] = None  # 视觉风格描述
    # 资源引用
    character_resources: List[ResourceReference] = field(default_factory=list)  # 角色资源引用
    scene_resource: Optional[ResourceReference] = None  # 场景资源引用
    prop_resources: List[ResourceReference] = field(default_factory=list)  # 道具资源引用
    action_resources: List[ResourceReference] = field(default_factory=list)  # 动作资源引用
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "shot_number": self.shot_number,
            "scene_number": self.scene_number,
            "shot_type": self.shot_type.value,
            "duration": self.duration,
            "description": self.description,
            "camera_angle": self.camera_angle,
            "characters": self.characters,
            "dialogue": self.dialogue,
            "transition": self.transition.value,
            "visual_style": self.visual_style,
            "character_resources": [ref.to_dict() for ref in self.character_resources],
            "scene_resource": self.scene_resource.to_dict() if self.scene_resource else None,
            "prop_resources": [ref.to_dict() for ref in self.prop_resources],
            "action_resources": [ref.to_dict() for ref in self.action_resources],
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Shot":
        """从字典创建镜头对象"""
        return cls(
            shot_number=data["shot_number"],
            scene_number=data["scene_number"],
            shot_type=ShotType(data["shot_type"]),
            duration=data["duration"],
            description=data["description"],
            camera_angle=data.get("camera_angle"),
            characters=data.get("characters", []),
            dialogue=data.get("dialogue"),
            transition=TransitionType(data.get("transition", "cut")),
            visual_style=data.get("visual_style"),
            character_resources=[
                ResourceReference.from_dict(ref) 
                for ref in data.get("character_resources", [])
            ],
            scene_resource=ResourceReference.from_dict(data["scene_resource"]) 
                if data.get("scene_resource") else None,
            prop_resources=[
                ResourceReference.from_dict(ref) 
                for ref in data.get("prop_resources", [])
            ],
            action_resources=[
                ResourceReference.from_dict(ref) 
                for ref in data.get("action_resources", [])
            ],
            metadata=data.get("metadata", {}),
        )
    
    def get_resource_summary(self) -> str:
        """获取资源来源摘要
        
        Returns:
            资源来源的文本摘要，用于在描述中标注
        """
        parts = []
        
        if self.character_resources:
            char_names = [ref.resource_name for ref in self.character_resources]
            parts.append(f"角色: {', '.join(char_names)} (来自资源库)")
        
        if self.scene_resource:
            parts.append(f"场景: {self.scene_resource.resource_name} (来自资源库)")
        
        if self.prop_resources:
            prop_names = [ref.resource_name for ref in self.prop_resources]
            parts.append(f"道具: {', '.join(prop_names)} (来自资源库)")
        
        if self.action_resources:
            action_names = [ref.resource_name for ref in self.action_resources]
            parts.append(f"动作: {', '.join(action_names)} (来自资源库)")
        
        return "; ".join(parts) if parts else ""


@dataclass
class Storyboard:
    """分镜脚本
    
    包含完整的分镜脚本信息。
    """
    title: str  # 标题
    shots: List[Shot] = field(default_factory=list)  # 镜头列表
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    created_at: datetime = field(default_factory=datetime.now)  # 创建时间
    
    @property
    def total_duration(self) -> float:
        """总时长（秒）"""
        return sum(shot.duration for shot in self.shots)
    
    @property
    def total_shots(self) -> int:
        """总镜头数"""
        return len(self.shots)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "title": self.title,
            "storyboard": [shot.to_dict() for shot in self.shots],
            "metadata": {
                **self.metadata,
                "total_duration": self.total_duration,
                "total_shots": self.total_shots,
                "created_at": self.created_at.isoformat(),
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Storyboard":
        """从字典创建分镜脚本对象"""
        shots_data = data.get("storyboard", [])
        metadata = data.get("metadata", {})
        
        # 从metadata中提取created_at
        created_at = datetime.now()
        if "created_at" in metadata:
            created_at = datetime.fromisoformat(metadata["created_at"])
        
        # 移除自动计算的字段
        metadata = {k: v for k, v in metadata.items() 
                   if k not in ["total_duration", "total_shots", "created_at"]}
        
        return cls(
            title=data.get("title", ""),
            shots=[Shot.from_dict(shot_data) for shot_data in shots_data],
            metadata=metadata,
            created_at=created_at,
        )

