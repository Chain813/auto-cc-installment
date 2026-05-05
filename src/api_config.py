"""API 配置管理模块"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .utils import get_config_path, print_success, print_error, print_info

console = Console()


class APIConfig:
    """API 配置管理器"""

    DEFAULT_CONFIG = {
        "deepseek": {
            "api_key": "",
            "base_url_openai": "https://api.deepseek.com/v1",
            "base_url_anthropic": "https://api.deepseek.com/anthropic",
            "model": "deepseek-v4-flash",
            "models": {
                "flash": "deepseek-v4-flash",
                "pro": "deepseek-v4-pro"
            }
        },
        "claude_code": {
            "base_url": "https://api.deepseek.com/anthropic",
            "model": "deepseek-v4-flash"
        },
        "claude": {
            "install_path": "",
            "auto_update": True
        },
        "npm": {
            "registry": "https://registry.npmmirror.com"
        },
        "general": {
            "log_level": "INFO",
            "timeout": 30,
            "max_retries": 3
        }
    }

    def __init__(self):
        self.config_path = get_config_path()
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if config is None:
                    return self.DEFAULT_CONFIG.copy()
                return config
        except Exception as e:
            print_error(f"配置文件加载失败: {e}")
            return self.DEFAULT_CONFIG.copy()

    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print_success(f"配置已保存到: {self.config_path}")
            return True
        except Exception as e:
            print_error(f"配置保存失败: {e}")
            return False

    def get_deepseek_config(self) -> Dict[str, Any]:
        """获取 DeepSeek 配置"""
        return self.config.get("deepseek", {})

    def get_api_key(self) -> Optional[str]:
        """获取 DeepSeek API Key"""
        # 优先从环境变量获取
        env_key = os.environ.get("DEEPSEEK_API_KEY")
        if env_key:
            return env_key

        return self.config.get("deepseek", {}).get("api_key")

    def set_api_key(self, api_key: str):
        """设置 DeepSeek API Key"""
        if "deepseek" not in self.config:
            self.config["deepseek"] = {}
        self.config["deepseek"]["api_key"] = api_key

    def get_base_url(self, api_type: str = "openai") -> str:
        """获取 DeepSeek Base URL

        Args:
            api_type: API 类型，'openai' 或 'anthropic'
        """
        deepseek = self.config.get("deepseek", {})
        if api_type == "anthropic":
            return deepseek.get("base_url_anthropic", "https://api.deepseek.com/anthropic")
        return deepseek.get("base_url_openai", "https://api.deepseek.com/v1")

    def get_model(self) -> str:
        """获取 DeepSeek 模型名称"""
        return self.config.get("deepseek", {}).get("model", "deepseek-v4-flash")

    def get_claude_code_config(self) -> Dict[str, Any]:
        """获取 Claude Code 配置"""
        return self.config.get("claude_code", {
            "base_url": "https://api.deepseek.com/anthropic",
            "model": "deepseek-v4-flash"
        })

    def get_npm_registry(self) -> str:
        """获取 npm 镜像源"""
        return self.config.get("npm", {}).get("registry", "https://registry.npmmirror.com")

    def configure_interactive(self):
        """交互式配置"""
        console.print("\n[bold blue]=== API 配置向导 ===[/bold blue]\n")

        # DeepSeek API Key
        current_key = self.get_api_key()
        if current_key:
            masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
            print_info(f"当前 API Key: {masked_key}")

        api_key = Prompt.ask(
            "请输入 DeepSeek API Key",
            default="",
            show_default=False
        )

        if api_key:
            self.set_api_key(api_key)

        # Model
        current_model = self.get_model()
        model = Prompt.ask(
            "请选择模型",
            choices=["deepseek-v4-flash", "deepseek-v4-pro"],
            default=current_model
        )
        self.config["deepseek"]["model"] = model

        # 保存配置
        if Confirm.ask("是否保存配置?", default=True):
            self.save_config()
        else:
            print_info("配置未保存")

    def show_config(self):
        """显示当前配置"""
        console.print("\n[bold blue]=== 当前配置 ===[/bold blue]\n")

        # DeepSeek 配置
        deepseek = self.get_deepseek_config()
        api_key = self.get_api_key()

        if api_key:
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        else:
            masked_key = "未设置"

        console.print(f"[bold]DeepSeek API 配置:[/bold]")
        console.print(f"  API Key: {masked_key}")
        console.print(f"  OpenAI 端点: {deepseek.get('base_url_openai', '未设置')}")
        console.print(f"  Anthropic 端点: {deepseek.get('base_url_anthropic', '未设置')}")
        console.print(f"  模型: {deepseek.get('model', '未设置')}")

        # Claude Code 配置
        claude_code = self.get_claude_code_config()
        console.print(f"\n[bold]Claude Code 接入配置:[/bold]")
        console.print(f"  Anthropic 端点: {claude_code.get('base_url', '未设置')}")
        console.print(f"  模型: {claude_code.get('model', '未设置')}")

        # Claude 安装配置
        claude = self.config.get("claude", {})
        console.print(f"\n[bold]Claude Code 安装配置:[/bold]")
        console.print(f"  安装路径: {claude.get('install_path', '默认')}")
        console.print(f"  自动更新: {'是' if claude.get('auto_update', True) else '否'}")

        # npm 配置
        npm = self.config.get("npm", {})
        console.print(f"\n[bold]npm 镜像配置:[/bold]")
        console.print(f"  镜像源: {npm.get('registry', 'https://registry.npmmirror.com')}")

        # 通用配置
        general = self.config.get("general", {})
        console.print(f"\n[bold]通用配置:[/bold]")
        console.print(f"  日志级别: {general.get('log_level', 'INFO')}")
        console.print(f"  超时时间: {general.get('timeout', 30)}秒")
        console.print(f"  最大重试: {general.get('max_retries', 3)}次")
