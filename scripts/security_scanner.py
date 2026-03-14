#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Pre-commit Security Scanner
自动检测和替换敏感信息

使用方法：
1. 复制到 .git/hooks/pre-commit
2. 添加执行权限：chmod +x .git/hooks/pre-commit
3. 每次 commit 前自动运行
"""

import os
import re
import sys
from pathlib import Path

# 敏感信息模式
SECRET_PATTERNS = {
    "Dashscope API Key": r"sk-[a-zA-Z0-9]{20,}",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{20,}",
    "GitHub Token": r"gh[pousr]_[a-zA-Z0-9]{30,}",
    "Slack Token": r"xox[baprs]-[0-9a-zA-Z-]+",
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Private Key": r"BEGIN (RSA |OPENSSH )?PRIVATE KEY",
    "Password": r"(?i)password\s*[:=]\s*[^\s]+",
    "Secret": r"(?i)secret\s*[:=]\s*[^\s]+",
}

# 替换为指代符号
REDACTED_FORMAT = "[REDACTED: {}]"


def get_staged_files():
    """获取暂存的文件列表"""
    import subprocess
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split("\n") if result.stdout.strip() else []


def should_skip_file(filepath):
    """检查是否应该跳过此文件"""
    skip_patterns = [
        ".example",
        ".template",
        ".sample",
        ".gitignore",
        ".git/",
        "node_modules/",
        "__pycache__/",
        ".pyc",
        ".log",
    ]
    return any(pattern in filepath for pattern in skip_patterns)


def scan_file(filepath):
    """扫描文件中的敏感信息"""
    if not os.path.isfile(filepath):
        return []
    
    found_secrets = []
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        for secret_type, pattern in SECRET_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                found_secrets.append({
                    "file": filepath,
                    "type": secret_type,
                    "count": len(matches),
                    "matches": matches[:5],  # 只显示前 5 个匹配
                })
    except Exception as e:
        print(f"⚠️  读取文件失败：{filepath} - {e}")
    
    return found_secrets


def redact_file(filepath):
    """替换文件中的敏感信息"""
    if not os.path.isfile(filepath):
        return False
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        original_content = content
        replaced_count = 0
        
        for secret_type, pattern in SECRET_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                for match in matches:
                    # 替换为指代符号
                    redacted = REDACTED_FORMAT.format(secret_type)
                    content = content.replace(match, redacted, 1)
                    replaced_count += 1
        
        if replaced_count > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 已替换 {filepath} 中的 {replaced_count} 个敏感信息")
            return True
        
        return False
    except Exception as e:
        print(f"❌ 处理文件失败：{filepath} - {e}")
        return False


def main():
    print("🔒 安全扫描：检查敏感信息...")
    print("=" * 60)
    
    # 获取暂存的文件
    staged_files = get_staged_files()
    
    if not staged_files:
        print("✅ 没有暂存的文件")
        sys.exit(0)
    
    print(f"📁 检查 {len(staged_files)} 个文件...")
    
    all_secrets = []
    
    # 扫描每个文件
    for filepath in staged_files:
        if should_skip_file(filepath):
            continue
        
        secrets = scan_file(filepath)
        all_secrets.extend(secrets)
    
    # 报告结果
    if all_secrets:
        print()
        print("🚨 发现敏感信息！")
        print("=" * 60)
        
        for secret in all_secrets:
            print(f"❌ {secret['file']}")
            print(f"   类型：{secret['type']}")
            print(f"   数量：{secret['count']}")
            print(f"   示例：{secret['matches'][:3]}")
            print()
        
        print("=" * 60)
        print()
        print("🛑 提交被阻止！")
        print()
        print("✅ 解决方案：")
        print("  1. 使用环境变量：os.environ.get('API_KEY')")
        print("  2. 将敏感文件添加到 .gitignore")
        print("  3. 使用 .env.example 作为模板")
        print()
        print("📝 示例代码：")
        print("  ❌ 错误：API_KEY = \"sk-xxxxx\"")
        print("  ✅ 正确：API_KEY = os.environ.get('API_KEY')")
        print()
        
        # 询问是否自动替换
        response = input("是否自动替换敏感信息为 [REDACTED]？(y/n): ")
        if response.lower() == 'y':
            print()
            print("🔄 开始替换...")
            for secret in all_secrets:
                redact_file(secret['file'])
            
            print()
            print("✅ 替换完成！请重新添加文件并提交：")
            print(f"   git add {' '.join(set(s['file'] for s in all_secrets))}")
            print("   git commit")
        else:
            print()
            print("⚠️  请手动移除敏感信息后重新提交")
        
        sys.exit(1)
    else:
        print("✅ 安全扫描通过 - 未发现敏感信息")
        sys.exit(0)


if __name__ == "__main__":
    main()
