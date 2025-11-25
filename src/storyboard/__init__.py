"""
分镜生成模块

提供从剧本生成分镜脚本的功能，支持资源库资源优先匹配。
"""

from .models import (
    Storyboard,
    Shot,
    ResourceReference,
    ShotType,
    TransitionType,
)
from .generator import StoryboardGenerator
from .matcher import ResourceMatcher

__all__ = [
    "Storyboard",
    "Shot",
    "ResourceReference",
    "ShotType",
    "TransitionType",
    "StoryboardGenerator",
    "ResourceMatcher",
]

