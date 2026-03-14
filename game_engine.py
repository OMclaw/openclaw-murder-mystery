#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 剧本杀 - 通用游戏引擎
渠道无关，支持 OpenClaw 所有渠道
"""

import json
import random
from typing import Dict, List, Optional, Tuple


class Character:
    """NPC 角色类"""
    
    def __init__(self, char_id: str, name: str, description: str, secret: str):
        self.char_id = char_id
        self.name = name
        self.description = description
        self.secret = secret
        self.questions = {
            "alibi": [],  # 不在场证明
            "relationship": [],  # 与死者关系
            "suspicious": [],  # 可疑行为
        }
    
    def get_response(self, question: str) -> str:
        """根据问题类型返回回答"""
        question_lower = question.lower()
        
        # 简单关键词匹配
        if any(word in question_lower for word in ["昨晚", "做什么", "在哪里", "时间"]):
            return self._get_alibi()
        elif any(word in question_lower for word in ["关系", "认识", "矛盾", "恩怨"]):
            return self._get_relationship()
        elif any(word in question_lower for word in ["可疑", "奇怪", "异常", "看到"]):
            return self._get_suspicious()
        else:
            return self._get_generic_response()
    
    def _get_alibi(self) -> str:
        """返回不在场证明"""
        if self.questions["alibi"]:
            return random.choice(self.questions["alibi"])
        return "昨晚我待在自己房间里，不太清楚外面发生了什么。"
    
    def _get_relationship(self) -> str:
        """返回关系描述"""
        if self.questions["relationship"]:
            return random.choice(self.questions["relationship"])
        return "我和老爷的关系... 这个不好说。"
    
    def _get_suspicious(self) -> str:
        """返回可疑行为"""
        if self.questions["suspicious"]:
            return random.choice(self.questions["suspicious"])
        return "我没发现什么异常。"
    
    def _get_generic_response(self) -> str:
        """通用回应"""
        responses = [
            "这个... 我不太清楚。",
            "你问这个做什么？",
            "我记得不是很清楚了。",
            "这件事我不想多说。"
        ]
        return random.choice(responses)


class GameState:
    """游戏状态管理"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置游戏状态"""
        self.game_started = False
        self.game_ended = False
        self.paused = False
        self.question_count = 0
        self.max_questions = 10
        self.clues_collected = []
        self.current_script = None
        self.player_name = None
    
    def start_game(self, script_id: str = "manor_murder"):
        """开始游戏"""
        self.reset()
        self.game_started = True
        self.current_script = script_id
    
    def pause_game(self):
        """暂停游戏"""
        if self.game_started and not self.game_ended:
            self.paused = True
            return True
        return False
    
    def resume_game(self):
        """继续游戏"""
        if self.paused:
            self.paused = False
            return True
        return False
    
    def ask_question(self, character_id: str, question: str) -> Tuple[Optional[str], str]:
        """询问 NPC"""
        if not self.game_started or self.game_ended or self.paused:
            return None, "游戏尚未开始或已暂停"
        
        if self.question_count >= self.max_questions:
            return None, "问题已用尽！请提交指认。"
        
        self.question_count += 1
        character = get_character(character_id)
        
        if not character:
            return None, f"未找到角色 '{character_id}'"
        
        answer = character.get_response(question)
        remaining = self.max_questions - self.question_count
        
        return answer, f"剩余问题：{remaining}/{self.max_questions}"
    
    def get_clues(self) -> Dict:
        """获取线索列表"""
        return {
            "physical": [
                {"name": "毒药瓶", "description": "装有氰化物的小玻璃瓶"},
                {"name": "怀表", "description": "指针停在 11:45"},
                {"name": "遗书", "description": "泛黄的信纸，有泪痕"}
            ],
            "testimony": [
                {"name": "管家证词", "content": "昨晚 11 点听到书房有动静"},
                {"name": "女仆证词", "content": "看到夫人深夜去过书房"}
            ]
        }
    
    def submit_accusation(self, suspect: str) -> str:
        """提交指认"""
        if not self.game_started:
            return "游戏尚未开始"
        
        self.game_ended = True
        
        # 简化版：随机判定
        correct = random.choice([True, False])
        
        if correct:
            return f"""🎉 恭喜！你找出了真凶！

【真相大白】
真凶是：{suspect}

【作案动机】
{self._get_motive(suspect)}

【评分】
⭐⭐⭐⭐⭐ 完美破案！"""
        else:
            return f"""❌ 很遗憾，指认错误。

【真相】
真凶另有其人。

{self._get_motive(suspect)}

游戏结束，发送 '重新开始' 再来一局！"""
    
    def _get_motive(self, suspect: str) -> str:
        """获取作案动机"""
        motives = {
            "管家": "管家为了报复老爷多年前的羞辱",
            "夫人": "夫人无法忍受长期的家庭暴力",
            "少爷": "少爷欠下巨额赌债，急需遗产",
            "女仆": "女仆被老爷威胁要赶出庄园",
            "园丁": "园丁目睹了老爷的秘密，被灭口未遂"
        }
        return motives.get(suspect, "动机成谜...")
    
    def get_hint(self) -> str:
        """获取提示"""
        if self.question_count >= self.max_questions:
            return "问题已用尽，请直接指认！"
        
        hints = [
            "注意死者的死亡时间",
            "书房是一个密室",
            "有人说了谎",
            "毒药瓶上的指纹很关键"
        ]
        return random.choice(hints)
    
    def is_game_command(self, message: str) -> bool:
        """检查是否是游戏命令"""
        commands = [
            "开始", "询问", "线索", "指认", "提示",
            "暂停", "继续", "退出", "重新开始", "帮助"
        ]
        return any(message.startswith(cmd) for cmd in commands)
    
    def get_off_topic_response(self) -> str:
        """无关问题的回应（沉浸感保护）"""
        responses = [
            "现在不是闲聊的时候，赵老爷的命案还没破呢！",
            "我们还是先找出真凶再说吧。",
            "等破了案，你再问我这些吧。",
            "现在最重要的是调查赵老爷的死因。"
        ]
        return random.choice(responses)


# 角色数据库
CHARACTERS = {
    "butler": Character(
        "butler", "王管家",
        "在庄园工作 30 年，忠诚谨慎，对庄园了如指掌",
        "目击了部分案发过程但不敢说"
    ),
    "wife": Character(
        "wife", "李夫人",
        "死者的妻子，婚姻不和，长期遭受冷暴力",
        "案发当晚去过书房"
    ),
    "son": Character(
        "son", "张少爷",
        "死者的独子，沉迷赌博，欠下巨额债务",
        "急需遗产还债"
    ),
    "maid": Character(
        "maid", "陈女仆",
        "负责书房清洁，胆小怕事，心思细腻",
        "发现了关键线索"
    ),
    "gardener": Character(
        "gardener", "刘园丁",
        "负责花园，沉默寡言，身体强壮",
        "案发时在花园工作"
    ),
}


def get_character(char_id: str) -> Optional[Character]:
    """获取角色"""
    return CHARACTERS.get(char_id)


# 角色名称映射
CHAR_MAP = {
    "管家": "butler",
    "王管家": "butler",
    "夫人": "wife",
    "李夫人": "wife",
    "少爷": "son",
    "张少爷": "son",
    "女仆": "maid",
    "陈女仆": "maid",
    "园丁": "gardener",
    "刘园丁": "gardener",
}


def get_character_id(name: str) -> Optional[str]:
    """根据名称获取角色 ID"""
    for key, value in CHAR_MAP.items():
        if key in name:
            return value
    return None
