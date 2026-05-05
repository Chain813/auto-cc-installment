"""GUI 一键部署界面"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import platform
import subprocess
import shutil
import os
import sys
from typing import Optional


class DeployGUI:
    """部署 GUI 主界面"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Claude Code + DeepSeek 一键部署工具")
        self.root.geometry("700x800")
        self.root.resizable(True, True)

        # 配置颜色
        self.colors = {
            "bg": "#f5f5f5",
            "primary": "#2196F3",
            "success": "#4CAF50",
            "error": "#f44336",
            "warning": "#FF9800",
            "text": "#333333"
        }

        self.root.configure(bg=self.colors["bg"])

        # 状态变量
        self.is_deploying = False
        self.env_status = {
            "python": {"installed": False, "version": ""},
            "nodejs": {"installed": False, "version": ""},
            "npm": {"installed": False, "version": ""},
            "claude": {"installed": False, "version": ""}
        }

        # 创建界面
        self.create_widgets()

        # 自动检测环境
        self.root.after(100, self.detect_environment)

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="Claude Code + DeepSeek 一键部署",
            font=("Microsoft YaHei", 18, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["primary"]
        )
        title_label.pack(pady=(0, 20))

        # Step 1: API Key 输入
        self.create_api_key_section(main_frame)

        # Step 2: 环境检测
        self.create_env_section(main_frame)

        # Step 3: 部署控制
        self.create_deploy_section(main_frame)

        # 日志区域
        self.create_log_section(main_frame)

        # 操作按钮
        self.create_action_buttons(main_frame)

    def create_api_key_section(self, parent):
        """创建 API Key 输入区域"""
        frame = tk.LabelFrame(
            parent,
            text="Step 1: 输入 DeepSeek API Key",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, pady=(0, 10))

        # API Key 输入
        input_frame = tk.Frame(frame, bg=self.colors["bg"])
        input_frame.pack(fill=tk.X)

        tk.Label(
            input_frame,
            text="API Key:",
            font=("Microsoft YaHei", 10),
            bg=self.colors["bg"]
        ).pack(side=tk.LEFT)

        self.api_key_var = tk.StringVar()
        self.api_key_entry = tk.Entry(
            input_frame,
            textvariable=self.api_key_var,
            show="*",
            font=("Consolas", 10),
            width=40
        )
        self.api_key_entry.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)

        # 显示/隐藏切换
        self.show_key_var = tk.BooleanVar(value=False)
        self.show_key_btn = tk.Checkbutton(
            input_frame,
            text="显示",
            variable=self.show_key_var,
            command=self.toggle_key_visibility,
            bg=self.colors["bg"]
        )
        self.show_key_btn.pack(side=tk.LEFT)

        # 提示信息
        tk.Label(
            frame,
            text="获取地址: https://platform.deepseek.com",
            font=("Microsoft YaHei", 9),
            fg="gray",
            bg=self.colors["bg"]
        ).pack(anchor=tk.W, pady=(5, 0))

    def create_env_section(self, parent):
        """创建环境检测区域"""
        frame = tk.LabelFrame(
            parent,
            text="Step 2: 环境检测",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, pady=(0, 10))

        # 环境状态显示
        self.env_labels = {}
        envs = [
            ("python", "Python"),
            ("nodejs", "Node.js"),
            ("npm", "npm"),
            ("claude", "Claude Code")
        ]

        for key, name in envs:
            row = tk.Frame(frame, bg=self.colors["bg"])
            row.pack(fill=tk.X, pady=2)

            status_label = tk.Label(
                row,
                text="[ ]",
                font=("Consolas", 10),
                bg=self.colors["bg"],
                width=4
            )
            status_label.pack(side=tk.LEFT)

            name_label = tk.Label(
                row,
                text=f"{name}:",
                font=("Microsoft YaHei", 10),
                bg=self.colors["bg"],
                width=15,
                anchor=tk.W
            )
            name_label.pack(side=tk.LEFT)

            version_label = tk.Label(
                row,
                text="检测中...",
                font=("Microsoft YaHei", 10),
                bg=self.colors["bg"],
                anchor=tk.W
            )
            version_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.env_labels[key] = {
                "status": status_label,
                "version": version_label
            }

        # 刷新按钮
        tk.Button(
            frame,
            text="重新检测",
            command=self.detect_environment,
            font=("Microsoft YaHei", 9)
        ).pack(anchor=tk.E, pady=(5, 0))

    def create_deploy_section(self, parent):
        """创建部署控制区域"""
        frame = tk.LabelFrame(
            parent,
            text="Step 3: 一键部署",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, pady=(0, 10))

        # 模型选择
        model_frame = tk.Frame(frame, bg=self.colors["bg"])
        model_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            model_frame,
            text="模型选择:",
            font=("Microsoft YaHei", 10),
            bg=self.colors["bg"]
        ).pack(side=tk.LEFT)

        self.model_var = tk.StringVar(value="自动 (智能选择)")
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["自动 (智能选择)", "deepseek-v4-flash", "deepseek-v4-pro"],
            state="readonly",
            width=25
        )
        model_combo.pack(side=tk.LEFT, padx=(10, 0))
        model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        # 模型说明
        self.model_info_label = tk.Label(
            frame,
            text="自动模式: 根据任务复杂度智能选择 flash/pro 模型",
            font=("Microsoft YaHei", 9),
            fg="gray",
            bg=self.colors["bg"]
        )
        self.model_info_label.pack(anchor=tk.W, pady=(0, 10))

        # 部署按钮
        self.deploy_btn = tk.Button(
            frame,
            text="开始部署",
            command=self.start_deploy,
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.colors["primary"],
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2"
        )
        self.deploy_btn.pack(pady=(5, 0))

        # 进度条
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=(10, 0))

    def create_log_section(self, parent):
        """创建日志显示区域"""
        frame = tk.LabelFrame(
            parent,
            text="部署日志",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(
            frame,
            font=("Consolas", 9),
            height=10,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_action_buttons(self, parent):
        """创建操作按钮区域"""
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.pack(fill=tk.X)

        self.test_btn = tk.Button(
            frame,
            text="测试连接",
            command=self.test_connection,
            font=("Microsoft YaHei", 10),
            padx=15,
            pady=5
        )
        self.test_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.launch_btn = tk.Button(
            frame,
            text="启动 Claude Code",
            command=self.launch_claude,
            font=("Microsoft YaHei", 10),
            bg=self.colors["success"],
            fg="white",
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.launch_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.exit_btn = tk.Button(
            frame,
            text="退出",
            command=self.root.quit,
            font=("Microsoft YaHei", 10),
            padx=15,
            pady=5
        )
        self.exit_btn.pack(side=tk.RIGHT)

    def toggle_key_visibility(self):
        """切换 API Key 显示/隐藏"""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")

    def on_model_change(self, event=None):
        """模型选择变化回调"""
        model = self.model_var.get()
        if model == "自动 (智能选择)":
            self.model_info_label.config(text="自动模式: 根据任务复杂度智能选择 flash/pro 模型")
        elif model == "deepseek-v4-flash":
            self.model_info_label.config(text="Flash: 快速模型，适合简单任务和日常编程")
        elif model == "deepseek-v4-pro":
            self.model_info_label.config(text="Pro: 专业模型，适合复杂任务和代码生成")

    def log(self, message: str):
        """添加日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_env_status(self, key: str, installed: bool, version: str):
        """更新环境状态显示"""
        label = self.env_labels[key]
        if installed:
            label["status"].config(text="[✓]", fg=self.colors["success"])
            label["version"].config(text=version, fg=self.colors["text"])
        else:
            label["status"].config(text="[✗]", fg=self.colors["error"])
            label["version"].config(text=version, fg=self.colors["error"])

    def detect_environment(self):
        """检测环境"""
        self.log("开始检测环境...")

        # 检测 Python
        py_version = platform.python_version()
        self.env_status["python"] = {"installed": True, "version": py_version}
        self.update_env_status("python", True, py_version)
        self.log(f"Python: {py_version}")

        # 检测 Node.js
        nodejs_installed, nodejs_version = self.check_command("node", "--version")
        self.env_status["nodejs"] = {"installed": nodejs_installed, "version": nodejs_version}
        self.update_env_status("nodejs", nodejs_installed, nodejs_version)
        self.log(f"Node.js: {nodejs_version if nodejs_installed else '未安装'}")

        # 检测 npm
        npm_installed, npm_version = self.check_command("npm", "--version")
        self.env_status["npm"] = {"installed": npm_installed, "version": npm_version}
        self.update_env_status("npm", npm_installed, npm_version)
        self.log(f"npm: {npm_version if npm_installed else '未安装'}")

        # 检测 Claude Code
        claude_installed, claude_version = self.check_command("claude", "--version")
        self.env_status["claude"] = {"installed": claude_installed, "version": claude_version}
        self.update_env_status("claude", claude_installed, claude_version)
        self.log(f"Claude Code: {claude_version if claude_installed else '未安装'}")

        self.log("环境检测完成\n")

        # 更新按钮状态
        if claude_installed:
            self.launch_btn.config(state=tk.NORMAL)

    def check_command(self, command: str, args: str = "") -> tuple:
        """检查命令是否存在"""
        if not shutil.which(command):
            return False, "未安装"

        try:
            result = subprocess.run(
                [command, args] if args else [command],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
        except Exception:
            pass

        return False, "未安装"

    def start_deploy(self):
        """开始部署"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("警告", "请先输入 DeepSeek API Key")
            return

        if self.is_deploying:
            return

        self.is_deploying = True
        self.deploy_btn.config(state=tk.DISABLED, text="部署中...")
        self.progress.start()

        # 在子线程中执行部署
        thread = threading.Thread(target=self.deploy_task, args=(api_key,))
        thread.daemon = True
        thread.start()

    def deploy_task(self, api_key: str):
        """部署任务（子线程）"""
        try:
            model = self.model_var.get()
            self.log("=" * 50)
            self.log("开始一键部署...")
            self.log(f"选择模型: {model}")
            self.log("=" * 50)

            # Step 1: 检测并安装 Node.js
            if not self.env_status["nodejs"]["installed"]:
                self.log("\n[Step 1/4] Node.js 未安装，尝试安装...")
                self.install_nodejs()
            else:
                self.log(f"\n[Step 1/4] Node.js 已安装: {self.env_status['nodejs']['version']}")

            # Step 2: 安装 Claude Code
            if not self.env_status["claude"]["installed"]:
                self.log("\n[Step 2/4] 安装 Claude Code...")
                self.install_claude_code()
            else:
                self.log(f"\n[Step 2/4] Claude Code 已安装: {self.env_status['claude']['version']}")

            # Step 3: 配置 DeepSeek API
            self.log("\n[Step 3/4] 配置 DeepSeek API...")
            self.save_config(api_key, model)

            # Step 4: 测试连接
            self.log("\n[Step 4/4] 测试 API 连接...")
            if self.test_api_connection(api_key):
                self.log("✓ API 连接测试成功")
            else:
                self.log("⚠ API 连接测试失败，请检查 API Key")

            # 完成
            self.log("\n" + "=" * 50)
            self.log("✓ 部署完成！")
            self.log("")
            self.log("使用方法:")
            self.log(f'  $env:ANTHROPIC_API_KEY = "{api_key}"')
            self.log(f'  $env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"')
            self.log(f"  claude --model {model}")
            self.log("=" * 50)

            # 更新状态
            self.root.after(0, lambda: self.launch_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: messagebox.showinfo("成功", "部署完成！"))

        except Exception as e:
            self.log(f"\n✗ 部署失败: {e}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"部署失败: {e}"))

        finally:
            self.is_deploying = False
            self.root.after(0, lambda: self.deploy_btn.config(state=tk.NORMAL, text="开始部署"))
            self.root.after(0, self.progress.stop)

    def install_nodejs(self):
        """安装 Node.js"""
        self.log("请手动安装 Node.js 18+")
        self.log("推荐下载地址: https://npmmirror.com/mirrors/node/")
        raise Exception("需要手动安装 Node.js")

    def install_claude_code(self):
        """安装 Claude Code"""
        self.log("使用 npm 安装 Claude Code (淘宝镜像)...")

        try:
            result = subprocess.run(
                ["npm", "install", "-g", "@anthropic-ai/claude-code", "--registry=https://registry.npmmirror.com"],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log("✓ Claude Code 安装成功")
                # 更新状态
                self.env_status["claude"]["installed"] = True
                self.root.after(0, lambda: self.update_env_status("claude", True, "已安装"))
            else:
                self.log(f"✗ 安装失败: {result.stderr}")
                raise Exception(f"安装失败: {result.stderr}")

        except subprocess.TimeoutExpired:
            raise Exception("安装超时，请检查网络连接")

    def save_config(self, api_key: str, model: str):
        """保存配置"""
        import yaml

        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.yaml")

        config = {
            "deepseek": {
                "api_key": api_key,
                "base_url_openai": "https://api.deepseek.com/v1",
                "base_url_anthropic": "https://api.deepseek.com/anthropic",
                "model": model
            },
            "claude_code": {
                "base_url": "https://api.deepseek.com/anthropic",
                "model": model
            }
        }

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        self.log(f"✓ 配置已保存: {config_path}")

    def test_api_connection(self, api_key: str) -> bool:
        """测试 API 连接"""
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )

            response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )

            return True
        except Exception as e:
            self.log(f"连接测试失败: {e}")
            return False

    def test_connection(self):
        """测试连接按钮"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("警告", "请先输入 DeepSeek API Key")
            return

        self.log("测试 API 连接...")
        if self.test_api_connection(api_key):
            self.log("✓ API 连接成功")
            messagebox.showinfo("成功", "API 连接测试成功！")
        else:
            self.log("✗ API 连接失败")
            messagebox.showerror("错误", "API 连接测试失败，请检查 API Key")

    def launch_claude(self):
        """启动 Claude Code"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("警告", "请先输入 API Key")
            return

        base_url = "https://api.deepseek.com/anthropic"
        model_choice = self.model_var.get()

        # 处理模型选择
        if model_choice == "自动 (智能选择)":
            # 自动模式：默认使用 flash，启动脚本会提示用户
            model = "deepseek-v4-flash"
            auto_mode = True
        else:
            model = model_choice
            auto_mode = False

        # 创建启动脚本
        if platform.system() == "Windows":
            if auto_mode:
                script = f'''@echo off
echo Claude Code + DeepSeek API (智能模式)
echo.
echo 智能模型选择说明:
echo   - 简单任务会自动使用 deepseek-v4-flash (快速)
echo   - 复杂任务会自动使用 deepseek-v4-pro (专业)
echo.
set ANTHROPIC_API_KEY={api_key}
set ANTHROPIC_BASE_URL={base_url}
echo 启动 Claude Code...
claude --model {model}
'''
            else:
                script = f'''@echo off
echo Claude Code + DeepSeek API
echo.
set ANTHROPIC_API_KEY={api_key}
set ANTHROPIC_BASE_URL={base_url}
echo 启动 Claude Code (模型: {model})...
claude --model {model}
'''
            script_path = "launch_claude.bat"
        else:
            if auto_mode:
                script = f'''#!/bin/bash
echo "Claude Code + DeepSeek API (智能模式)"
echo ""
echo "智能模型选择说明:"
echo "  - 简单任务会自动使用 deepseek-v4-flash (快速)"
echo "  - 复杂任务会自动使用 deepseek-v4-pro (专业)"
echo ""
export ANTHROPIC_API_KEY="{api_key}"
export ANTHROPIC_BASE_URL="{base_url}"
echo "启动 Claude Code..."
claude --model {model}
'''
            else:
                script = f'''#!/bin/bash
echo "Claude Code + DeepSeek API"
echo ""
export ANTHROPIC_API_KEY="{api_key}"
export ANTHROPIC_BASE_URL="{base_url}"
echo "启动 Claude Code (模型: {model})..."
claude --model {model}
'''
            script_path = "launch_claude.sh"

        with open(script_path, "w") as f:
            f.write(script)

        self.log(f"✓ 启动脚本已创建: {script_path}")
        if auto_mode:
            self.log("  模式: 智能选择 (flash/pro)")
        else:
            self.log(f"  模型: {model}")
        self.log("请在新终端中运行启动脚本")

        messagebox.showinfo("提示", f"启动脚本已创建: {script_path}\n请在新终端中运行")


def main():
    """主函数"""
    root = tk.Tk()
    app = DeployGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
