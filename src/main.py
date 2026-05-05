"""主程序入口"""

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from .installer import ClaudeCodeInstaller
from .api_config import APIConfig
from .deepseek_client import DeepSeekClient
from .utils import print_success, print_error, print_info, print_warning

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="claude-deepseek")
def cli():
    """Claude Code 自动化安装 + DeepSeek API 接入工具"""
    pass


@cli.command()
def install():
    """安装 Claude Code"""
    installer = ClaudeCodeInstaller()
    success = installer.install()
    if success:
        print_success("\n安装完成！")
        print_info("运行 'claude' 启动 Claude Code")
    else:
        print_error("\n安装失败")
        raise click.Abort()


@cli.command()
def configure():
    """配置 DeepSeek API"""
    config = APIConfig()
    config.configure_interactive()


@cli.command("setup-env")
def setup_env():
    """一键设置环境变量（当前终端会话）"""
    config = APIConfig()
    api_key = config.get_api_key()

    if not api_key:
        print_error("请先配置 DeepSeek API Key")
        print_info("运行 'python -m src.main configure' 进行配置")
        raise click.Abort()

    claude_code_config = config.get_claude_code_config()
    base_url = claude_code_config.get("base_url", "https://api.deepseek.com/anthropic")
    model = claude_code_config.get("model", "deepseek-v4-flash")

    console.print("\n[bold blue]=== 一键设置环境变量 ===[/bold blue]\n")

    # 设置环境变量
    os.environ["ANTHROPIC_API_KEY"] = api_key
    os.environ["ANTHROPIC_BASE_URL"] = base_url

    print_success("环境变量已设置:")
    print_info(f"  ANTHROPIC_API_KEY = {api_key[:8]}...{api_key[-4:]}")
    print_info(f"  ANTHROPIC_BASE_URL = {base_url}")
    print_info(f"  默认模型 = {model}")

    print()
    print_warning("注意: 环境变量仅在当前终端会话有效")
    print_info("如需永久配置，请运行: python -m src.main configure-claude-code")

    # 测试连接
    print()
    if Confirm.ask("是否测试 API 连接?", default=True):
        from openai import OpenAI
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            print_success("API 连接测试成功!")
        except Exception as e:
            print_error(f"API 连接测试失败: {e}")


@cli.command("configure-claude-code")
def configure_claude_code():
    """配置 Claude Code 使用 DeepSeek API"""
    config = APIConfig()
    api_key = config.get_api_key()

    if not api_key:
        print_error("请先配置 DeepSeek API Key")
        print_info("运行 'python -m src.main configure' 进行配置")
        raise click.Abort()

    console.print("\n[bold blue]=== 配置 Claude Code 使用 DeepSeek API ===[/bold blue]\n")

    claude_code_config = config.get_claude_code_config()
    base_url = claude_code_config.get("base_url", "https://api.deepseek.com/anthropic")
    model = claude_code_config.get("model", "deepseek-v4-flash")

    print_info(f"Anthropic 端点: {base_url}")
    print_info(f"模型: {model}")
    print()

    # 显示配置命令
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print_info(f"当前 API Key: {masked_key}")
    print_info("请在终端中运行以下命令配置 Claude Code:")
    print()

    if os.name == "nt":  # Windows
        console.print("[bold green]PowerShell:[/bold green]")
        console.print('  $env:ANTHROPIC_API_KEY = "your-deepseek-api-key"')
        console.print(f'  $env:ANTHROPIC_BASE_URL = "{base_url}"')
        console.print(f'  claude --model {model}')
        print()
        console.print("[bold green]CMD:[/bold green]")
        console.print('  set ANTHROPIC_API_KEY=your-deepseek-api-key')
        console.print(f'  set ANTHROPIC_BASE_URL={base_url}')
        console.print(f'  claude --model {model}')
    else:  # Linux/macOS
        console.print("[bold green]Bash/Zsh:[/bold green]")
        console.print('  export ANTHROPIC_API_KEY="your-deepseek-api-key"')
        console.print(f'  export ANTHROPIC_BASE_URL="{base_url}"')
        console.print(f'  claude --model {model}')

    print()
    print_warning("注意: 这些环境变量仅在当前终端会话有效")
    print_info("如需永久配置，请将上述命令添加到 shell 配置文件")

    # 询问是否创建启动脚本
    if Confirm.ask("\n是否创建启动脚本?", default=True):
        # 创建启动脚本（使用环境变量，不硬编码 API Key）
        if os.name == "nt":
            script_content = f'''@echo off
REM Claude Code with DeepSeek API 启动脚本
REM 注意: 请先运行 setup-env 命令设置环境变量，或手动设置

echo Claude Code + DeepSeek API
echo.
echo 请确保已运行: python -m src.main setup-env
echo 或手动设置以下环境变量:
echo   ANTHROPIC_API_KEY
echo   ANTHROPIC_BASE_URL={base_url}
echo.
echo 正在启动 Claude Code (模型: {model})...
claude --model {model}
'''
            script_path = "start_claude_deepseek.bat"
        else:
            script_content = f'''#!/bin/bash
# Claude Code with DeepSeek API 启动脚本
# 注意: 请先运行 setup-env 命令设置环境变量，或手动设置

echo "Claude Code + DeepSeek API"
echo ""
echo "请确保已运行: python -m src.main setup-env"
echo "或手动设置以下环境变量:"
echo "  ANTHROPIC_API_KEY"
echo "  ANTHROPIC_BASE_URL={base_url}"
echo ""
echo "正在启动 Claude Code (模型: {model})..."
claude --model {model}
'''
            script_path = "start_claude_deepseek.sh"

        with open(script_path, "w") as f:
            f.write(script_content)
        print_success(f"启动脚本已创建: {script_path}")
        print_warning("注意: 脚本不再包含 API Key，请先运行 setup-env 设置环境变量")


@cli.command()
def show():
    """显示当前配置"""
    config = APIConfig()
    config.show_config()


@cli.command()
def test():
    """测试 API 连接"""
    config = APIConfig()
    client = DeepSeekClient(config)
    success = client.test_connection()
    if not success:
        raise click.Abort()


@cli.command()
@click.option('--auto-model', is_flag=True, default=False, help='启用智能模型选择')
def chat(auto_model):
    """启动交互式聊天"""
    config = APIConfig()
    client = DeepSeekClient(config)

    if auto_model:
        # 使用智能模型选择
        console.print("\n[bold blue]=== 智能模型选择已启用 ===[/bold blue]")
        print_info("将根据任务复杂度自动选择 flash/pro 模型\n")
        client.interactive_chat_with_auto_model()
    else:
        client.interactive_chat()


@cli.command()
def status():
    """显示系统状态"""
    installer = ClaudeCodeInstaller()
    config = APIConfig()

    console.print("\n[bold blue]=== 系统状态 ===[/bold blue]\n")

    # Node.js 状态
    if installer.check_nodejs():
        print_success(f"Node.js: {installer.get_node_version()}")
    else:
        print_error("Node.js: 未安装")

    # npm 状态
    if installer.check_npm():
        print_success(f"npm: {installer.get_npm_version()}")
    else:
        print_error("npm: 未安装")

    # Claude Code 状态
    if installer.check_claude_code():
        print_success("Claude Code: 已安装")
    else:
        print_error("Claude Code: 未安装")

    # API 配置状态
    api_key = config.get_api_key()
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print_success(f"DeepSeek API Key: {masked_key}")
    else:
        print_error("DeepSeek API Key: 未配置")


def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold]Claude Code + DeepSeek API 工具[/bold]\n"
        "自动化安装和配置\n"
        "[dim]无需 VPN，直连使用[/dim]",
        title="欢迎",
        border_style="blue"
    ))
    cli()


if __name__ == "__main__":
    main()
