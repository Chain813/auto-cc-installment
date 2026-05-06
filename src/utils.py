"""工具函数模块"""

import platform
import subprocess
import shutil
import sys
from pathlib import Path
from typing import List
from rich.console import Console

# 修复 Windows 终端编码（跳过 pytest，避免破坏其 capture 机制）
if sys.platform == "win32" and "_pytest" not in sys.modules:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

console = Console()


def get_os_type() -> str:
    """获取操作系统类型"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"


def check_command_exists(command: str) -> bool:
    """检查命令是否存在"""
    return shutil.which(command) is not None


def run_command(command: List[str], check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess:
    """
    安全地运行系统命令

    Args:
        command: 命令列表（避免 shell=True 的安全风险）
        check: 是否检查返回码
        capture_output: 是否捕获输出
    """
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]命令执行失败: {' '.join(command)}[/red]")
        console.print(f"[red]错误信息: {e.stderr}[/red]")
        raise


def run_command_safe(command: str, check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess:
    """
    运行命令（兼容旧调用方式，但内部使用列表）

    注意：此函数会将命令按空格分割，不适用于包含空格参数的命令
    """
    cmd_list = command.split()
    return run_command(cmd_list, check, capture_output)


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def get_config_dir() -> Path:
    """获取配置目录"""
    config_dir = get_project_root() / "config"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_path() -> Path:
    """获取配置文件路径"""
    return get_config_dir() / "config.yaml"


def mask_sensitive(value: str, show_chars: int = 4) -> str:
    """遮蔽敏感信息"""
    if not value or len(value) <= show_chars * 2:
        return "***"
    return f"{value[:show_chars]}...{value[-show_chars:]}"


def print_success(message: str):
    """打印成功信息"""
    console.print(f"[green]✓ {message}[/green]")


def print_error(message: str):
    """打印错误信息"""
    console.print(f"[red]✗ {message}[/red]")


def print_warning(message: str):
    """打印警告信息"""
    console.print(f"[yellow]⚠ {message}[/yellow]")


def print_info(message: str):
    """打印信息"""
    console.print(f"[blue]ℹ {message}[/blue]")
