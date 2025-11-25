"""
资源存储模块

负责资源的文件系统存储和索引管理。
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import Asset, ResourceType


class AssetStorage:
    """资源存储管理器
    
    负责资源的文件系统存储、索引管理和文件操作。
    """
    
    def __init__(self, base_dir: str = "./assets"):
        """初始化资源存储
        
        Args:
            base_dir: 资源库根目录路径
        """
        self.base_dir = Path(base_dir)
        self.index_file = self.base_dir / "index.json"
        self._ensure_directories()
        self._load_index()
    
    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        # 创建资源类型目录
        for resource_type in ResourceType:
            (self.base_dir / resource_type.value).mkdir(parents=True, exist_ok=True)
        
        # 创建图片目录
        (self.base_dir / "images").mkdir(parents=True, exist_ok=True)
    
    def _load_index(self) -> None:
        """加载资源索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.index: Dict[str, Dict[str, Any]] = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.index = {}
        else:
            self.index = {}
    
    def _save_index(self) -> None:
        """保存资源索引"""
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise RuntimeError(f"保存索引文件失败: {e}")
    
    def get_resource_dir(self, resource_type: ResourceType) -> Path:
        """获取资源类型目录
        
        Args:
            resource_type: 资源类型
            
        Returns:
            资源类型目录路径
        """
        return self.base_dir / resource_type.value
    
    def get_image_dir(self) -> Path:
        """获取图片目录
        
        Returns:
            图片目录路径
        """
        return self.base_dir / "images"
    
    def save_image(
        self, 
        image_path: str, 
        resource_id: str, 
        resource_type: ResourceType,
        suffix: str = ""
    ) -> str:
        """保存图片文件
        
        Args:
            image_path: 源图片路径
            resource_id: 资源ID
            resource_type: 资源类型
            suffix: 文件名后缀（用于区分同一资源的不同图片，如：_front, _side, _expression_happy等）
            
        Returns:
            保存后的图片路径（相对路径）
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 获取文件扩展名
        ext = Path(image_path).suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            raise ValueError(f"不支持的图片格式: {ext}")
        
        # 构建目标路径
        image_dir = self.get_image_dir() / resource_type.value
        image_dir.mkdir(parents=True, exist_ok=True)
        
        # 构建文件名：resource_id + suffix + ext
        filename = f"{resource_id}{suffix}{ext}"
        target_path = image_dir / filename
        
        # 复制文件
        shutil.copy2(image_path, target_path)
        
        # 返回相对路径
        return str(target_path.relative_to(self.base_dir))
    
    def delete_image(self, image_path: str) -> None:
        """删除图片文件
        
        Args:
            image_path: 图片路径（相对路径或绝对路径）
        """
        if not image_path:
            return
            
        if os.path.isabs(image_path):
            full_path = Path(image_path)
        else:
            full_path = self.base_dir / image_path
        
        if full_path.exists():
            full_path.unlink()
    
    def delete_character_images(self, character_id: str, expressions: Dict[str, str]) -> None:
        """删除角色的所有图片（三视图和表情）
        
        Args:
            character_id: 角色ID
            expressions: 表情字典
        """
        # 删除三视图（如果存在）
        image_dir = self.get_image_dir() / ResourceType.CHARACTER.value
        for suffix in ["", "_front", "_side", "_back"]:
            for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
                image_path = image_dir / f"{character_id}{suffix}{ext}"
                if image_path.exists():
                    image_path.unlink()
        
        # 删除表情图片
        for expression_path in expressions.values():
            if expression_path:
                self.delete_image(expression_path)
    
    def add_to_index(self, asset: Asset) -> None:
        """添加资源到索引
        
        Args:
            asset: 资源对象
        """
        self.index[asset.id] = asset.to_dict()
        self._save_index()
    
    def remove_from_index(self, resource_id: str) -> None:
        """从索引中移除资源
        
        Args:
            resource_id: 资源ID
        """
        if resource_id in self.index:
            del self.index[resource_id]
            self._save_index()
    
    def update_index(self, asset: Asset) -> None:
        """更新索引中的资源
        
        Args:
            asset: 资源对象
        """
        asset.updated_at = datetime.now()
        self.index[asset.id] = asset.to_dict()
        self._save_index()
    
    def get_from_index(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """从索引获取资源信息
        
        Args:
            resource_id: 资源ID
            
        Returns:
            资源字典，如果不存在返回None
        """
        return self.index.get(resource_id)
    
    def list_resources(self, resource_type: Optional[ResourceType] = None) -> List[Dict[str, Any]]:
        """列出所有资源
        
        Args:
            resource_type: 可选的资源类型过滤
            
        Returns:
            资源列表
        """
        if resource_type:
            return [
                resource for resource in self.index.values()
                if resource.get("resource_type") == resource_type.value
            ]
        return list(self.index.values())
    
    def search_resources(
        self,
        keyword: Optional[str] = None,
        tags: Optional[List[str]] = None,
        resource_type: Optional[ResourceType] = None
    ) -> List[Dict[str, Any]]:
        """搜索资源
        
        Args:
            keyword: 关键词（搜索名称和描述）
            tags: 标签列表
            resource_type: 资源类型过滤
            
        Returns:
            匹配的资源列表
        """
        results = []
        
        for resource in self.index.values():
            # 资源类型过滤
            if resource_type and resource.get("resource_type") != resource_type.value:
                continue
            
            # 关键词搜索
            if keyword:
                keyword_lower = keyword.lower()
                name_match = keyword_lower in resource.get("name", "").lower()
                desc_match = keyword_lower in resource.get("description", "").lower()
                if not (name_match or desc_match):
                    continue
            
            # 标签搜索
            if tags:
                resource_tags = resource.get("tags", [])
                if not any(tag in resource_tags for tag in tags):
                    continue
            
            results.append(resource)
        
        return results
    
    def get_image_path(self, image_path: str) -> Path:
        """获取图片的完整路径
        
        Args:
            image_path: 图片相对路径
            
        Returns:
            图片完整路径
        """
        if os.path.isabs(image_path):
            return Path(image_path)
        return self.base_dir / image_path

