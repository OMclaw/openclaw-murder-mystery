#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 剧本杀 - 大模型增强版游戏引擎
使用 qwen-image-2.0 实时生成图片
使用大模型生成 NPC 对话
"""

import json
import os
import random
import requests
from typing import Dict, List, Optional, Tuple

# API 配置 - 自动读取 OpenClaw 配置，兼容 OpenAI 和所有兼容 OpenAI API 的大模型
def get_llm_config():
    """
    自动读取 OpenClaw 的大模型配置
    支持多种配置来源，优雅降级
    兼容：OpenAI, Dashscope, Azure OpenAI, 以及其他兼容 OpenAI API 的模型
    """
    # 1. 优先使用环境变量（支持多种命名）
    api_keys_to_try = [
        ("OPENAI_API_KEY", "openai"),
        ("DASHSCOPE_API_KEY", "dashscope"),
        ("AZURE_OPENAI_API_KEY", "azure_openai"),
        ("LLM_API_KEY", "generic"),
    ]
    
    for env_var, provider in api_keys_to_try:
        api_key = os.environ.get(env_var)
        if api_key and not api_key.startswith("$"):
            return api_key, provider
    
    # 2. 尝试读取 OpenClaw 配置
    try:
        openclaw_config_paths = [
            os.path.expanduser("~/.openclaw/openclaw.json"),
            os.path.join(os.path.dirname(__file__), "..", "..", "openclaw.json"),
        ]
        
        for config_path in openclaw_config_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 尝试从 models.providers 读取
                providers = config.get("models", {}).get("providers", {})
                
                # 支持的提供商优先级（可按需调整）
                provider_priority = [
                    "openai",
                    "dashscope",
                    "azure_openai",
                    "dashscope-us",
                    "anthropic",
                    "google",
                    "ollama",
                    "localai",
                    "vllm",
                ]
                
                # 按优先级尝试
                for provider_name in provider_priority:
                    if provider_name in providers:
                        provider_config = providers[provider_name]
                        if isinstance(provider_config, dict):
                            api_key = provider_config.get("apiKey")
                            if api_key and not api_key.startswith("$"):
                                return api_key, provider_name
                
                # 尝试任意提供商
                for provider_name, provider_config in providers.items():
                    if isinstance(provider_config, dict):
                        api_key = provider_config.get("apiKey")
                        if api_key and not api_key.startswith("$"):
                            return api_key, provider_name
    except Exception as e:
        print(f"读取 OpenClaw 配置失败：{e}")
    
    # 3. 都没有则返回 None，使用规则模式
    return None, None

# 获取配置
API_KEY, LLM_PROVIDER = get_llm_config()

# 根据提供商确定 API 端点和模型
def get_provider_config(provider):
    """获取提供商的 API 配置"""
    configs = {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "chat_model": "gpt-4o",
            "image_model": "dall-e-3",
            "image_endpoint": "https://api.openai.com/v1/images/generations",
        },
        "dashscope": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "chat_model": "qwen3.5-plus",
            "image_model": "qwen-image-2.0",
            "image_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
        },
        "dashscope-us": {
            "base_url": "https://dashscope-us.aliyuncs.com/compatible-mode/v1",
            "chat_model": "qwen3.5-plus",
            "image_model": "qwen-image-2.0",
            "image_endpoint": "https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
        },
        "azure_openai": {
            "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT", "https://YOUR_RESOURCE.openai.azure.com"),
            "chat_model": os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            "image_model": "dall-e-3",
            "image_endpoint": None,  # Azure 需要特殊处理
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com/v1",
            "chat_model": "claude-3-5-sonnet-20241022",
            "image_model": None,  # Anthropic 不支持图片生成
            "image_endpoint": None,
        },
        "google": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
            "chat_model": "gemini-2.0-flash",
            "image_model": "imagen-3.0-generate-001",
            "image_endpoint": None,  # Google 需要特殊处理
        },
        "ollama": {
            "base_url": os.environ.get("OLLAMA_HOST", "http://localhost:11434/v1"),
            "chat_model": os.environ.get("OLLAMA_MODEL", "qwen2.5:32b"),
            "image_model": None,  # Ollama 通常不支持图片生成
            "image_endpoint": None,
        },
        "localai": {
            "base_url": os.environ.get("LOCALAI_HOST", "http://localhost:8080/v1"),
            "chat_model": os.environ.get("LOCALAI_MODEL", "gpt-3.5-turbo"),
            "image_model": "stable-diffusion",
            "image_endpoint": None,
        },
        "vllm": {
            "base_url": os.environ.get("VLLM_HOST", "http://localhost:8000/v1"),
            "chat_model": os.environ.get("VLLM_MODEL", "Qwen/Qwen2.5-32B-Instruct"),
            "image_model": None,
            "image_endpoint": None,
        },
    }
    return configs.get(provider, configs["openai"])

PROVIDER_CONFIG = get_provider_config(LLM_PROVIDER) if LLM_PROVIDER else None

IMAGE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images", "generated")

# 检测是否可用大模型
LLM_AVAILABLE = API_KEY is not None and not str(API_KEY).startswith("$")

# 检测是否支持图片生成
IMAGE_GENERATION_AVAILABLE = LLM_AVAILABLE and PROVIDER_CONFIG and PROVIDER_CONFIG.get("image_model") is not None

# 确保输出目录存在
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)


class LLMCharacter:
    """使用大模型的 NPC 角色类"""
    
    def __init__(self, char_id: str, name: str, description: str, secret: str, backstory: str):
        self.char_id = char_id
        self.name = name
        self.description = description
        self.secret = secret
        self.backstory = backstory
        self.memory = []  # 对话记忆
    
    def get_response(self, question: str, context: str = "") -> str:
        """使用大模型生成智能回复（兼容 OpenAI API 格式）"""
        
        if not LLM_AVAILABLE or not PROVIDER_CONFIG:
            return self._get_fallback_response(question)
        
        # 构建系统提示词
        system_prompt = f"""你正在扮演剧本杀游戏中的角色。请完全沉浸在这个角色中回答玩家的问题。

【角色信息】
姓名：{self.name}
身份：{self.description}
秘密：{self.secret}（不能直接说出，但要有所暗示）
背景故事：{self.backstory}

【回答规则】
1. 保持角色一致性，使用符合身份的说话方式
2. 不要直接透露秘密，但可以暗示
3. 回答要自然，像真人一样
4. 如果玩家问到敏感问题，可以回避或撒谎
5. 回答长度控制在 50-200 字

【当前情境】
{context if context else "玩家正在调查一起谋杀案，你是嫌疑人之一。"}

请根据以上信息，以{self.name}的身份回答玩家的问题。"""

        # 调用大模型 API（兼容 OpenAI 格式）
        try:
            base_url = PROVIDER_CONFIG["base_url"]
            model = PROVIDER_CONFIG["chat_model"]
            
            # 构建 API 端点
            if base_url.endswith("/v1"):
                chat_endpoint = f"{base_url}/chat/completions"
            else:
                chat_endpoint = f"{base_url}/chat/completions"
            
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            # 构建请求体（OpenAI 兼容格式）
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 300,
                "temperature": 0.8
            }
            
            # Anthropic 特殊处理
            if LLM_PROVIDER == "anthropic":
                headers["x-api-key"] = API_KEY
                headers["anthropic-version"] = "2023-06-01"
                payload = {
                    "model": model,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": question}],
                    "max_tokens": 1024
                }
            
            response = requests.post(
                chat_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 兼容不同 API 格式的响应
                if "choices" in result:
                    answer = result["choices"][0]["message"]["content"]
                elif "content" in result:
                    answer = result["content"][0]["text"]
                else:
                    answer = str(result)
                
                # 保存到记忆
                self.memory.append({
                    "question": question,
                    "answer": answer
                })
                
                return answer
            else:
                print(f"大模型 API 错误：{response.status_code} - {response.text[:200]}")
                return self._get_fallback_response(question)
                
        except Exception as e:
            print(f"大模型调用失败：{e}")
            return self._get_fallback_response(question)
    
    def _get_fallback_response(self, question: str) -> str:
        """大模型失败时的备选回复"""
        responses = [
            "这件事... 我不想多说。",
            "你问这个做什么？",
            "我记得不是很清楚了。",
            "这个... 让我想想。"
        ]
        return random.choice(responses)


class RealtimeImageGenerator:
    """实时图片生成器（兼容 OpenAI DALL-E 和 Dashscope）"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.provider = LLM_PROVIDER
        self.config = PROVIDER_CONFIG
    
    def generate_image(self, prompt: str, save_name: str) -> Optional[str]:
        """
        实时生成图片（兼容 OpenAI DALL-E 3 和 Dashscope qwen-image）
        
        Args:
            prompt: 图片描述提示词
            save_name: 保存的文件名
        
        Returns:
            图片文件路径，失败返回 None
        """
        
        if not IMAGE_GENERATION_AVAILABLE:
            print("⚠️ 当前模型不支持图片生成")
            return None
        
        # 检查是否已存在
        image_path = os.path.join(IMAGE_OUTPUT_DIR, save_name)
        if os.path.exists(image_path):
            print(f"图片已存在：{image_path}")
            return image_path
        
        # OpenAI DALL-E 3
        if self.provider == "openai":
            return self._generate_dalle(prompt, save_name)
        # Dashscope qwen-image
        elif self.provider in ["dashscope", "dashscope-us"]:
            return self._generate_qwen_image(prompt, save_name)
        # 其他提供商
        else:
            print(f"⚠️ 提供商 {self.provider} 的图片生成暂未支持")
            return None
    
    def _generate_dalle(self, prompt: str, save_name: str) -> Optional[str]:
        """使用 OpenAI DALL-E 3 生成图片"""
        image_path = os.path.join(IMAGE_OUTPUT_DIR, save_name)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result["data"][0]["url"]
                
                # 下载图片
                img_response = requests.get(image_url, timeout=30)
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"✅ DALL-E 3 图片生成成功：{image_path}")
                return image_path
            else:
                print(f"❌ DALL-E 错误：{response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            print(f"❌ DALL-E 生成失败：{e}")
            return None
    
    def _generate_qwen_image(self, prompt: str, save_name: str) -> Optional[str]:
        """使用 Dashscope qwen-image 生成图片"""
        image_path = os.path.join(IMAGE_OUTPUT_DIR, save_name)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "qwen-image-2.0",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ]
            },
            "parameters": {
                "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有 AI 感，构图混乱，文字模糊，扭曲",
                "prompt_extend": True,
                "watermark": False,
                "size": "1024*1024"
            }
        }
        
        try:
            url = self.config.get("image_endpoint", 
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation")
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'output' in result and 'choices' in result['output']:
                    image_url = result['output']['choices'][0]['message']['content'][0]['image']
                    
                    # 下载图片
                    img_response = requests.get(image_url, timeout=30)
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"✅ qwen-image 图片生成成功：{image_path}")
                    return image_path
                else:
                    print(f"❌ 返回格式异常：{result}")
                    return None
            else:
                print(f"❌ qwen-image 错误：{response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            print(f"❌ qwen-image 生成失败：{e}")
            return None
    
    def generate_scene(self, scene_type: str) -> Optional[str]:
        """生成场景图片"""
        scenes = {
            "manor_night": "神秘的欧式庄园夜景，午夜时分，古老的维多利亚式庄园，哥特式建筑风格，尖顶塔楼，窗户透出微弱灯光，周围有枯树和浓雾，悬疑恐怖氛围，电影级画质，8k 超高清",
            "study_room": "豪华欧式书房内部，中年男子尸体倒在红木书桌旁，地上有血迹，文件散落一地，台灯倒在地上发出微弱光线，书架上满古籍，窗帘紧闭，悬疑推理氛围，写实风格，电影级布光",
            "living_room": "复古欧式客厅，豪华吊灯，壁炉燃烧着火焰，古典真皮沙发，红木茶几，墙上挂着油画，温暖的灯光，电影级画质，细节丰富",
            "corridor": "昏暗的庄园长廊，墙上挂满复古油画，烛光摇曳，木地板反光，哥特式拱门，悬疑氛围，电影级布光，8k 高清"
        }
        
        prompt = scenes.get(scene_type, scenes["manor_night"])
        return self.generate_image(prompt, f"scene_{scene_type}.png")
    
    def generate_character(self, character_name: str, description: str) -> Optional[str]:
        """生成角色立绘"""
        prompt = f"{character_name}肖像，{description}，专业摄影棚灯光，8k 人像摄影，细节清晰"
        filename = f"character_{character_name.lower().replace(' ', '_')}.png"
        return self.generate_image(prompt, filename)
    
    def generate_clue(self, clue_name: str, description: str) -> Optional[str]:
        """生成线索道具图片"""
        prompt = f"{description}，{clue_name}，微距摄影，细节清晰，悬疑氛围"
        filename = f"clue_{clue_name.lower().replace(' ', '_')}.png"
        return self.generate_image(prompt, filename)


class AdvancedGameState:
    """大模型增强版游戏状态管理"""
    
    def __init__(self, use_llm: bool = True, use_realtime_images: bool = True):
        self.use_llm = use_llm  # 是否使用大模型 NPC
        self.use_realtime_images = use_realtime_images  # 是否实时生成图片
        self.image_generator = RealtimeImageGenerator() if use_realtime_images else None
        self.reset()
        self._init_characters()
    
    def _init_characters(self):
        """初始化大模型 NPC"""
        if self.use_llm:
            self.characters = {
                "butler": LLMCharacter(
                    "butler", "王管家",
                    "在庄园工作 30 年，忠诚谨慎，对庄园了如指掌",
                    "目击了部分案发过程但不敢说",
                    "30 年前被赵老爷收留，一直忠心耿耿。但昨晚他听到书房有争吵声，看到一个黑影从书房出来。"
                ),
                "wife": LLMCharacter(
                    "wife", "李夫人",
                    "死者的妻子，婚姻不和，长期遭受冷暴力",
                    "案发当晚去过书房",
                    "与赵老爷婚姻不和，经常争吵。昨晚 11 点去过书房，想讨论离婚的事，但赵老爷拒绝了。"
                ),
                "son": LLMCharacter(
                    "son", "张少爷",
                    "死者的独子，沉迷赌博，欠下巨额债务",
                    "急需遗产还债",
                    "欠下巨额赌债，急需继承遗产。昨晚一直在自己房间，但没人能证明。"
                ),
                "maid": LLMCharacter(
                    "maid", "陈女仆",
                    "负责书房清洁，胆小怕事，心思细腻",
                    "发现了关键线索",
                    "今天下午在书房打扫时，发现毒药瓶被移动过。她看到了什么，但不敢说。"
                ),
                "gardener": LLMCharacter(
                    "gardener", "刘园丁",
                    "负责花园，沉默寡言，身体强壮",
                    "案发时在花园工作",
                    "昨晚在花园修剪树枝，看到一个陌生人影在庄园外徘徊。"
                )
            }
        else:
            self.characters = {}
    
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
        self.generated_images = []
    
    def start_game(self, script_id: str = "manor_murder"):
        """开始游戏"""
        self.reset()
        self.game_started = True
        self.current_script = script_id
        
        # 预生成场景图片
        if self.use_realtime_images and self.image_generator:
            print("🎨 正在生成场景图片...")
            self.image_generator.generate_scene("manor_night")
            self.image_generator.generate_scene("study_room")
    
    def ask_question(self, character_id: str, question: str) -> Tuple[Optional[str], str]:
        """询问 NPC（大模型版本）"""
        if not self.game_started or self.game_ended or self.paused:
            return None, "游戏尚未开始或已暂停"
        
        if self.question_count >= self.max_questions:
            return None, "问题已用尽！请提交指认。"
        
        self.question_count += 1
        
        if self.use_llm and character_id in self.characters:
            character = self.characters[character_id]
            answer = character.get_response(question)
            
            # 生成角色图片（如果还没有）
            if self.use_realtime_images and self.image_generator:
                image_path = self.image_generator.generate_character(
                    character.name,
                    character.description
                )
                if image_path:
                    self.generated_images.append(image_path)
            
            remaining = self.max_questions - self.question_count
            return answer, f"剩余问题：{remaining}/{self.max_questions}"
        else:
            # 降级到规则版本
            return None, "角色不存在"
    
    def get_clue_image(self, clue_name: str, description: str) -> Optional[str]:
        """获取线索图片（实时生成）"""
        if self.use_realtime_images and self.image_generator:
            image_path = self.image_generator.generate_clue(clue_name, description)
            if image_path:
                self.generated_images.append(image_path)
                return image_path
        return None
    
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


# 简化版（不使用大模型）
class SimpleGameState:
    """简化版游戏状态（基于规则）"""
    
    def __init__(self):
        from game_engine import GameState
        self.simple_game = GameState()
    
    def __getattr__(self, name):
        # 代理到简单版本
        return getattr(self.simple_game, name)


# 工厂函数
def create_game(use_llm: bool = None, use_realtime_images: bool = None):
    """
    创建游戏实例
    
    Args:
        use_llm: 是否使用大模型 NPC（None=自动检测）
        use_realtime_images: 是否实时生成图片（None=自动检测）
    
    Returns:
        游戏实例
    """
    # 自动检测配置
    if use_llm is None:
        use_llm = LLM_AVAILABLE
    
    if use_realtime_images is None:
        use_realtime_images = LLM_AVAILABLE
    
    # 优雅降级：如果没有 API Key，自动使用规则模式
    if not LLM_AVAILABLE:
        print("ℹ️ 未检测到大模型 API 配置，使用基于规则的模式（兜底方案）")
        print("💡 如需启用大模型功能，请配置 DASHSCOPE_API_KEY 环境变量")
        return SimpleGameState()
    
    # 使用大模型增强版
    if use_llm or use_realtime_images:
        mode_desc = []
        if use_llm:
            mode_desc.append("🧠 大模型 NPC")
        if use_realtime_images:
            mode_desc.append("🎨 实时图片")
        print(f"✅ 已启用：{', '.join(mode_desc)}")
        return AdvancedGameState(use_llm, use_realtime_images)
    else:
        return SimpleGameState()


# 测试
if __name__ == "__main__":
    print("🎭 AI 剧本杀 - 大模型增强版测试\n")
    print("=" * 60)
    
    # 创建游戏（使用大模型 + 实时图片）
    game = create_game(use_llm=True, use_realtime_images=True)
    game.start_game()
    
    print("\n📖 游戏开始！\n")
    
    # 测试对话
    test_questions = [
        ("butler", "昨晚你在做什么？"),
        ("wife", "你和死者的关系怎么样？"),
        ("son", "有人看到你去过书房吗？"),
    ]
    
    for char_id, question in test_questions:
        print(f"\n👤 玩家：{question}")
        answer, status = game.ask_question(char_id, question)
        print(f"🎭 {game.characters[char_id].name}: {answer[:100]}...")
        print(f"📊 {status}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print(f"🎨 生成的图片：{len(game.generated_images)} 张")
