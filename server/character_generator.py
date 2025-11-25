"""
随机角色生成器

生成随机角色描述和图片。
"""

import random
from typing import Dict, List, Tuple


class RandomCharacterGenerator:
    """随机角色生成器"""
    
    # 角色模板
    APPEARANCES = [
        "年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装，棕色皮靴，腰间挂着剑",
        "年轻女性，银色长发，紫色眼睛，穿着魔法师袍，手持法杖，头戴魔法帽",
        "中年男性，棕色短发，绿色眼睛，穿着商人服装，手持账本，面带微笑",
        "年轻女性，金色卷发，蓝色眼睛，穿着公主裙，头戴王冠，优雅端庄",
        "年轻男性，红色短发，棕色眼睛，穿着战士盔甲，手持盾牌，表情坚毅",
        "年轻女性，黑色直发，黑色眼睛，穿着忍者服，手持苦无，动作敏捷",
        "中年女性，灰色长发，绿色眼睛，穿着学者长袍，手持书籍，知识渊博",
        "年轻男性，蓝色短发，灰色眼睛，穿着科技服装，手持设备，未来感十足",
        "年轻女性，粉色长发，粉色眼睛，穿着可爱服装，手持玩偶，活泼可爱",
        "中年男性，白色胡须，棕色眼睛，穿着长者服装，手持拐杖，智慧慈祥",
    ]
    
    PERSONALITIES = [
        "勇敢、乐观、善良",
        "聪明、冷静、理性",
        "活泼、开朗、热情",
        "神秘、优雅、高贵",
        "坚毅、果断、勇敢",
        "机智、灵活、敏捷",
        "博学、深思、智慧",
        "创新、前卫、科技感",
        "可爱、天真、纯真",
        "慈祥、温和、智慧",
    ]
    
    NAMES = [
        "小明", "小红", "小刚", "小美", "小强",
        "艾莉", "杰克", "露娜", "凯文", "艾米",
        "张伟", "李娜", "王强", "刘芳", "陈明",
        "亚瑟", "莉莉", "汤姆", "艾丽", "大卫",
    ]
    
    STYLES = ["anime", "cartoon", "realistic", "3D", "pixar"]
    
    GENDERS = ["男", "女"]
    
    AGES = list(range(15, 50))
    
    TAGS_POOL = [
        "主角", "冒险者", "魔法师", "战士", "商人",
        "公主", "忍者", "学者", "科技", "可爱",
        "男性", "女性", "年轻", "中年", "勇敢",
        "聪明", "活泼", "神秘", "坚毅", "机智",
    ]
    
    def generate_random_character(self) -> Dict:
        """生成随机角色数据
        
        Returns:
            包含角色信息的字典
        """
        # 随机选择外观和性格（保持一致性）
        index = random.randint(0, len(self.APPEARANCES) - 1)
        appearance = self.APPEARANCES[index]
        personality = self.PERSONALITIES[index]
        
        # 随机选择其他属性
        name = random.choice(self.NAMES)
        age = random.choice(self.AGES)
        gender = random.choice(self.GENDERS)
        style = random.choice(self.STYLES)
        
        # 随机选择标签（2-4个）
        num_tags = random.randint(2, 4)
        tags = random.sample(self.TAGS_POOL, num_tags)
        
        # 生成描述
        description = f"一个{age}岁的{gender}性角色，{personality}。"
        
        return {
            "name": name,
            "description": description,
            "appearance": appearance,
            "personality": personality,
            "age": age,
            "gender": gender,
            "style": style,
            "tags": tags,
        }
    
    def generate_character_with_variations(self, base_appearance: str = None) -> Dict:
        """基于给定外观生成变体角色
        
        Args:
            base_appearance: 基础外观描述，如果为None则随机生成
            
        Returns:
            包含角色信息的字典
        """
        if base_appearance is None:
            return self.generate_random_character()
        
        # 基于基础外观生成变体
        name = random.choice(self.NAMES)
        age = random.choice(self.AGES)
        gender = random.choice(self.GENDERS)
        style = random.choice(self.STYLES)
        personality = random.choice(self.PERSONALITIES)
        
        num_tags = random.randint(2, 4)
        tags = random.sample(self.TAGS_POOL, num_tags)
        
        description = f"一个{age}岁的{gender}性角色，{personality}。"
        
        return {
            "name": name,
            "description": description,
            "appearance": base_appearance,
            "personality": personality,
            "age": age,
            "gender": gender,
            "style": style,
            "tags": tags,
        }

