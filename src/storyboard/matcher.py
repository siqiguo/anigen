"""
资源匹配器

提供从资源库中匹配资源的功能，支持基于描述、标签、属性等的智能匹配。
"""

from typing import List, Optional, Dict, Any, Tuple
from difflib import SequenceMatcher

from ..assets import AssetManager, Character, Scene, Prop, Action, ResourceType
from .models import ResourceReference


class ResourceMatcher:
    """资源匹配器
    
    提供智能资源匹配功能，根据描述、属性等从资源库中查找最匹配的资源。
    """
    
    def __init__(self, asset_manager: AssetManager):
        """初始化资源匹配器
        
        Args:
            asset_manager: 资源管理器实例
        """
        self.asset_manager = asset_manager
    
    def match_character(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        style: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_score: float = 0.3
    ) -> Optional[Tuple[Character, ResourceReference]]:
        """匹配角色资源
        
        Args:
            name: 角色名称（模糊匹配）
            description: 角色描述
            style: 风格要求
            tags: 标签列表
            min_score: 最小匹配分数阈值
            
        Returns:
            (角色对象, 资源引用) 元组，如果未找到匹配返回None
        """
        # 搜索角色资源
        candidates = self.asset_manager.search_resources(
            keyword=name,
            tags=tags,
            resource_type=ResourceType.CHARACTER
        )
        
        characters = [c for c in candidates if isinstance(c, Character)]
        
        # 风格过滤
        if style:
            characters = [c for c in characters if c.style == style]
        
        if not characters:
            return None
        
        # 计算匹配分数
        best_match = None
        best_score = 0.0
        best_reason = ""
        
        for char in characters:
            score = 0.0
            reasons = []
            
            # 名称匹配（权重：0.4）
            if name:
                name_score = self._calculate_similarity(name.lower(), char.name.lower())
                score += name_score * 0.4
                if name_score > 0.5:
                    reasons.append(f"名称相似度: {name_score:.2f}")
            
            # 描述匹配（权重：0.3）
            if description:
                desc_score = self._calculate_text_similarity(
                    description.lower(), 
                    char.description.lower()
                )
                score += desc_score * 0.3
                if desc_score > 0.3:
                    reasons.append(f"描述相似度: {desc_score:.2f}")
            
            # 标签匹配（权重：0.2）
            if tags:
                tag_score = self._calculate_tag_match(tags, char.tags)
                score += tag_score * 0.2
                if tag_score > 0:
                    reasons.append(f"标签匹配: {tag_score:.2f}")
            
            # 风格匹配（权重：0.1）
            if style and char.style == style:
                score += 0.1
                reasons.append("风格匹配")
            
            if score > best_score and score >= min_score:
                best_score = score
                best_match = char
                best_reason = "; ".join(reasons) if reasons else "基础匹配"
        
        if best_match:
            return (
                best_match,
                ResourceReference(
                    resource_id=best_match.id,
                    resource_type=ResourceType.CHARACTER.value,
                    resource_name=best_match.name,
                    match_score=best_score,
                    match_reason=best_reason,
                )
            )
        
        return None
    
    def match_scene(
        self,
        location_type: Optional[str] = None,
        description: Optional[str] = None,
        mood: Optional[str] = None,
        style: Optional[str] = None,
        time_of_day: Optional[str] = None,
        weather: Optional[str] = None,
        min_score: float = 0.3
    ) -> Optional[Tuple[Scene, ResourceReference]]:
        """匹配场景资源
        
        Args:
            location_type: 场景类型
            description: 场景描述
            mood: 氛围
            style: 风格
            time_of_day: 时间
            weather: 天气
            min_score: 最小匹配分数阈值
            
        Returns:
            (场景对象, 资源引用) 元组，如果未找到匹配返回None
        """
        # 搜索场景资源
        candidates = self.asset_manager.search_resources(
            keyword=description,
            resource_type=ResourceType.SCENE
        )
        
        scenes = [s for s in candidates if isinstance(s, Scene)]
        
        if not scenes:
            return None
        
        # 计算匹配分数
        best_match = None
        best_score = 0.0
        best_reason = ""
        
        for scene in scenes:
            score = 0.0
            reasons = []
            match_count = 0
            total_checks = 0
            
            # 场景类型匹配
            if location_type:
                total_checks += 1
                if scene.location_type == location_type:
                    score += 0.25
                    match_count += 1
                    reasons.append("场景类型匹配")
            
            # 氛围匹配
            if mood:
                total_checks += 1
                if scene.mood == mood:
                    score += 0.25
                    match_count += 1
                    reasons.append("氛围匹配")
            
            # 风格匹配
            if style:
                total_checks += 1
                if scene.style == style:
                    score += 0.2
                    match_count += 1
                    reasons.append("风格匹配")
            
            # 时间匹配
            if time_of_day:
                total_checks += 1
                if scene.time_of_day == time_of_day:
                    score += 0.15
                    match_count += 1
                    reasons.append("时间匹配")
            
            # 天气匹配
            if weather:
                total_checks += 1
                if scene.weather == weather:
                    score += 0.15
                    match_count += 1
                    reasons.append("天气匹配")
            
            # 描述匹配
            if description:
                desc_score = self._calculate_text_similarity(
                    description.lower(),
                    scene.description.lower()
                )
                score += desc_score * 0.3
                if desc_score > 0.3:
                    reasons.append(f"描述相似度: {desc_score:.2f}")
            
            if score > best_score and score >= min_score:
                best_score = score
                best_match = scene
                best_reason = "; ".join(reasons) if reasons else "基础匹配"
        
        if best_match:
            return (
                best_match,
                ResourceReference(
                    resource_id=best_match.id,
                    resource_type=ResourceType.SCENE.value,
                    resource_name=best_match.name,
                    match_score=best_score,
                    match_reason=best_reason,
                )
            )
        
        return None
    
    def match_props(
        self,
        names: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        style: Optional[str] = None,
        min_score: float = 0.3
    ) -> List[Tuple[Prop, ResourceReference]]:
        """匹配道具资源
        
        Args:
            names: 道具名称列表
            categories: 道具类别列表
            style: 风格
            min_score: 最小匹配分数阈值
            
        Returns:
            (道具对象, 资源引用) 元组列表
        """
        matches = []
        
        if not names and not categories:
            return matches
        
        # 搜索道具资源
        candidates = self.asset_manager.search_resources(
            resource_type=ResourceType.PROP
        )
        
        props = [p for p in candidates if isinstance(p, Prop)]
        
        # 风格过滤
        if style:
            props = [p for p in props if p.style == style]
        
        # 为每个名称或类别查找匹配
        search_terms = (names or []) + (categories or [])
        
        for term in search_terms:
            best_match = None
            best_score = 0.0
            best_reason = ""
            
            for prop in props:
                score = 0.0
                reasons = []
                
                # 名称匹配
                name_score = self._calculate_similarity(term.lower(), prop.name.lower())
                score += name_score * 0.5
                if name_score > 0.5:
                    reasons.append(f"名称相似度: {name_score:.2f}")
                
                # 类别匹配
                if prop.category:
                    category_score = self._calculate_similarity(
                        term.lower(), 
                        prop.category.lower()
                    )
                    score += category_score * 0.3
                    if category_score > 0.3:
                        reasons.append(f"类别相似度: {category_score:.2f}")
                
                # 描述匹配
                desc_score = self._calculate_text_similarity(
                    term.lower(),
                    prop.description.lower()
                )
                score += desc_score * 0.2
                if desc_score > 0.3:
                    reasons.append(f"描述相似度: {desc_score:.2f}")
                
                if score > best_score and score >= min_score:
                    best_score = score
                    best_match = prop
                    best_reason = "; ".join(reasons) if reasons else "基础匹配"
            
            if best_match:
                matches.append((
                    best_match,
                    ResourceReference(
                        resource_id=best_match.id,
                        resource_type=ResourceType.PROP.value,
                        resource_name=best_match.name,
                        match_score=best_score,
                        match_reason=best_reason,
                    )
                ))
        
        return matches
    
    def match_actions(
        self,
        action_types: Optional[List[str]] = None,
        style: Optional[str] = None,
        min_score: float = 0.3
    ) -> List[Tuple[Action, ResourceReference]]:
        """匹配动作资源
        
        Args:
            action_types: 动作类型列表
            style: 风格
            min_score: 最小匹配分数阈值
            
        Returns:
            (动作对象, 资源引用) 元组列表
        """
        matches = []
        
        if not action_types:
            return matches
        
        # 搜索动作资源
        candidates = self.asset_manager.search_resources(
            resource_type=ResourceType.ACTION
        )
        
        actions = [a for a in candidates if isinstance(a, Action)]
        
        # 风格过滤
        if style:
            actions = [a for a in actions if a.style == style]
        
        for action_type in action_types:
            best_match = None
            best_score = 0.0
            best_reason = ""
            
            for action in actions:
                score = 0.0
                reasons = []
                
                # 动作类型匹配
                type_score = self._calculate_similarity(
                    action_type.lower(),
                    action.action_type.lower()
                )
                score += type_score * 0.6
                if type_score > 0.5:
                    reasons.append(f"动作类型相似度: {type_score:.2f}")
                
                # 名称匹配
                name_score = self._calculate_similarity(
                    action_type.lower(),
                    action.name.lower()
                )
                score += name_score * 0.4
                if name_score > 0.5:
                    reasons.append(f"名称相似度: {name_score:.2f}")
                
                if score > best_score and score >= min_score:
                    best_score = score
                    best_match = action
                    best_reason = "; ".join(reasons) if reasons else "基础匹配"
            
            if best_match:
                matches.append((
                    best_match,
                    ResourceReference(
                        resource_id=best_match.id,
                        resource_type=ResourceType.ACTION.value,
                        resource_name=best_match.name,
                        match_score=best_score,
                        match_reason=best_reason,
                    )
                ))
        
        return matches
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度
        
        Args:
            str1: 字符串1
            str2: 字符串2
            
        Returns:
            相似度分数（0-1）
        """
        return SequenceMatcher(None, str1, str2).ratio()
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的相似度（考虑关键词匹配）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数（0-1）
        """
        # 基础字符串相似度
        base_score = self._calculate_similarity(text1, text2)
        
        # 关键词匹配
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return base_score
        
        # 计算共同关键词比例
        common_words = words1 & words2
        keyword_score = len(common_words) / max(len(words1), len(words2))
        
        # 综合分数
        return (base_score * 0.5) + (keyword_score * 0.5)
    
    def _calculate_tag_match(self, tags1: List[str], tags2: List[str]) -> float:
        """计算标签匹配度
        
        Args:
            tags1: 标签列表1
            tags2: 标签列表2
            
        Returns:
            匹配度分数（0-1）
        """
        if not tags1 or not tags2:
            return 0.0
        
        set1 = set(t.lower() for t in tags1)
        set2 = set(t.lower() for t in tags2)
        
        common = set1 & set2
        return len(common) / max(len(set1), len(set2))

