#!/usr/bin/env python3
"""CLI 一键安装脚本 - 替代原 install.bat 中的逻辑"""

import sys
import os
import platform
import shutil
import subprocess

# 确保项目根目录在 sys.path 中
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def print_banner():
    """打印欢迎横幅"""
    print()
    print("  ############################################")
    print("  #                                          #")
    print("  #      Claude Code + DeepSeek API          #")
    print("  #           一 键 安 装 工 具              #")
    print("  #                                          #")
    print("  ############################################")
    print()
    print("  无需 VPN，国内直连")
    print()
    print("=" * 48)
    print()


def check_command(cmd, args=None):
    """检查命令是否可用并返回版本"""
    if not shutil.which(cmd):
        return False, ""
    try:
        cmd_list = [cmd, args] if args else [cmd]
        result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""


def step_check_python():
    """Step 1: 检查 Python"""
    print("[1/5] 检查 Python...")
    version = platform.python_version()
    print(f"      Python {version} - OK")
    print()
    return True


def step_check_deps():
    """Step 2: 检查/安装 Python 依赖"""
    print("[2/5] 检查 Python 依赖...")
    try:
        import yaml, requests, rich, click, openai  # noqa: F401
        print("      依赖已就绪 - OK")
    except ImportError:
        print("      正在安装依赖...")
        req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "-r", req_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            # 尝试 --user 安装
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--user", "-r", req_path],
                capture_output=True, text=True
            )
        if result.returncode != 0:
            print("      [错误] 依赖安装失败，请检查网络连接")
            return False
        print("      依赖安装完成 - OK")
    print()
    return True


def step_check_nodejs():
    """Step 3: 检查/安装 Node.js"""
    print("[3/5] 检查 Node.js...")
    ok, version = check_command("node", "--version")
    if ok:
        print(f"      Node.js {version} - OK")
        print()
        return True

    print("      Node.js 未安装，尝试自动安装...")

    if platform.system() == "Windows":
        # 尝试 winget
        if shutil.which("winget"):
            print("      使用 winget 安装 Node.js LTS...")
            result = subprocess.run(
                ["winget", "install", "OpenJS.NodeJS.LTS",
                 "--accept-package-agreements", "--accept-source-agreements"],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print("      Node.js 安装完成 - OK")
                print()
                print("  [提示] Node.js 刚安装完成，PATH 可能未刷新")
                print("  请关闭此窗口，重新打开运行本脚本")
                return False

        # 尝试 choco
        if shutil.which("choco"):
            print("      使用 Chocolatey 安装 Node.js...")
            result = subprocess.run(
                ["choco", "install", "nodejs-lts", "-y"],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print("      Node.js 安装完成 - OK")
                print()
                print("  [提示] 请关闭此窗口，重新打开运行本脚本")
                return False

    print()
    print("  [错误] 自动安装失败，请手动安装 Node.js 18+")
    print("  国内镜像下载: https://npmmirror.com/mirrors/node/")
    print("  安装后重新运行本脚本")
    return False


def step_check_claude():
    """Step 4: 检查/安装 Claude Code"""
    print("[4/5] 检查 Claude Code...")
    ok, version = check_command("claude", "--version")
    if ok:
        print(f"      Claude Code {version} - OK")
        print()
        return True

    print("      Claude Code 未安装，正在通过 npm 安装...")
    print("      使用淘宝镜像，无需 VPN")

    result = subprocess.run(
        ["npm", "install", "-g", "@anthropic-ai/claude-code",
         "--registry=https://registry.npmmirror.com"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print()
        print("  [错误] Claude Code 安装失败")
        print("  请检查网络连接后重试")
        return False

    print("      Claude Code 安装完成 - OK")
    print()
    return True


def step_configure_api():
    """Step 5: 配置 DeepSeek API"""
    print("[5/5] 配置 DeepSeek API...")
    print()
    print("  请输入你的 DeepSeek API Key")
    print("  获取地址: https://platform.deepseek.com")
    print()

    try:
        api_key = input("  API Key: ").strip()
    except (EOFError, KeyboardInterrupt):
        api_key = ""

    if not api_key:
        print()
        print("  [警告] 未输入 API Key，跳过配置")
        print("  稍后可运行: python -m src.main configure")
        return True

    # 保存配置
    try:
        import yaml
        config_dir = os.path.join(PROJECT_ROOT, "config")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.yaml")
        config = {
            "deepseek": {
                "api_key": api_key,
                "base_url_openai": "https://api.deepseek.com/v1",
                "base_url_anthropic": "https://api.deepseek.com/anthropic",
                "model": "deepseek-v4-flash"
            },
            "claude_code": {
                "base_url": "https://api.deepseek.com/anthropic",
                "model": "deepseek-v4-flash"
            }
        }
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        print(f"      配置已保存: {config_path}")
    except Exception as e:
        print(f"      [警告] 配置保存失败: {e}")

    # 测试连接
    print()
    print("      测试 API 连接...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print("      API 连接成功 - OK")
    except Exception:
        print("      [警告] API 连接测试失败，请检查 Key 是否正确")

    return True


def print_summary():
    """打印安装完成信息"""
    print()
    print("=" * 48)
    print()
    print("  安装完成！")
    print()
    print("  使用方法:")
    print("    1. 设置环境变量:  python -m src.main setup-env")
    print("    2. 启动 Claude:   claude")
    print()
    print("  其他命令:")
    print("    python -m src.main chat          交互式聊天")
    print("    python -m src.main chat --auto-model  智能模型聊天")
    print("    python -m src.main show          查看配置")
    print("    python -m src.main status        系统状态")
    print("    python launcher.py               GUI 界面")
    print()
    print("=" * 48)
    print()


def main():
    # 设置控制台编码
    if sys.platform == "win32":
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass

    print_banner()

    if not step_check_python():
        return
    if not step_check_deps():
        return
    if not step_check_nodejs():
        return
    if not step_check_claude():
        return
    step_configure_api()
    print_summary()


if __name__ == "__main__":
    main()
