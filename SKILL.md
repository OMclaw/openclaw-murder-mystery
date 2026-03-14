---
name: ai-murder-mystery
description: AI 剧本杀 - 沉浸式侦探推理游戏，与 AI NPC 互动破案
author: OMclaw
version: 2.0.0
homepage: https://github.com/OMclaw/openclaw-murder-mystery
triggers:
  - "剧本杀"
  - "侦探游戏"
  - "推理游戏"
  - "谋杀之谜"
  - "玩剧本杀"
  - "开始侦探"
metadata: {
  "clawdbot": {
    "emoji": "🔍",
    "requires": {
      "bins": ["python3"]
    }
  }
}
---

# AI 剧本杀 - Murder Mystery

沉浸式侦探推理游戏，与 AI NPC 互动，找出真凶！

## ✨ 特性

- 🖼️ **高清配图** - 15 张精美插图（场景 + 角色 + 线索）
- 🤖 **AI NPC** - 5 个独立人格的嫌疑人
- 🔍 **推理破案** - 10 个问题内找出真凶
- 🌐 **多渠道** - 支持飞书、Telegram、Discord 等
- 🔒 **安全配置** - Pre-commit Hook 自动扫描敏感信息

## 🎮 开始游戏

```
"我想玩剧本杀"
"开始侦探游戏"
"来个推理案件"
```

## 🎯 游戏规则

1. 你扮演侦探，调查一起谋杀案
2. 有 5 个 NPC 嫌疑人（由 AI 扮演）
3. 你有 **10 个问题** 的机会
4. 找出真凶 + 完整推理 = 胜利
5. 问题用光或指认错误 = 失败

## 💬 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `开始游戏` | 开始新游戏 | `开始游戏` |
| `询问 [角色] [问题]` | 询问 NPC | `询问管家 昨晚你在做什么` |
| `线索` | 查看线索 | `线索` |
| `指认 [凶手]` | 提交答案 | `指认园丁` |
| `提示` | 获取提示 | `提示` |
| `暂停` | 暂停游戏 | `暂停` |
| `继续` | 继续游戏 | `继续` |
| `退出` | 退出游戏 | `退出` |

## 📖 当前剧本

### 🏰 庄园谋杀案（主角本）

**背景**: 1930 年，上海郊外的豪华庄园。庄园主人赵老爷被发现死在书房，是一个完美的"密室"。

**嫌疑人**:
1. 王管家 - 在庄园工作 30 年，忠诚谨慎
2. 李夫人 - 死者的妻子，婚姻不和
3. 张少爷 - 死者的独子，沉迷赌博
4. 陈女仆 - 负责书房清洁，胆小怕事
5. 刘园丁 - 负责花园，沉默寡言

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
│   └── manor_murder/           # 庄园谋杀案
└── scripts/
    └── security_scanner.py     # 安全扫描器
```

## 🔧 配置

### 环境变量（可选）

```bash
# 复制模板
cp config/.env.example .env

# 编辑 .env 文件
vim .env

# 或设置环境变量
export API_KEY=sk-xxx
```

### 安全配置

```bash
# 安装 Pre-commit Hook
chmod +x .git/hooks/pre-commit

# 安装安全扫描器
bash scripts/install_security.sh
```

## 📊 游戏统计

| 项目 | 数量 |
|------|------|
| 场景图 | 4 张 |
| 角色立绘 | 5 张 |
| 线索道具 | 6 张 |
| 剧本 | 1 个 |
| NPC | 5 个 |

## 🔗 链接

- **GitHub**: https://github.com/OMclaw/openclaw-murder-mystery
- **README**: 查看完整文档

## 📄 许可证

MIT License

---

**🔍 享受推理的乐趣！**
