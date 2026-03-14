# 🎭 AI 剧本杀 Skills

> 沉浸式侦探推理游戏，与 AI NPC 互动，找出真凶！

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/OMclaw/openclaw-murder-mystery)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 特性

- 🖼️ **高清配图** - 15 张精美插图（场景 + 角色 + 线索）
- 🤖 **AI NPC** - 5 个独立人格的嫌疑人
- 🔍 **推理破案** - 10 个问题内找出真凶
- 🌐 **多渠道** - 支持飞书、Telegram、Discord 等
- 🔒 **安全配置** - Pre-commit Hook 自动扫描

---

## 🚀 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OMclaw/openclaw-murder-mystery.git ai-murder-mystery
```

### 配置（可选）

```bash
# 复制模板
cp config/.env.example .env

# 编辑 .env
vim .env
```

### 开始游戏

在 OpenClaw 中发送：
```
"我想玩剧本杀"
"开始侦探游戏"
```

---

## 🎮 游戏说明

### 故事背景

1930 年，上海郊外的豪华庄园。庄园主人赵老爷被发现死在书房，门窗紧闭，是一个完美的"密室"。

### 游戏规则

1. 扮演侦探，调查谋杀案
2. 5 个 NPC 嫌疑人
3. 10 个问题的机会
4. 找出真凶 = 胜利

### 嫌疑人

| 角色 | 身份 | 特点 |
|------|------|------|
| 王管家 | 工作 30 年 | 忠诚谨慎 |
| 李夫人 | 死者妻子 | 婚姻不和 |
| 张少爷 | 死者独子 | 沉迷赌博 |
| 陈女仆 | 书房清洁 | 胆小怕事 |
| 刘园丁 | 花园管理 | 沉默寡言 |

### 可用命令

| 命令 | 说明 |
|------|------|
| `开始游戏` | 开始新游戏 |
| `询问 [角色] [问题]` | 询问 NPC |
| `线索` | 查看线索 |
| `指认 [凶手]` | 提交答案 |
| `提示` | 获取提示 |

---

## 📁 项目结构

```
ai-murder-mystery/
├── murder_mystery_skill.py    # Skill 主入口
├── game_engine.py              # 游戏引擎（规则版）
├── game_engine_llm.py          # 游戏引擎（大模型版）
├── config/.env.example         # 环境变量模板
├── images/                     # 15 张游戏配图
├── scenarios/manor_murder/     # 庄园谋杀案
└── scripts/security_scanner.py # 安全扫描器
```

---

## 🔧 配置

### 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `API_KEY` | 大模型 API Key | 否 |
| `GITHUB_TOKEN` | GitHub Token | 否 |

**说明：** 不配置 API Key 会自动使用规则模式（无需 API）

### 使用方式

```bash
# 方式 1：.env 文件
API_KEY = "sk-YOUR-API-KEY-HERE"

# 方式 2：环境变量
export API_KEY=sk-xxx
```

---

## 🔒 安全配置

### 安装安全工具

```bash
bash scripts/install_security.sh
```

### 安全检查

```bash
# 自动扫描（commit 前）
git commit -m "xxx"

# 手动扫描
python3 scripts/security_scanner.py
```

### 检测范围

- API Key (Dashscope, OpenAI)
- GitHub Token
- Password/Secret
- Private Key

---

## 🐛 故障排除

**Q: 游戏无法启动？**
```bash
ls ~/.openclaw/workspace/skills/ai-murder-mystery
python3 -c "import murder_mystery_skill"
```

**Q: NPC 回复很奇怪？**
- 检查是否配置了 API Key
- 没有 API Key 会使用规则模式（回复较简单）

**Q: 图片无法显示？**
```bash
ls images/*.png
```

---

## 📄 许可证

MIT License

---

## 🔗 链接

- **GitHub**: https://github.com/OMclaw/openclaw-murder-mystery
- **安全报告**: SECURITY_REPORT.md

---

**🔍 享受推理的乐趣！** 🎭✨
