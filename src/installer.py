"""Claude Code 安装模块"""

import subprocess
from rich.console import Console
from rich.prompt import Confirm, Prompt
from .utils import (
    get_os_type,
    check_command_exists,
    run_command,
    print_success,
    print_error,
    print_warning,
    print_info
)

console = Console()

# 国内 npm 镜像源
NPM_MIRRORS = {
    "淘宝镜像 (推荐)": "https://registry.npmmirror.com",
    "阿里云镜像": "https://npm.aliyun.com",
    "腾讯云镜像": "https://mirrors.cloud.tencent.com/npm",
    "华为云镜像": "https://repo.huaweicloud.com/repository/npm/",
    "官方源 (需要VPN)": "https://registry.npmjs.org"
}


class ClaudeCodeInstaller:
    """Claude Code 安装器"""

    def __init__(self):
        self.os_type = get_os_type()
        self.npm_mirror = None

    def check_nodejs(self) -> bool:
        """检查 Node.js 是否已安装"""
        return check_command_exists("node")

    def check_npm(self) -> bool:
        """检查 npm 是否已安装"""
        return check_command_exists("npm")

    def get_node_version(self) -> str:
        """获取 Node.js 版本"""
        try:
            result = run_command(["node", "--version"], check=False)
            return result.stdout.strip()
        except Exception:
            return "未安装"

    def get_npm_version(self) -> str:
        """获取 npm 版本"""
        try:
            result = run_command(["npm", "--version"], check=False)
            return result.stdout.strip()
        except Exception:
            return "未安装"

    def install_nodejs(self) -> bool:
        """安装 Node.js"""
        print_info("正在安装 Node.js...")

        if self.os_type == "windows":
            print_warning("Windows 系统请手动安装 Node.js:")
            print()
            print_info("下载地址（任选其一）:")
            print("  1. 官方网站: https://nodejs.org (可能需要 VPN)")
            print("  2. 国内镜像: https://npmmirror.com/mirrors/node/")
            print("  3. 腾讯镜像: https://mirrors.cloud.tencent.com/nodejs-release/")
            print()
            print_info("推荐使用国内镜像下载，无需 VPN")
            print_info("安装完成后重新运行此程序")
            return False

        elif self.os_type == "macos":
            if check_command_exists("brew"):
                print_info("使用 Homebrew 安装 Node.js...")
                try:
                    run_command(["brew", "install", "node@18"])
                    print_success("Node.js 安装成功")
                    return True
                except Exception as e:
                    print_error(f"Node.js 安装失败: {e}")
                    return False
            else:
                print_warning("请先安装 Homebrew:")
                print_info('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
                return False

        elif self.os_type == "linux":
            print_info("使用包管理器安装 Node.js...")
            try:
                # 尝试使用 apt (Debian/Ubuntu)
                run_command(["sudo", "apt", "update"])
                run_command(["sudo", "apt", "install", "-y", "nodejs", "npm"])
                print_success("Node.js 安装成功")
                return True
            except Exception:
                try:
                    # 尝试使用 yum (CentOS/RHEL)
                    run_command(["sudo", "yum", "install", "-y", "nodejs", "npm"])
                    print_success("Node.js 安装成功")
                    return True
                except Exception as e:
                    print_error(f"Node.js 安装失败: {e}")
                    print_info("请手动安装 Node.js 18+: https://nodejs.org")
                    return False

        return False

    def select_npm_mirror(self) -> str:
        """选择 npm 镜像源"""
        print_info("选择 npm 镜像源（国内用户推荐使用镜像）:")
        print()

        mirrors = list(NPM_MIRRORS.keys())
        for i, name in enumerate(mirrors, 1):
            url = NPM_MIRRORS[name]
            print(f"  {i}. {name}")
            print(f"     {url}")
            print()

        choice = Prompt.ask(
            "请选择镜像源",
            choices=[str(i) for i in range(1, len(mirrors) + 1)],
            default="1"
        )

        selected_name = mirrors[int(choice) - 1]
        selected_url = NPM_MIRRORS[selected_name]
        print_success(f"已选择: {selected_name}")
        return selected_url

    def check_claude_code(self) -> bool:
        """检查 Claude Code 是否已安装"""
        return check_command_exists("claude")

    def install_claude_code(self) -> bool:
        """安装 Claude Code"""
        print_info("正在安装 Claude Code...")

        if not self.check_npm():
            print_error("npm 未安装，请先安装 Node.js")
            return False

        # 选择镜像源
        if not self.npm_mirror:
            self.npm_mirror = self.select_npm_mirror()

        try:
            # 使用指定镜像源安装（使用列表避免 shell=True）
            print_info(f"使用镜像源: {self.npm_mirror}")
            run_command([
                "npm", "install", "-g", "@anthropic-ai/claude-code",
                f"--registry={self.npm_mirror}"
            ])
            print_success("Claude Code 安装成功")
            return True
        except Exception as e:
            print_error(f"Claude Code 安装失败: {e}")
            print_warning("如果安装失败，请尝试:")
            print_info("1. 选择其他镜像源")
            print_info("2. 检查网络连接")
            return False

    def verify_installation(self) -> bool:
        """验证 Claude Code 安装"""
        if not self.check_claude_code():
            return False

        try:
            result = run_command(["claude", "--version"], check=False)
            if result.returncode == 0:
                print_success(f"Claude Code 版本: {result.stdout.strip()}")
                return True
        except Exception:
            pass

        return False

    def install(self) -> bool:
        """执行完整安装流程"""
        console.print("\n[bold blue]=== Claude Code 安装向导 ===[/bold blue]\n")

        # 检查 Node.js
        if not self.check_nodejs():
            print_warning("Node.js 未安装")
            if Confirm.ask("是否自动安装 Node.js?"):
                if not self.install_nodejs():
                    return False
            else:
                print_info("请手动安装 Node.js 18+ 后重试")
                return False
        else:
            print_success(f"Node.js 已安装: {self.get_node_version()}")

        # 检查 npm
        if not self.check_npm():
            print_error("npm 未安装")
            return False
        else:
            print_success(f"npm 已安装: {self.get_npm_version()}")

        # 检查 Claude Code
        if self.check_claude_code():
            print_success("Claude Code 已安装")
            if not Confirm.ask("是否重新安装?"):
                return True

        # 安装 Claude Code
        if not self.install_claude_code():
            return False

        # 验证安装
        if not self.verify_installation():
            print_warning("安装验证失败，但安装可能已完成")
            print_info("请尝试运行 'claude --version' 验证")

        return True
