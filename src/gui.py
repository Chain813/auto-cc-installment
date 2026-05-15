"""GUI 一键部署界面 - 深度优化版"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import platform
import subprocess
import shutil
import os
import time
import tempfile
import atexit


class ToolTip:
    """鼠标悬停提示"""
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def update_text(self, text):
        self.text = text

    def show(self, event=None):
        if not self.text:
            return
        self.hide()
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, bg="#1e293b", fg="#e2e8f0",
                         font=("Microsoft YaHei UI", 9), padx=8, pady=4,
                         relief=tk.SOLID, borderwidth=1)
        label.pack()
        self.tip_window = tw

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class DeployGUI:
    """部署 GUI 主界面"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Claude Code + DeepSeek 一键部署工具 v0.1.0")
        self.root.geometry("800x850")

        self.colors = {
            "bg": "#0B1121",          # 更深的极客蓝黑底色
            "card": "#162032",        # 卡片背景，带微弱蓝调
            "primary": "#3B82F6",     # 亮蓝（部署按钮）
            "accent": "#0ea5e9",      # 天蓝（高亮/装饰）
            "success": "#10B981",     # 翠绿
            "error": "#EF4444",       # 鲜红
            "warning": "#F59E0B",     # 琥珀
            "text": "#F8FAFC",        # 近白文字
            "text_dim": "#94A3B8",    # 灰白辅助文字
            "border": "#1E293B"       # 边框色
        }
        self.font_main = ("Segoe UI", 10)
        self.font_title = ("Segoe UI", 22, "bold")
        self.font_subtitle = ("Segoe UI", 12)
        self.font_bold = ("Segoe UI", 10, "bold")
        self.font_code = ("Consolas", 10)

        self.root.configure(bg=self.colors["bg"])
        self.setup_styles()

        self.is_deploying = False
        self.env_status = {
            "python": {"installed": False, "version": ""},
            "nodejs": {"installed": False, "version": ""},
            "npm": {"installed": False, "version": ""},
            "claude": {"installed": False, "version": ""}
        }

        self.create_widgets()

        # 自动加载已保存的配置
        self.root.after(100, self.load_config)

        # 自动检测环境
        self.root.after(500, self.detect_environment)

    def load_config(self):
        """从配置文件加载 API Key 和模型设置"""
        try:
            import yaml
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cfg_path = os.path.join(base_dir, "config", "config.yaml")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                    if cfg and "deepseek" in cfg:
                        saved_key = cfg["deepseek"].get("api_key", "")
                        self.api_key_var.set(saved_key)

                        saved_model = cfg["deepseek"].get("model", "自动 (智能选择)")
                        # 如果保存的模型在当前选项中，则设置它
                        models = ["自动 (智能选择)", "deepseek-v4-flash", "deepseek-v4-pro"]
                        if saved_model in models:
                            self.model_var.set(saved_model)
                self.log("已从本地配置文件恢复上次的设置", "INFO")
        except Exception as e:
            self.log(f"加载配置失败: {e}", "WARNING")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Primary.TButton", font=self.font_bold,
            background=self.colors["primary"], foreground="white", borderwidth=0, padding=10)
        style.map("Primary.TButton", background=[("active", self.colors["accent"])])
        style.configure("TProgressbar", thickness=8,
            troughcolor=self.colors["bg"], background=self.colors["accent"], borderwidth=0)
        style.configure("TCombobox", fieldbackground=self.colors["bg"],
            background=self.colors["card"], foreground=self.colors["text"],
            darkcolor=self.colors["border"], lightcolor=self.colors["border"],
            arrowcolor=self.colors["text"], borderwidth=1)

    def create_widgets(self):
        container = tk.Frame(self.root, bg=self.colors["bg"], padx=40, pady=30)
        container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(container, bg=self.colors["bg"])
        header.pack(fill=tk.X, pady=(0, 25))

        tk.Label(header, text="Claude Code + DeepSeek", font=self.font_title,
            bg=self.colors["bg"], fg=self.colors["text"]).pack(side=tk.LEFT)
        tk.Label(header, text=" 一键部署工具", font=self.font_subtitle,
            bg=self.colors["bg"], fg=self.colors["accent"]).pack(side=tk.LEFT, pady=(12, 0))

        self.create_card(container, "Step 1: API 接入配置", self.create_api_section)
        self.create_card(container, "Step 2: 系统环境监测", self.create_env_section)
        self.create_card(container, "Step 3: 自动化部署控制", self.create_deploy_section)

        log_frame = tk.Frame(container, bg=self.colors["bg"])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        tk.Label(log_frame, text="Deploy Console", font=("Segoe UI", 9, "bold"),
            bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor=tk.W, pady=(0, 5))
        self.log_text = scrolledtext.ScrolledText(log_frame, font=self.font_code,
            bg="#020617", fg="#10B981", insertbackground="white",
            borderwidth=1, relief=tk.FLAT, height=10, padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        footer = tk.Frame(container, bg=self.colors["bg"], pady=15)
        footer.pack(fill=tk.X)
        tk.Button(footer, text="📄 查看配置指南", command=self.open_docs,
            font=self.font_main, bg=self.colors["bg"], activebackground=self.colors["bg"], activeforeground="white",
            fg=self.colors["text_dim"], borderwidth=0, cursor="hand2").pack(side=tk.LEFT)
        tk.Button(footer, text="安全退出", command=self.root.quit,
            font=self.font_main, bg=self.colors["border"], activebackground="#475569", activeforeground="white", fg="white",
            padx=20, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT)

    def create_card(self, parent, title, content_func):
        card = tk.Frame(parent, bg=self.colors["card"], padx=20, pady=20,
            highlightbackground=self.colors["border"], highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 15))
        tk.Label(card, text=title, font=self.font_bold,
            bg=self.colors["card"], fg=self.colors["accent"]).pack(anchor=tk.W, pady=(0, 15))
        content_func(card)

    def create_api_section(self, card):
        row = tk.Frame(card, bg=self.colors["card"])
        row.pack(fill=tk.X)
        tk.Label(row, text="DeepSeek API Key:", font=self.font_main,
            bg=self.colors["card"], fg=self.colors["text_dim"]).pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = tk.Entry(row, textvariable=self.api_key_var, show="*",
            bg="#0B1121", fg="white", insertbackground="white", font=self.font_code,
            borderwidth=1, relief=tk.FLAT, highlightbackground=self.colors["border"], highlightcolor=self.colors["accent"], highlightthickness=1)
        self.api_key_entry.pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True, ipady=4)
        self.show_key_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row, text="显示", variable=self.show_key_var,
            command=self.toggle_key_visibility, bg=self.colors["card"],
            fg=self.colors["text_dim"], activebackground=self.colors["card"], activeforeground="white",
            selectcolor=self.colors["card"], font=self.font_main).pack(side=tk.LEFT)

    def create_env_section(self, card):
        grid = tk.Frame(card, bg=self.colors["card"])
        grid.pack(fill=tk.X)
        self.env_labels = {}
        envs = [("python", "Python 环境"), ("nodejs", "Node.js 运行时"),
                ("npm", "npm 包管理器"), ("claude", "Claude Code CLI")]
        for i, (key, name) in enumerate(envs):
            item = tk.Frame(grid, bg=self.colors["card"], pady=5)
            item.grid(row=i // 2, column=i % 2, sticky="we", padx=10, pady=5)
            ind = tk.Label(item, text="○", font=("Segoe UI", 14),
                bg=self.colors["card"], fg=self.colors["text_dim"], width=2)
            ind.pack(side=tk.LEFT)
            tf = tk.Frame(item, bg=self.colors["card"])
            tf.pack(side=tk.LEFT, padx=5)
            tk.Label(tf, text=name, font=self.font_bold,
                bg=self.colors["card"], fg=self.colors["text"]).pack(anchor=tk.W)
            vl = tk.Label(tf, text="检测中...", font=("Segoe UI", 8),
                bg=self.colors["card"], fg=self.colors["text_dim"])
            vl.pack(anchor=tk.W)
            self.env_labels[key] = {"indicator": ind, "version": vl}
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    def create_deploy_section(self, card):
        controls = tk.Frame(card, bg=self.colors["card"])
        controls.pack(fill=tk.X)
        model_row = tk.Frame(controls, bg=self.colors["card"])
        model_row.pack(fill=tk.X, pady=(0, 15))
        tk.Label(model_row, text="推理模型:", font=self.font_main,
            bg=self.colors["card"], fg=self.colors["text_dim"]).pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value="自动 (智能选择)")
        combo = ttk.Combobox(model_row, textvariable=self.model_var,
            values=["自动 (智能选择)", "deepseek-v4-flash", "deepseek-v4-pro"],
            state="readonly", width=22, font=self.font_main)
        combo.pack(side=tk.LEFT, padx=15)
        combo.bind("<<ComboboxSelected>>", self.on_model_change)
        self.model_desc = tk.Label(model_row, text="推荐：自动模式可平衡速度与质量",
            font=("Segoe UI", 9), bg=self.colors["card"], fg=self.colors["accent"])
        self.model_desc.pack(side=tk.LEFT, padx=5)

        btn_row = tk.Frame(controls, bg=self.colors["card"], pady=5)
        btn_row.pack(fill=tk.X)
        self.deploy_btn = tk.Button(btn_row, text="🚀 一键部署环境",
            command=self.start_deploy, font=self.font_bold,
            bg=self.colors["primary"], fg="white", activebackground=self.colors["accent"], activeforeground="white",
            padx=30, pady=10, relief=tk.FLAT, cursor="hand2")
        self.deploy_btn.pack(side=tk.LEFT)
        self.test_btn = tk.Button(btn_row, text="测试 API 连接",
            command=self.test_connection, font=self.font_main,
            bg=self.colors["border"], fg="white", activebackground="#475569", activeforeground="white",
            padx=20, pady=10, relief=tk.FLAT, cursor="hand2")
        self.test_btn.pack(side=tk.LEFT, padx=15)
        self.launch_btn = tk.Button(btn_row, text="⚡ 启动 Claude Code",
            command=self.launch_claude_terminal, font=self.font_bold,
            bg=self.colors["success"], fg="white", activebackground="#059669", activeforeground="white",
            padx=30, pady=10, relief=tk.FLAT, state=tk.DISABLED, cursor="hand2")
        self.launch_btn.pack(side=tk.RIGHT)
        self._launch_tooltip = ToolTip(self.launch_btn, "请先点击「一键部署环境」安装 Claude Code")
        self.progress = ttk.Progressbar(card, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(15, 0))

    # --- 回调与工具方法 ---

    def toggle_key_visibility(self):
        self.api_key_entry.config(show="" if self.show_key_var.get() else "*")

    def on_model_change(self, event=None):
        m = self.model_var.get()
        if "flash" in m:
            self.model_desc.config(text="Flash: 极速响应，适合代码修改")
        elif "pro" in m:
            self.model_desc.config(text="Pro: 深度推理，适合复杂架构")
        else:
            self.model_desc.config(text="推荐：自动模式可平衡速度与质量")

    def log(self, message, level="INFO"):
        prefix = " > "
        if level == "SUCCESS":
            prefix = " ✓ "
        elif level == "ERROR":
            prefix = " ✗ "
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, prefix + message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_env_status(self, key, installed, version):
        lbl = self.env_labels[key]
        if installed:
            lbl["indicator"].config(text="●", fg=self.colors["success"])
            lbl["version"].config(text=version, fg=self.colors["text_dim"])
        else:
            lbl["indicator"].config(text="●", fg=self.colors["error"])
            lbl["version"].config(text="未检测到", fg=self.colors["error"])

    def check_command(self, command, args=""):
        """检查命令是否存在并获取版本"""
        # 在 Windows 上，npm/claude 等通常是 .cmd 文件
        search_cmd = command
        if platform.system() == "Windows":
            if not command.endswith(".cmd") and not command.endswith(".exe"):
                # 优先尝试原始命令，如果 shutil.which 找不到，尝试 .cmd
                if not shutil.which(command):
                    search_cmd = command + ".cmd"

        full_path = shutil.which(search_cmd)
        if not full_path:
            return False, ""

        try:
            # 使用 shell=True 增加 Windows 批处理文件的兼容性
            res = subprocess.run(
                [full_path, args] if args else [full_path],
                capture_output=True,
                text=True,
                timeout=10,
                shell=(platform.system() == "Windows")
            )
            return (res.returncode == 0, res.stdout.strip())
        except Exception:
            return False, ""

    def _refresh_path(self):
        """刷新当前进程的 PATH（从注册表读取最新值）"""
        if platform.system() != "Windows":
            return
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as k:
                sys_path = winreg.QueryValueEx(k, "Path")[0]
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
                user_path = winreg.QueryValueEx(k, "Path")[0]

            # 展开发生在注册表中的变量如 %SystemRoot%
            sys_path = os.path.expandvars(sys_path)
            user_path = os.path.expandvars(user_path)

            os.environ["PATH"] = sys_path + ";" + user_path
            self.log("已刷新系统环境变量 PATH")
        except Exception:
            pass

    # --- 环境检测 ---

    def detect_environment(self):
        self.log("正在初始化系统环境检测...")
        self.update_env_status("python", True, platform.python_version())

        # Node.js
        ok, v = self.check_command("node", "--version")
        self.update_env_status("nodejs", ok, v)

        # npm (Windows 下通常为 npm.cmd)
        ok, v = self.check_command("npm", "--version")
        self.update_env_status("npm", ok, v)

        # Claude (Windows 下通常为 claude.cmd)
        ok, v = self.check_command("claude", "--version")
        self.update_env_status("claude", ok, v)

        claude_ok = self.check_command("claude")[0]
        if claude_ok:
            self.launch_btn.config(state=tk.NORMAL)
            self._launch_tooltip.update_text("")
            self.log("环境就绪，可以直接启动 Claude Code", "SUCCESS")
        else:
            self._launch_tooltip.update_text("未检测到 Claude Code，请先点击「一键部署环境」")
            self.log("提示：Claude Code 未安装，请点击「一键部署环境」")

    # --- 部署逻辑 ---

    def start_deploy(self):
        key = self.api_key_var.get().strip()
        if not key:
            messagebox.showwarning("配置缺失", "请输入 DeepSeek API Key 以继续部署")
            return
        self.is_deploying = True
        self.deploy_btn.config(state=tk.DISABLED, text="正在部署...")
        self.progress.start()
        threading.Thread(target=self.deploy_task, args=(key,), daemon=True).start()

    def deploy_task(self, key):
        try:
            model = self.model_var.get()
            if "自动" in model:
                model = "deepseek-v4-flash"

            self.log("-" * 40)
            self.log("开始自动部署流程 (模型: {})".format(model))

            # === Step 1: Node.js ===
            if not self.check_command("node")[0]:
                self.log("[Step 1/3] Node.js 未安装，尝试自动安装...")
                installed_node = False

                if platform.system() == "Windows" and shutil.which("winget"):
                    self.log("使用 winget 安装 Node.js LTS（可能需要1-2分钟）...")
                    res = subprocess.run(
                        ["winget", "install", "OpenJS.NodeJS.LTS",
                         "--accept-package-agreements", "--accept-source-agreements"],
                        capture_output=True, text=True, timeout=600
                    )
                    if res.returncode == 0:
                        self.log("Node.js 安装完成", "SUCCESS")
                        installed_node = True
                    else:
                        self.log("winget 安装返回错误: " + res.stderr[:150], "ERROR")

                if installed_node:
                    self._refresh_path()
                    time.sleep(3)

                # 最终检查
                if not self.check_command("node")[0]:
                    self.log("Node.js 未就绪。请手动安装后重启本程序。", "ERROR")
                    self.log("下载地址: https://npmmirror.com/mirrors/node/")
                    self.root.after(0, lambda: messagebox.showwarning(
                        "需要安装 Node.js",
                        "Node.js 未就绪。\n\n"
                        "请从以下地址下载安装 Node.js 18+：\n"
                        "https://npmmirror.com/mirrors/node/\n\n"
                        "安装完成后关闭并重新打开本程序。"
                    ))
                    return
            else:
                self.log("[Step 1/3] Node.js 已就绪", "SUCCESS")

            # === Step 2: Claude Code ===
            if not self.check_command("claude")[0]:
                self.log("[Step 2/3] 正在通过 npm 安装 Claude Code（淘宝镜像）...")

                # Windows 上 npm 有时需要用 npm.cmd
                npm_cmd = "npm"
                if platform.system() == "Windows":
                    if shutil.which("npm.cmd"):
                        npm_cmd = "npm.cmd"
                    elif not shutil.which("npm"):
                        self._refresh_path()
                        time.sleep(1)
                        if shutil.which("npm.cmd"):
                            npm_cmd = "npm.cmd"

                if not shutil.which(npm_cmd):
                    self.log("找不到 npm，请确认 Node.js 已正确安装", "ERROR")
                    return

                res = subprocess.run(
                    [npm_cmd, "install", "-g", "@anthropic-ai/claude-code",
                     "--registry=https://registry.npmmirror.com"],
                    capture_output=True, text=True, timeout=600
                )
                if res.returncode == 0:
                    self.log("Claude Code 安装成功", "SUCCESS")
                    self._refresh_path()
                else:
                    self.log("Claude Code 安装失败: " + res.stderr[:200], "ERROR")
                    self.root.after(0, lambda: messagebox.showerror(
                        "安装失败", "Claude Code 安装失败，请检查网络连接。"))
                    return
            else:
                self.log("[Step 2/3] Claude Code 已就绪", "SUCCESS")

            # === Step 3: 保存配置 ===
            self.log("[Step 3/3] 保存 API 配置...")
            self.save_config(key, model)
            self.log("配置保存成功", "SUCCESS")

            self.root.after(0, self.detect_environment)
            self.root.after(0, lambda: messagebox.showinfo(
                "部署成功", "环境已配置完成！\n现在可以点击「启动 Claude Code」开始使用。"))

        except Exception as e:
            self.log("部署中断: {}".format(e), "ERROR")
        finally:
            self.is_deploying = False
            self.root.after(0, lambda: self.deploy_btn.config(
                state=tk.NORMAL, text="🚀 一键部署环境"))
            self.root.after(0, self.progress.stop)

    # --- 配置保存 ---

    def save_config(self, key, model):
        import yaml
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cfg_dir = os.path.join(base_dir, "config")
        os.makedirs(cfg_dir, exist_ok=True)
        cfg = {
            "deepseek": {
                "api_key": key,
                "base_url_openai": "https://api.deepseek.com/v1",
                "base_url_anthropic": "https://api.deepseek.com/anthropic",
                "model": model
            },
            "claude_code": {
                "base_url": "https://api.deepseek.com/anthropic",
                "model": model
            }
        }
        with open(os.path.join(cfg_dir, "config.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)

    # --- API 测试 ---

    def test_connection(self):
        key = self.api_key_var.get().strip()
        if not key:
            messagebox.showwarning("提示", "请先输入 API Key")
            return
        self.log("正在验证 API 连接有效性...")
        threading.Thread(target=self._test_api_thread, args=(key,), daemon=True).start()

    def _test_api_thread(self, key):
        try:
            from openai import OpenAI
            c = OpenAI(api_key=key, base_url="https://api.deepseek.com/v1")
            c.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=5
            )
            self.log("API 连接验证通过", "SUCCESS")
            self.root.after(0, lambda: messagebox.showinfo(
                "测试成功", "API Key 有效，网络连接正常。"))
        except Exception as e:
            err = str(e)
            self.log("验证失败: {}".format(err), "ERROR")
            self.root.after(0, lambda err=err: messagebox.showerror(
                "测试失败", "无法连接到 API: {}".format(err)))

    # --- 启动 Claude Code ---

    def launch_claude_terminal(self):
        key = self.api_key_var.get().strip()
        model = self.model_var.get()
        if "自动" in model:
            model = "deepseek-v4-flash"
        base_url = "https://api.deepseek.com/anthropic"

        self.log(f"正在启动终端并注入环境变量 (模型: {model})...")

        if platform.system() == "Windows":
            # 探测 claude 完整路径，防止 cmd 找不到命令
            claude_path = shutil.which("claude") or shutil.which("claude.cmd")
            if not claude_path:
                # 尝试再次刷新 PATH 后检测
                self._refresh_path()
                claude_path = shutil.which("claude") or shutil.which("claude.cmd")

            if not claude_path:
                self.log("找不到 claude 命令，请确认已安装 @anthropic-ai/claude-code", "ERROR")
                messagebox.showerror("启动失败", "在您的 PATH 中找不到 'claude' 命令。\n\n请尝试重新点击「一键部署环境」。")
                return

            # 写入临时 .bat 文件避免 cmd 引号嵌套问题
            bat_content = (
                f'@echo off\r\n'
                f'set "ANTHROPIC_API_KEY={key}"\r\n'
                f'set "ANTHROPIC_BASE_URL={base_url}"\r\n'
                f'echo ------------------------------------------\r\n'
                f'echo 环境已就绪！当前模型: {model}\r\n'
                f'echo ------------------------------------------\r\n'
                f'"{claude_path}" --model {model}\r\n'
            )
            fd, bat_path = tempfile.mkstemp(suffix=".bat", prefix="claude_launch_")
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(bat_content)
            atexit.register(lambda p=bat_path: os.path.exists(p) and os.unlink(p))

            subprocess.Popen(f'start "Claude Code + DeepSeek" cmd /k ""{bat_path}""', shell=True)
            self.log("终端已启动", "SUCCESS")

        elif platform.system() == "Darwin":
            script = ('tell application "Terminal" to do script '
                      '"export ANTHROPIC_API_KEY=\'{}\' && export ANTHROPIC_BASE_URL=\'{}\' '
                      '&& claude --model {}"').format(key, base_url, model)
            subprocess.run(["osascript", "-e", script])
        else:
            self.log("Linux: 请手动设置环境变量后运行 claude", "ERROR")

    # --- 文档 ---

    def open_docs(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        doc = os.path.join(base_dir, "CLAUDE_CODE_CONFIG.md")
        if os.path.exists(doc):
            if platform.system() == "Windows":
                os.startfile(doc)
            elif platform.system() == "Darwin":
                subprocess.run(["open", doc])
            else:
                subprocess.run(["xdg-open", doc])
        else:
            messagebox.showinfo("提示", "请参考项目根目录下的 README.md")


def main():
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    DeployGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

