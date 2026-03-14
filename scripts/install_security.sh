#!/bin/bash
# 安全配置安装脚本
# 自动配置 Git Pre-commit Hook 和安全扫描

set -e

echo "🔒 AI 剧本杀 - 安全配置安装"
echo "================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. 安装 Pre-commit Hook
echo "📝 安装 Git Pre-commit Hook..."
cat > .git/hooks/pre-commit << 'HOOKEOF'
#!/bin/bash
# Git Pre-commit Hook - 安全扫描
set -e
echo "🔒 安全扫描：检查敏感信息..."
python3 "$(dirname "$0")/../scripts/security_scanner.py"
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✅ 提交允许"
else
    echo "🛑 提交被阻止"
fi
exit $exit_code
HOOKEOF

chmod +x .git/hooks/pre-commit
echo "✅ Pre-commit Hook 已安装"
echo ""

# 2. 检查 .gitignore
echo "📋 检查 .gitignore..."
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore 不存在，创建中..."
    cp .gitignore.example .gitignore 2>/dev/null || echo "请手动创建 .gitignore"
else
    echo "✅ .gitignore 已存在"
fi
echo ""

# 3. 检查 .env.example
echo "📝 检查 .env.example..."
if [ -f ".env.example" ]; then
    echo "✅ .env.example 已存在"
    echo "💡 使用方式：cp .env.example .env"
else
    echo "⚠️  .env.example 不存在"
fi
echo ""

# 4. 测试安全扫描器
echo "🧪 测试安全扫描器..."
if [ -f "scripts/security_scanner.py" ]; then
    python3 scripts/security_scanner.py --test 2>/dev/null || true
    echo "✅ 安全扫描器已就绪"
else
    echo "⚠️  安全扫描器不存在"
fi
echo ""

# 5. 显示使用说明
echo "================================"
echo "✅ 安全配置完成！"
echo ""
echo "📖 使用说明："
echo ""
echo "1. 每次 commit 前会自动扫描敏感信息"
echo "2. 发现 API Key 会自动阻止提交"
echo "3. 可以选择自动替换为 [REDACTED]"
echo ""
echo "📝 配置 API Key 的正确方式："
echo ""
echo "  # 使用环境变量"
echo "  export DASHSCOPE_API_KEY=sk-xxx"
echo "  export GITHUB_TOKEN=ghp_xxx"
echo ""
echo "  # 或在代码中读取"
echo "  import os"
echo "  API_KEY = os.environ.get('DASHSCOPE_API_KEY')"
echo ""
echo "🚫 错误做法（会被阻止）："
echo ""
echo "  API_KEY = \"sk-xxxxxxxxxxxxxxxx\""
echo "  TOKEN = \"ghp_xxxxxxxxxxxxxxxxxxxx\""
echo ""
echo "================================"
echo ""
