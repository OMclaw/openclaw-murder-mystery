# 🎭 AI 剧本杀 Skills

沉浸式侦探推理游戏，与 AI NPC 互动，找出真凶！

## ✨ 特性

- 🖼️ **高清配图** - 15 张精美插图（场景 + 角色 + 线索）
- 🤖 **AI NPC** - 5 个独立人格的嫌疑人
- 🔍 **推理破案** - 10 个问题内找出真凶
- 🌐 **多渠道** - 支持飞书、Telegram、Discord 等
- 🔒 **安全配置** - Pre-commit Hook 自动扫描敏感信息

## 📁 项目结构

```
ai-murder-mystery/
├── murder_mystery_skill.py    # Skill 主入口
├── game_engine.py              # 游戏引擎（规则版）
├── game_engine_llm.py          # 游戏引擎（大模型版）
├── config/
│   └── .env.example            # 环境变量模板
├── images/                     # 15 张游戏配图
├── scenarios/
│   └── manor_murder/           # 庄园谋杀案（主角本）
└── scripts/
    └── security_scanner.py     # 安全扫描器
```

## 🚀 快速开始

### 在 OpenClaw 中使用

```
"我想玩剧本杀"
"开始侦探游戏"
```

### 配置环境变量

```bash
# 复制模板
cp config/.env.example .env

# 编辑 .env 文件
vim .env

# 或设置环境变量
export DASHSCOPE_API_KEY=sk-xxx
```

## 🎮 游戏命令

| 命令 | 说明 |
|------|------|
| `开始游戏` | 开始新游戏 |
| `询问 [角色] [问题]` | 询问 NPC |
| `线索` | 查看线索 |
| `指认 [凶手]` | 提交答案 |
| `提示` | 获取提示 |

## 🔒 安全配置

### Pre-commit Hook

每次 commit 前自动扫描敏感信息：

```bash
# 安装
chmod +x .git/hooks/pre-commit
```

### 检测的敏感信息

- API Key (Dashscope, OpenAI)
- GitHub Token
- Password/Secret
- Private Key

### 环境变量

**✅ 正确做法**:
```python
import os
API_KEY = os.environ.get("DASHSCOPE_API_KEY")
```

**❌ 错误做法**:
```python
API_KEY = "sk-xxxxx"  # 禁止硬编码！
```

## 📊 游戏统计

| 项目 | 数量 |
|------|------|
| 场景图 | 4 张 |
| 角色立绘 | 5 张 |
| 线索道具 | 6 张 |
| 剧本 | 1 个 |
| NPC | 5 个 |

## 📄 许可证

MIT License

---

**🔍 享受推理的乐趣！**
