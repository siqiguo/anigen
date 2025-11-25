"""
剧本解析器

将文本剧本解析为结构化数据。
"""

import re
from typing import Dict, Any, List, Optional


class ScriptParser:
    """剧本解析器
    
    将文本格式的剧本解析为结构化数据。
    支持简单的文本格式剧本。
    """
    
    def __init__(self):
        """初始化剧本解析器"""
        pass
    
    def parse(self, script_text: str, title: Optional[str] = None) -> Dict[str, Any]:
        """解析剧本文本
        
        Args:
            script_text: 剧本文本
            title: 剧本标题（可选，如果未提供则从文本中提取）
            
        Returns:
            结构化剧本数据
        """
        lines = script_text.strip().split('\n')
        
        # 提取标题
        if not title:
            title = self._extract_title(lines)
        
        # 解析场景
        scenes = self._parse_scenes(lines)
        
        # 提取角色信息
        characters = self._extract_characters(scenes)
        
        return {
            "title": title or "未命名剧本",
            "scenes": scenes,
            "characters": characters,
        }
    
    def _extract_title(self, lines: List[str]) -> Optional[str]:
        """从文本中提取标题
        
        Args:
            lines: 文本行列表
            
        Returns:
            标题字符串
        """
        # 查找第一行非空文本作为标题
        for line in lines[:5]:  # 只检查前5行
            line = line.strip()
            if line and not line.startswith(('场景', '第', '【', '[')):
                # 如果行较短且不包含冒号，可能是标题
                if len(line) < 50 and '：' not in line and ':' not in line:
                    return line
        return None
    
    def _parse_scenes(self, lines: List[str]) -> List[Dict[str, Any]]:
        """解析场景
        
        Args:
            lines: 文本行列表
            
        Returns:
            场景列表
        """
        scenes = []
        current_scene = None
        scene_number = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测场景开始标记
            scene_match = re.match(
                r'^(?:场景|第\s*(\d+)\s*场|【场景\s*(\d+)|\[场景\s*(\d+))',
                line,
                re.IGNORECASE
            )
            
            if scene_match:
                # 保存上一个场景
                if current_scene:
                    scenes.append(current_scene)
                
                # 开始新场景
                scene_number = int(scene_match.group(1) or scene_match.group(2) or scene_match.group(3) or len(scenes) + 1)
                current_scene = {
                    "scene_number": scene_number,
                    "location": "",
                    "time": "",
                    "characters": [],
                    "dialogue": [],
                    "action": "",
                    "notes": "",
                }
                continue
            
            if not current_scene:
                # 如果没有场景标记，创建第一个场景
                current_scene = {
                    "scene_number": scene_number,
                    "location": "",
                    "time": "",
                    "characters": [],
                    "dialogue": [],
                    "action": "",
                    "notes": "",
                }
            
            # 解析场景信息
            self._parse_scene_line(line, current_scene)
        
        # 添加最后一个场景
        if current_scene:
            scenes.append(current_scene)
        
        # 如果没有解析到场景，创建一个默认场景
        if not scenes:
            scenes.append({
                "scene_number": 1,
                "location": "未知地点",
                "time": "",
                "characters": [],
                "dialogue": [],
                "action": "",
                "notes": "",
            })
        
        return scenes
    
    def _parse_scene_line(self, line: str, scene: Dict[str, Any]) -> None:
        """解析场景中的一行文本
        
        Args:
            line: 文本行
            scene: 场景字典（会被修改）
        """
        # 解析地点
        location_match = re.search(r'(?:地点|场景|位置)[:：]\s*(.+)', line, re.IGNORECASE)
        if location_match:
            scene["location"] = location_match.group(1).strip()
            return
        
        # 解析时间
        time_match = re.search(r'(?:时间|时刻)[:：]\s*(.+)', line, re.IGNORECASE)
        if time_match:
            scene["time"] = time_match.group(1).strip()
            return
        
        # 解析对话（格式：角色名：对话内容）
        dialogue_match = re.match(r'^([^：:]+)[：:]\s*(.+)', line)
        if dialogue_match:
            character = dialogue_match.group(1).strip()
            text = dialogue_match.group(2).strip()
            
            # 提取情绪（如果存在）
            emotion_match = re.search(r'[（(](.+?)[）)]', text)
            emotion = emotion_match.group(1) if emotion_match else None
            
            # 移除情绪标记
            if emotion_match:
                text = re.sub(r'[（(].+?[）)]', '', text).strip()
            
            scene["dialogue"].append({
                "character": character,
                "text": text,
                "emotion": emotion or "平静"
            })
            
            # 添加角色到角色列表
            if character not in scene["characters"]:
                scene["characters"].append(character)
            
            return
        
        # 解析动作（格式：动作：... 或 [动作] ...）
        action_match = re.search(r'(?:动作|行为)[:：]\s*(.+)|^\[动作\]\s*(.+)', line, re.IGNORECASE)
        if action_match:
            scene["action"] = (action_match.group(1) or action_match.group(2)).strip()
            return
        
        # 解析备注
        notes_match = re.search(r'(?:备注|说明)[:：]\s*(.+)|^\[备注\]\s*(.+)', line, re.IGNORECASE)
        if notes_match:
            scene["notes"] = (notes_match.group(1) or notes_match.group(2)).strip()
            return
        
        # 如果没有匹配到特定格式，可能是动作或描述
        if not scene["action"] and len(line) > 5:
            # 如果当前没有动作，将这一行作为动作
            if not scene["action"]:
                scene["action"] = line
            else:
                scene["action"] += " " + line
    
    def _extract_characters(self, scenes: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
        """从场景中提取角色信息
        
        Args:
            scenes: 场景列表
            
        Returns:
            角色信息字典
        """
        characters = {}
        
        for scene in scenes:
            for char_name in scene.get("characters", []):
                if char_name not in characters:
                    characters[char_name] = {
                        "description": f"{char_name}的角色描述",
                        "appearance": f"{char_name}的外观描述"
                    }
        
        return characters
    
    def parse_simple_format(self, script_text: str) -> Dict[str, Any]:
        """解析简单格式的剧本（每行一个对话或动作）
        
        Args:
            script_text: 剧本文本
            
        Returns:
            结构化剧本数据
        """
        lines = script_text.strip().split('\n')
        
        scenes = []
        current_scene = {
            "scene_number": 1,
            "location": "未知地点",
            "time": "",
            "characters": [],
            "dialogue": [],
            "action": "",
            "notes": "",
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 尝试解析为对话
            dialogue_match = re.match(r'^([^：:]+)[：:]\s*(.+)', line)
            if dialogue_match:
                character = dialogue_match.group(1).strip()
                text = dialogue_match.group(2).strip()
                
                current_scene["dialogue"].append({
                    "character": character,
                    "text": text,
                    "emotion": "平静"
                })
                
                if character not in current_scene["characters"]:
                    current_scene["characters"].append(character)
            else:
                # 作为动作处理
                if current_scene["action"]:
                    current_scene["action"] += " " + line
                else:
                    current_scene["action"] = line
        
        scenes.append(current_scene)
        characters = self._extract_characters(scenes)
        
        return {
            "title": "未命名剧本",
            "scenes": scenes,
            "characters": characters,
        }

