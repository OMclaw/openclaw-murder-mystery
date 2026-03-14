#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 剧本杀 - OpenClaw Skill 主入口
兼容所有 OpenClaw 支持的 Channel（飞书、Telegram、Discord 等）
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from game_engine import GameState, get_character_id, CHAR_MAP

# 游戏状态存储（生产环境应该用数据库）
games = {}


def get_user_game(user_id: str) -> GameState:
    """获取或创建用户的游戏实例"""
    if user_id not in games:
        games[user_id] = GameState()
    return games[user_id]


def create_welcome_message() -> dict:
    """创建欢迎消息（支持图片和文本）"""
    return {
        "type": "mixed",
        "content": [
            {
                "type": "image",
                "source": "images/scene_manor_exterior.png"
            },
            {
                "type": "text",
                "content": """
╔══════════════════════════════════════════╗
║        🔍 欢迎进入 AI 剧本杀世界          ║
╚══════════════════════════════════════════╝

在这里，你将扮演侦探，与 AI NPC 互动，
找出谋杀案的真凶！

【游戏规则】
• 你有 10 次提问机会
• 询问 NPC，收集线索
• 找出真凶并提交指认
• 问题用光或指认错误 = 失败

【当前可用剧本】
🏰 庄园谋杀案 - 午夜庄园，富商遇害，完美密室...

【如何开始】
发送 "开始游戏" 或 "庄园谋杀案" 开始游戏

【可用命令】
• 开始游戏 - 开始新游戏
• 询问 [角色] [问题] - 例如：询问管家昨晚你在做什么
• 线索 - 查看已收集的线索
• 指认 [凶手] - 提交答案
• 提示 - 获取提示（消耗 1 次提问机会）
• 暂停 - 暂停游戏（保留进度）
• 继续 - 继续游戏
• 退出 - 退出游戏（清空进度）
"""
            }
        ]
    }


def create_game_intro() -> dict:
    """创建游戏开始消息（支持图片）"""
    return {
        "type": "mixed",
        "content": [
            {
                "type": "image",
                "source": "images/scene_study_room.png"
            },
            {
                "type": "text",
                "content": """
╔══════════════════════════════════════════╗
║         🏰 庄园谋杀案                     ║
║            午夜庄园                       ║
╚══════════════════════════════════════════╝

【背景故事】
1930 年，上海郊外的一座豪华庄园。
庄园主人赵老爷是当地有名的富商，为人严厉，树敌众多。

今晚，赵老爷在书房处理账目，家人都已回房休息。
午夜 12 点，一声尖叫划破夜空...

当众人赶到书房时，赵老爷趴在书桌上，已经没有了呼吸。
书房的门从里面反锁，窗户紧闭，是一个完美的"密室"。

你是被请来的侦探，必须在天亮前找出真凶！

【死者信息】
• 姓名：赵老爷
• 年龄：58 岁
• 死因：氰化物中毒
• 死亡时间：约 23:30-24:00

【嫌疑人】
"""
            },
            # 角色立绘
            {
                "type": "image",
                "source": "images/character_butler.png"
            },
            {
                "type": "text",
                "content": "1️⃣ 王管家 - 在庄园工作 30 年，忠诚谨慎\n"
            },
            {
                "type": "image",
                "source": "images/character_mrs_li.png"
            },
            {
                "type": "text",
                "content": "2️⃣ 李夫人 - 死者的妻子，婚姻不和\n"
            },
            {
                "type": "image",
                "source": "images/character_young_master.png"
            },
            {
                "type": "text",
                "content": "3️⃣ 张少爷 - 死者的独子，沉迷赌博\n"
            },
            {
                "type": "image",
                "source": "images/character_maid.png"
            },
            {
                "type": "text",
                "content": "4️⃣ 陈女仆 - 负责书房清洁，胆小怕事\n"
            },
            {
                "type": "image",
                "source": "images/character_gardener.png"
            },
            {
                "type": "text",
                "content": """5️⃣ 刘园丁 - 负责花园，沉默寡言

【游戏开始】
你有 10 次提问机会，找出真凶！

【可用命令】
• 询问 [角色] [问题] - 例如：询问管家昨晚你在做什么
• 线索 - 查看已收集的线索
• 指认 [凶手] - 提交答案
• 提示 - 获取提示（消耗 1 次提问机会）
• 暂停 - 暂停游戏（保留进度）
• 继续 - 继续游戏
• 退出 - 退出游戏

─────────────────────────────────────────────
"""
            }
        ]
    }


def create_character_image(character_name: str) -> dict:
    """创建角色图片消息"""
    char_id = get_character_id(character_name)
    if not char_id:
        return None
    
    image_map = {
        "butler": "character_butler.png",
        "wife": "character_mrs_li.png",
        "son": "character_young_master.png",
        "maid": "character_maid.png",
        "gardener": "character_gardener.png",
    }
    
    image_file = image_map.get(char_id)
    if not image_file:
        return None
    
    return {
        "type": "mixed",
        "content": [
            {
                "type": "image",
                "source": f"images/{image_file}"
            }
        ]
    }


def create_clue_image(clue_name: str) -> dict:
    """创建线索图片消息"""
    clue_map = {
        "遗书": "clue_letter.png",
        "毒药": "clue_poison.png",
        "怀表": "clue_watch.png",
        "匕首": "clue_dagger.png",
        "照片": "clue_photo.png",
        "脚印": "clue_footprint.png",
    }
    
    image_file = None
    for key, value in clue_map.items():
        if key in clue_name:
            image_file = value
            break
    
    if not image_file:
        return None
    
    return {
        "type": "mixed",
        "content": [
            {
                "type": "image",
                "source": f"images/{image_file}"
            }
        ]
    }


def handle_user_message(user_id: str, message: str, channel: str = None) -> dict:
    """
    处理用户消息 - Channel 无关
    
    Args:
        user_id: 用户 ID
        message: 用户消息
        channel: Channel 名称（可选）
    
    Returns:
        响应消息（支持文本、图片、混合消息）
    """
    game = get_user_game(user_id)
    message = message.strip()
    
    # 开始游戏
    if message in ["开始游戏", "庄园谋杀案", "开始"]:
        game.start_game("manor_murder")
        return create_game_intro()
    
    # 检查游戏状态
    if not game.game_started:
        return {
            "type": "text",
            "content": "游戏尚未开始，请发送 '开始游戏' 开始。"
        }
    
    # 暂停游戏
    if message in ["暂停", "暂停游戏"]:
        response = game.pause_game()
        return {
            "type": "text",
            "content": "游戏已暂停。发送 '继续' 继续游戏。" if response else "游戏无法暂停"
        }
    
    # 继续游戏
    if message in ["继续", "继续游戏"]:
        response = game.resume_game()
        return {
            "type": "text",
            "content": "游戏已继续。" if response else "游戏未暂停"
        }
    
    # 退出游戏
    if message in ["退出", "退出游戏"]:
        game.reset()
        return {
            "type": "text",
            "content": "游戏已退出。发送 '开始游戏' 重新开始。"
        }
    
    # 检查是否无关问题（沉浸感保护）
    if game.game_started and not game.game_ended and not game.paused:
        if not game.is_game_command(message):
            response = game.get_off_topic_response()
            return {
                "type": "text",
                "content": response
            }
    
    if game.game_ended:
        return {
            "type": "text",
            "content": "游戏已结束。发送 '重新开始' 开始新游戏。"
        }
    
    # 询问 NPC
    if message.startswith("询问"):
        return handle_inquiry(game, message)
    
    # 查看线索
    elif message == "线索":
        return handle_clues(game)
    
    # 指认凶手
    elif message.startswith("指认"):
        return handle_accusation(game, message)
    
    # 获取提示
    elif message == "提示":
        hint = game.get_hint()
        return {
            "type": "text",
            "content": f"💡 提示：{hint}"
        }
    
    # 重新开始
    elif message == "重新开始":
        game.reset()
        game.start_game("manor_murder")
        return create_game_intro()
    
    # 帮助
    elif message in ["帮助", "help", "?"]:
        return {
            "type": "text",
            "content": """【可用命令】
• 询问 [角色] [问题] - 例如：询问管家昨晚你在做什么
• 线索 - 查看已收集的线索
• 指认 [凶手] - 提交答案
• 提示 - 获取提示（消耗 1 次提问机会）
• 暂停 - 暂停游戏（保留进度）
• 继续 - 继续游戏
• 退出 - 退出游戏（清空进度）
• 重新开始 - 重新开始游戏"""
        }
    
    else:
        return {
            "type": "text",
            "content": """我不理解这个命令。

【可用命令】
• 询问 [角色] [问题]
• 线索
• 指认 [凶手]
• 提示
• 暂停
• 继续
• 退出

发送 '帮助' 查看更多。"""
        }


def handle_inquiry(game, command: str) -> dict:
    """处理询问命令"""
    parts = command[2:].strip().split(" ", 1)
    
    if len(parts) < 2:
        return {
            "type": "text",
            "content": "格式错误。请使用：询问 [角色] [问题]\n例如：询问管家 昨晚你在做什么"
        }
    
    character = parts[0]
    question = parts[1]
    
    # 获取角色 ID
    char_id = get_character_id(character)
    
    if not char_id:
        return {
            "type": "text",
            "content": f"未找到角色 '{character}'。\n可用角色：管家、夫人、少爷、女仆、园丁"
        }
    
    # 执行询问
    answer, status = game.ask_question(char_id, question)
    
    if answer is None:
        return {
            "type": "text",
            "content": status
        }
    
    # 构建响应（带角色图片）
    remaining = game.max_questions - game.question_count
    
    response_content = []
    
    # 添加角色图片
    char_image = create_character_image(character)
    if char_image:
        response_content.extend(char_image["content"])
    
    # 添加回答文本
    response_content.append({
        "type": "text",
        "content": f"{answer}\n\n【剩余问题】{remaining}/{game.max_questions}"
    })
    
    # 检查游戏是否结束
    if game.game_ended:
        response_content.append({
            "type": "text",
            "content": "\n\n⚠️ 问题已用尽！发送 '指认 [凶手]' 提交答案。"
        })
    
    return {
        "type": "mixed",
        "content": response_content
    }


def handle_clues(game) -> dict:
    """处理查看线索命令"""
    clues = game.get_clues()
    
    response_content = []
    
    # 物理线索（带图片）
    if "physical" in clues:
        for clue in clues["physical"]:
            # 尝试添加线索图片
            clue_image = create_clue_image(clue["name"])
            if clue_image:
                response_content.extend(clue_image["content"])
            
            response_content.append({
                "type": "text",
                "content": f"📦 {clue['name']}: {clue['description']}\n"
            })
    
    # 证词线索
    if "testimony" in clues:
        response_content.append({
            "type": "text",
            "content": "\n📝 证词线索：\n"
        })
        for clue in clues["testimony"]:
            response_content.append({
                "type": "text",
                "content": f"  • {clue['name']}: {clue['content']}\n"
            })
    
    return {
        "type": "mixed",
        "content": response_content
    }


def handle_accusation(game, command: str) -> dict:
    """处理指认命令"""
    suspect = command[2:].strip()
    
    if not suspect:
        return {
            "type": "text",
            "content": "请指定要指认的凶手。\n例如：指认园丁"
        }
    
    result = game.submit_accusation(suspect)
    
    return {
        "type": "text",
        "content": result
    }


# OpenClaw Skill 入口
def main(message: str, user_id: str, channel: str = None) -> dict:
    """
    OpenClaw Skill 主入口函数
    
    Args:
        message: 用户消息
        user_id: 用户 ID
        channel: Channel 名称（飞书、Telegram 等）
    
    Returns:
        响应消息
    """
    return handle_user_message(user_id, message, channel)


# 测试
if __name__ == "__main__":
    # 模拟用户消息
    test_messages = [
        "开始游戏",
        "询问管家 昨晚你在做什么",
        "这个技能怎么做的",  # 无关问题
        "线索",
        "提示",
        "暂停",
        "继续",
        "指认园丁"
    ]
    
    user_id = "test_user"
    
    print("🎭 AI 剧本杀 - 渠道无关版本测试\n")
    print("=" * 60)
    
    for msg in test_messages:
        print(f"\n👤 用户：{msg}")
        response = handle_user_message(user_id, msg)
        
        if response["type"] == "mixed":
            for item in response["content"]:
                if item["type"] == "image":
                    print(f"🖼️ [图片] {item['source']}")
                elif item["type"] == "text":
                    print(f"💬 {item['content'][:200]}...")
        else:
            print(f"💬 {response['content'][:200]}...")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
