# 🎭 AI 剧本杀 Skills

> 沉浸式侦探推理游戏，与 AI NPC 互动，找出真凶！

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/OMclaw/openclaw-murder-mystery)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![LLM](https://img.shields.io/badge/llm-OpenAI%20%7C%20Qwen%20%7C%20Claude-lightblue.svg)](https://github.com/OMclaw/openclaw-murder-mystery)

---

## 📖 目录

- [特性](#-特性)
- [快速开始](#-快速开始)
- [游戏说明](#-游戏说明)
- [配置](#-配置)
- [项目结构](#-项目结构)
- [安全配置](#-安全配置)
- [API 参考](#-api-参考)
- [故障排除](#-故障排除)
- [开发](#-开发)
- [许可证](#-许可证)

---

## ✨ 特性

### 🎮 游戏特色
- **沉浸式体验** - 15 张高清配图（场景 + 角色 + 线索）
- **AI NPC** - 5 个独立人格的嫌疑人，每个都有自己的秘密
- **推理破案** - 10 个问题内找出真凶
- **多渠道支持** - 飞书、Telegram、Discord 等
- **智能对话** - 支持大模型（Qwen、GPT-4、Claude 等）或规则模式

### 🔒 安全特性
- **Pre-commit Hook** - 自动扫描敏感信息
- **环境变量** - 所有配置通过环境变量管理
- **安全扫描器** - 检测 9 种敏感信息模式
- **零泄漏** - Git 历史干净，无敏感信息

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- OpenClaw 环境
- （可选）大模型 API Key

### 安装

#### 方式 1：从 GitHub 安装（推荐）

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OMclaw/openclaw-murder-mystery.git ai-murder-mystery
cd ai-murder-mystery
```

#### 方式 2：OpenClaw 技能市场

```
在 OpenClaw 中搜索 "剧本杀" 并安装
```

### 配置环境变量（可选）

```bash
# 复制模板
cp config/.env.example .env

# 编辑 .env 文件
vim .env

# 填写你的 API Key（不配置会使用规则模式）
API_KEY = "sk-your-api-key-here"
GITHUB_TOKEN = "ghp_your-token-here"
```

### 开始游戏

在 OpenClaw 中发送：

```
"我想玩剧本杀"
"开始侦探游戏"
"来个推理案件"
```

---

## 🎮 游戏说明

### 故事背景

**庄园谋杀案** - 1930 年，上海郊外的豪华庄园。庄园主人赵老爷被发现死在书房，门窗紧闭，是一个完美的"密室"。你是被请来的侦探，必须在天亮前找出真凶！

### 游戏规则

1. 你扮演侦探，调查一起谋杀案
2. 有 5 个 NPC 嫌疑人（由 AI 扮演）
3. 你有 **10 个问题** 的机会
4. 找出真凶 + 完整推理 = 胜利
5. 问题用光或指认错误 = 失败

### 嫌疑人

| 角色 | 身份 | 特点 |
|------|------|------|
| **王管家** | 在庄园工作 30 年 | 忠诚谨慎，知道很多秘密 |
| **李夫人** | 死者的妻子 | 婚姻不和，神色慌张 |
| **张少爷** | 死者的独子 | 沉迷赌博，欠下巨债 |
| **陈女仆** | 负责书房清洁 | 胆小怕事，发现线索 |
| **刘园丁** | 负责花园 | 沉默寡言，身体强壮 |

### 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `开始游戏` | 开始新游戏 | `开始游戏` |
| `询问 [角色] [问题]` | 询问 NPC | `询问管家 昨晚你在做什么` |
| `线索` | 查看已收集的线索 | `线索` |
| `指认 [凶手]` | 提交答案 | `指认园丁` |
| `提示` | 获取提示（消耗 1 次提问） | `提示` |
| `暂停` | 暂停游戏（保留进度） | `暂停` |
| `继续` | 继续游戏 | `继续` |
| `退出` | 退出游戏（清空进度） | `退出` |

### 游戏示例

```
你：我想玩剧本杀

AI: 🏰 庄园谋杀案 - 午夜庄园
    【背景故事】1930 年，上海郊外...
    【嫌疑人】
    1. 王管家
    2. 李夫人
    3. 张少爷
    4. 陈女仆
    5. 刘园丁
    
    你想先询问谁？

你：询问管家 昨晚你在做什么

AI: 🎭 王管家："昨晚 11 点我听到书房有动静..."
    【剩余问题】9/10

你：线索

AI: 【已收集的线索】
    📦 物理线索：
      • 毒药瓶：装有氰化物的小玻璃瓶
      • 怀表：指针停在 11:45
    📝 证词线索：
      • 管家证词：昨晚 11 点听到书房有动静

你：指认园丁

AI: 🎉 恭喜！你找出了真凶！
    【真相】园丁目睹了老爷的秘密...
    【评分】⭐⭐⭐⭐⭐ 完美破案！
```

---

## 🔧 配置

### 环境变量

| 变量名 | 说明 | 必需 | 示例 |
|--------|------|------|------|
| `API_KEY` | 大模型 API Key | 否 | `sk-YOUR-API-KEY-HERE` |
| `GITHUB_TOKEN` | GitHub Token | 否 | `ghp_YOUR-TOKEN-HERE` |

**说明：**
- 不配置 `API_KEY` 会自动使用规则模式（无需 API）
- 配置 `API_KEY` 会启用大模型智能对话

### 使用方式

#### 方式 1：.env 文件（推荐）

```bash
# .env
API_KEY = "sk-your-api-key-here"
GITHUB_TOKEN = "ghp_your-token-here"
```

#### 方式 2：环境变量

```bash
export API_KEY=sk-YOUR-API-KEY-HERE
export GITHUB_TOKEN=ghp_YOUR-TOKEN-HERE
```

#### 方式 3：代码中读取

```python
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    print("使用规则模式（无需 API）")
```

---

## 📁 项目结构

```
ai-murder-mystery/
├── murder_mystery_skill.py    # Skill 主入口（OpenClaw 接口）
├── game_engine.py              # 游戏引擎（规则版）
├── game_engine_llm.py          # 游戏引擎（大模型版）
├── config/
│   └── .env.example            # 环境变量模板
├── images/                     # 游戏配图（15 张）
│   ├── scene_*.png             # 场景图（4 张）
│   ├── character_*.png         # 角色立绘（5 张）
│   └── clue_*.png              # 线索道具（6 张）
├── scenarios/
│   └── manor_murder/           # 庄园谋杀案（主角本）
│       ├── config.yaml         # 剧本配置
│       ├── characters.json     # 角色信息
│       └── clues.json          # 线索信息
├── scripts/
│   ├── security_scanner.py     # 安全扫描器
│   └── install_security.sh     # 安全安装脚本
├── README.md                   # 本文档
├── SKILL.md                    # OpenClaw Skill 配置
├── SECURITY_AUDIT.md           # 安全审计报告
└── .gitignore                  # Git 忽略配置
```

---

## 🔒 安全配置

### 安装安全工具

```bash
# 安装 Pre-commit Hook
bash scripts/install_security.sh

# 或手动安装
chmod +x .git/hooks/pre-commit
```

### 安全检查

```bash
# 提交前自动扫描
git commit -m "xxx"
# 🔒 安全扫描：检查敏感信息...
# ✅ 安全扫描通过

# 手动扫描
python3 scripts/security_scanner.py

# 检查暂存区
git diff --cached | grep -E "sk-|ghp_|apikey|secret"
```

### 检测的敏感信息

- ✅ Dashscope/OpenAI API Key (`sk-[20+ 字符]`)
- ✅ GitHub Token (`gh[pousr]_[30+ 字符]`)
- ✅ Slack Token (`xox[baprs]-xxx`)
- ✅ Google API Key (`AIza[35 字符]`)
- ✅ AWS Access Key (`AKIA[16 字符]`)
- ✅ Private Key (`BEGIN PRIVATE KEY`)
- ✅ Password/Secret (`password = xxx`)

### 安全最佳实践

**✅ 正确做法：**
```python
# 从环境变量读取
import os
API_KEY = os.environ.get("API_KEY")
```

**❌ 错误做法（禁止！）：**
```python
# 硬编码（绝对禁止！）
API_KEY = "sk-57c62abc0ecb43e587bdc8fb4fbe9a8e"
```

---

## 📊 API 参考

### 支持的大模型

| 提供商 | 模型 | 配置方式 |
|--------|------|----------|
| **OpenAI** | GPT-4o | `API_KEY=sk-YOUR-API-KEY-HERE` |
| **通义千问** | Qwen3.5 | `API_KEY=sk-YOUR-API-KEY-HERE` |
| **Anthropic** | Claude 3.5 | `API_KEY=sk-ant-xxx` |
| **Google** | Gemini 2.0 | `API_KEY=xxx` |
| **Ollama** | 本地模型 | `OLLAMA_HOST=localhost:11434` |

### 环境变量配置

```bash
# OpenAI
export API_KEY=sk-proj-xxx

# 通义千问
export API_KEY=sk-YOUR-API-KEY-HERE

# Ollama（本地）
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=qwen2.5:32b
```

---

## 🐛 故障排除

### 问题 1：游戏无法启动

**症状：** 发送"开始游戏"没有反应

**解决：**
```bash
# 检查 Skill 是否正确安装
ls ~/.openclaw/workspace/skills/ai-murder-mystery

# 检查 Python 依赖
python3 -c "import murder_mystery_skill"
```

### 问题 2：NPC 回复很奇怪

**症状：** NPC 回答不符合角色设定

**解决：**
```bash
# 检查是否配置了 API Key
cat .env

# 如果没有 API Key，会使用规则模式（回复较简单）
# 配置 API Key 后重启 OpenClaw
```

### 问题 3：图片无法显示

**症状：** 游戏开始不显示图片

**解决：**
```bash
# 检查图片文件是否存在
ls images/*.png

# 检查渠道是否支持图片
# 飞书、Telegram、Discord 支持图片
# 纯文本渠道会自动降级为文本
```

### 问题 4：提交被阻止

**症状：** `git commit` 时显示"提交被阻止"

**解决：**
```bash
# 检查是否包含敏感信息
git diff --cached | grep -E "sk-|ghp_"

# 如果误报，可以临时跳过
git commit -m "xxx" --no-verify

# 或从 .gitignore 中排除该文件
```

---

## 🛠️ 开发

### 本地测试

```bash
# 运行测试脚本
python3 scripts/security_scanner.py

# 测试游戏引擎
python3 game_engine.py

# 测试 Skill 主入口
python3 murder_mystery_skill.py
```

### 添加新剧本

1. 在 `scenarios/` 下创建新剧本目录
2. 添加 `config.yaml`、`characters.json`、`clues.json`
3. 在 `game_engine.py` 中注册新剧本

### 提交代码

```bash
# 添加文件
git add .

# 提交（自动扫描）
git commit -m "feat: 添加新功能"

# 推送
git push origin main
```

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/OMclaw/openclaw-murder-mystery
- **OpenClaw 文档**: https://docs.openclaw.ai
- **问题反馈**: https://github.com/OMclaw/openclaw-murder-mystery/issues

---

## 🙏 致谢

感谢所有贡献者和用户！

---

**🔍 享受推理的乐趣！** 🎭✨
