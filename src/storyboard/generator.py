"""
分镜生成器

提供从剧本生成分镜脚本的功能，优先使用资源库中的资源。
"""

from typing import List, Dict, Any, Optional
import logging

from .models import Storyboard, Shot, ShotType, TransitionType
from .matcher import ResourceMatcher
from ..assets import AssetManager

logger = logging.getLogger(__name__)


class StoryboardGenerator:
    """分镜生成器
    
    基于结构化剧本数据生成分镜脚本，优先从资源库中选择已有资源。
    """
    
    def __init__(
        self,
        asset_manager: AssetManager,
        default_shot_duration: float = 3.0,
        default_shot_type: ShotType = ShotType.MEDIUM
    ):
        """初始化分镜生成器
        
        Args:
            asset_manager: 资源管理器实例
            default_shot_duration: 默认镜头时长（秒）
            default_shot_type: 默认镜头类型
        """
        self.asset_manager = asset_manager
        self.matcher = ResourceMatcher(asset_manager)
        self.default_shot_duration = default_shot_duration
        self.default_shot_type = default_shot_type
    
    def generate_from_script(
        self,
        script_data: Dict[str, Any],
        prefer_existing_resources: bool = True
    ) -> Storyboard:
        """从剧本数据生成分镜脚本
        
        Args:
            script_data: 结构化剧本数据，格式参考 PROJECT_RULES.md
            prefer_existing_resources: 是否优先使用资源库中的资源
            
        Returns:
            生成的分镜脚本对象
        """
        title = script_data.get("title", "未命名剧本")
        scenes = script_data.get("scenes", [])
        characters_info = script_data.get("characters", {})
        
        shots = []
        shot_number = 1
        
        for scene_data in scenes:
            scene_number = scene_data.get("scene_number", 1)
            scene_shots = self._generate_scene_shots(
                scene_data,
                scene_number,
                characters_info,
                shot_number,
                prefer_existing_resources
            )
            shots.extend(scene_shots)
            shot_number += len(scene_shots)
        
        storyboard = Storyboard(
            title=title,
            shots=shots,
            metadata={
                "source": "script",
                "prefer_existing_resources": prefer_existing_resources,
            }
        )
        
        logger.info(f"生成分镜脚本完成: {len(shots)}个镜头，总时长 {storyboard.total_duration:.1f}秒")
        return storyboard
    
    def _generate_scene_shots(
        self,
        scene_data: Dict[str, Any],
        scene_number: int,
        characters_info: Dict[str, Any],
        start_shot_number: int,
        prefer_existing_resources: bool
    ) -> List[Shot]:
        """为单个场景生成镜头
        
        Args:
            scene_data: 场景数据
            scene_number: 场景编号
            characters_info: 角色信息字典
            start_shot_number: 起始镜头编号
            prefer_existing_resources: 是否优先使用资源库中的资源
            
        Returns:
            镜头列表
        """
        shots = []
        shot_number = start_shot_number
        
        location = scene_data.get("location", "")
        time = scene_data.get("time", "")
        characters = scene_data.get("characters", [])
        dialogue_list = scene_data.get("dialogue", [])
        action = scene_data.get("action", "")
        notes = scene_data.get("notes", "")
        
        # 匹配场景资源
        scene_resource_ref = None
        scene_style = None
        if prefer_existing_resources:
            scene_match = self.matcher.match_scene(
                location_type=self._extract_location_type(location),
                description=location,
                mood=notes,
                time_of_day=time
            )
            if scene_match:
                scene_resource_ref = scene_match[1]
                scene_style = scene_match[0].style
                logger.info(f"场景 {scene_number}: 匹配到资源库场景 '{scene_resource_ref.resource_name}'")
        
        # 匹配角色资源
        character_resources = {}
        if prefer_existing_resources and characters:
            for char_name in characters:
                char_info = characters_info.get(char_name, {})
                char_match = self.matcher.match_character(
                    name=char_name,
                    description=char_info.get("description", ""),
                    style=scene_style
                )
                if char_match:
                    character_resources[char_name] = char_match[1]
                    logger.info(f"场景 {scene_number}: 匹配到角色资源 '{char_match[1].resource_name}'")
        
        # 根据对话和动作生成镜头
        if dialogue_list:
            # 为每个对话生成一个镜头
            for i, dialogue_item in enumerate(dialogue_list):
                char_name = dialogue_item.get("character", "")
                dialogue_text = dialogue_item.get("text", "")
                emotion = dialogue_item.get("emotion", "")
                
                # 确定镜头类型（根据对话内容）
                shot_type = self._determine_shot_type_for_dialogue(
                    dialogue_text,
                    emotion,
                    i,
                    len(dialogue_list)
                )
                
                # 构建画面描述
                description = self._build_shot_description(
                    location=location,
                    characters=[char_name] if char_name else [],
                    action=action if i == 0 else None,  # 只在第一个镜头包含动作
                    dialogue=dialogue_text,
                    emotion=emotion,
                    scene_resource=scene_resource_ref,
                    character_resources=character_resources,
                    scene_number=scene_number
                )
                
                shot = Shot(
                    shot_number=shot_number,
                    scene_number=scene_number,
                    shot_type=shot_type,
                    duration=self.default_shot_duration,
                    description=description,
                    camera_angle=self._suggest_camera_angle(shot_type),
                    characters=[char_name] if char_name else [],
                    dialogue=dialogue_text,
                    transition=TransitionType.CUT if i == 0 else TransitionType.CUT,
                    visual_style=scene_style or "写实",
                    character_resources=[character_resources[char_name]] 
                        if char_name in character_resources else [],
                    scene_resource=scene_resource_ref,
                )
                
                shots.append(shot)
                shot_number += 1
        else:
            # 没有对话，生成动作镜头
            shot_type = ShotType.MEDIUM if action else self.default_shot_type
            
            description = self._build_shot_description(
                location=location,
                characters=characters,
                action=action,
                scene_resource=scene_resource_ref,
                character_resources=character_resources,
                scene_number=scene_number
            )
            
            shot = Shot(
                shot_number=shot_number,
                scene_number=scene_number,
                shot_type=shot_type,
                duration=self.default_shot_duration,
                description=description,
                camera_angle=self._suggest_camera_angle(shot_type),
                characters=characters,
                transition=TransitionType.CUT,
                visual_style=scene_style or "写实",
                character_resources=[
                    character_resources[char] 
                    for char in characters 
                    if char in character_resources
                ],
                scene_resource=scene_resource_ref,
            )
            
            shots.append(shot)
            shot_number += 1
        
        return shots
    
    def _build_shot_description(
        self,
        location: str,
        characters: List[str],
        action: Optional[str] = None,
        dialogue: Optional[str] = None,
        emotion: Optional[str] = None,
        scene_resource: Optional[Any] = None,
        character_resources: Optional[Dict[str, Any]] = None,
        scene_number: int = 1
    ) -> str:
        """构建镜头描述，包含资源来源标注
        
        Args:
            location: 场景位置
            characters: 角色列表
            action: 动作描述
            dialogue: 对话内容
            emotion: 情绪
            scene_resource: 场景资源引用
            character_resources: 角色资源引用字典
            scene_number: 场景编号
            
        Returns:
            完整的镜头描述文本
        """
        parts = []
        
        # 场景描述
        if scene_resource:
            parts.append(f"场景: {scene_resource.resource_name}（来自资源库）")
        else:
            parts.append(f"场景: {location}")
        
        # 角色描述
        if characters:
            char_descriptions = []
            for char in characters:
                if character_resources and char in character_resources:
                    char_descriptions.append(f"{char}（来自资源库）")
                else:
                    char_descriptions.append(char)
            parts.append(f"角色: {', '.join(char_descriptions)}")
        
        # 动作描述
        if action:
            parts.append(f"动作: {action}")
        
        # 对话和情绪
        if dialogue:
            emotion_text = f"（情绪: {emotion}）" if emotion else ""
            parts.append(f"对话: {dialogue}{emotion_text}")
        
        description = " | ".join(parts)
        
        return description
    
    def _determine_shot_type_for_dialogue(
        self,
        dialogue: str,
        emotion: str,
        index: int,
        total: int
    ) -> ShotType:
        """根据对话内容确定镜头类型
        
        Args:
            dialogue: 对话内容
            emotion: 情绪
            index: 当前对话索引
            total: 总对话数
            
        Returns:
            镜头类型
        """
        # 情绪相关的特写
        if emotion in ["悲伤", "愤怒", "惊讶", "恐惧"]:
            return ShotType.CLOSE_UP
        
        # 对话长度较短的可能是特写
        if len(dialogue) < 20:
            return ShotType.CLOSE_UP
        
        # 默认中景
        return ShotType.MEDIUM
    
    def _suggest_camera_angle(self, shot_type: ShotType) -> str:
        """根据镜头类型建议拍摄角度
        
        Args:
            shot_type: 镜头类型
            
        Returns:
            拍摄角度描述
        """
        angle_map = {
            ShotType.CLOSE_UP: "正面平视",
            ShotType.MEDIUM: "正面平视",
            ShotType.WIDE: "正面平视",
            ShotType.EXTREME_CLOSE_UP: "正面平视",
            ShotType.EXTREME_WIDE: "俯视或平视",
            ShotType.OVER_THE_SHOULDER: "过肩视角",
            ShotType.POINT_OF_VIEW: "主观视角",
        }
        return angle_map.get(shot_type, "正面平视")
    
    def _extract_location_type(self, location: str) -> Optional[str]:
        """从位置描述中提取场景类型
        
        Args:
            location: 位置描述
            
        Returns:
            场景类型（室内/室外等）
        """
        location_lower = location.lower()
        
        if any(keyword in location_lower for keyword in ["室内", "房间", "屋子", "建筑", "办公室"]):
            return "室内"
        elif any(keyword in location_lower for keyword in ["室外", "户外", "街道", "公园", "森林", "山"]):
            return "室外"
        
        return None

