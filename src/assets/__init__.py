"""
资源库模块

提供角色、道具、场景、动作等资源的存储和管理功能。
"""

from .models import (
    ResourceType,
    Asset,
    Character,
    Prop,
    Scene,
    Action,
)
from .manager import AssetManager
from .storage import AssetStorage

__all__ = [
    "ResourceType",
    "Asset",
    "Character",
    "Prop",
    "Scene",
    "Action",
    "AssetManager",
    "AssetStorage",
]

