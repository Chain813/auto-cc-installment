# Claude Code + DeepSeek API 自动化部署工具

[![CI](https://github.com/Chain813/auto-cc-installment/actions/workflows/ci.yml/badge.svg)](https://github.com/Chain813/auto-cc-installment/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

> 一键部署 Claude Code CLI，通过 DeepSeek API 的 Anthropic 兼容端点实现国内直连使用，无需 VPN。

---

## 目录

- [功能特性](#功能特性)
- [工作原理](#工作原理)
- [快速开始](#快速开始)
- [详细安装](#详细安装)
- [使用指南](#使用指南)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [智能模型选择](#智能模型选择)
- [前置要求](#前置要求)
- [常见问题](#常见问题)
- [相关文档](#相关文档)
- [许可证](#许可证)

---

## 功能特性

| 特性 | 说明 |
|------|------|
| **GUI 一键部署** | 图形界面操作，输入 API Key 即可自动完成全部配置 |
| **自动安装 Claude Code** | 检测并自动安装 Node.js、npm 和 Claude Code CLI |
| **DeepSeek API 集成** | 利用 Anthropic 兼容端点，在 Claude Code 中直接使用 DeepSeek |
| **交互式聊天** | 支持流式输出的命令行对话，含智能模型选择 |
| **跨平台支持** | 完整支持 Windows、macOS 和 Linux |
| **国内镜像加速** | 使用淘宝/阿里云/腾讯云/华为云 npm 镜像，无需 VPN |
| **智能模型切换** | 根据任务复杂度自动选择 flash/pro 模型 |
| **安全存储** | API Key 通过环境变量和本地配置管理，不硬编码 |

---

## 工作原理

DeepSeek 提供 **Anthropic 兼容端点**，Claude Code 可以直接对接，无需代理或中间层：

```
┌─────────────────┐       Anthropic 格式请求        ┌─────────────────┐
│   Claude Code   │ ──────────────────────────────→ │   DeepSeek API  │
│   CLI 工具       │                                 │   /anthropic    │
│                 │ ←──────────────────────────────  │                 │
└─────────────────┘       响应 (Claude 兼容)         └─────────────────┘
```

| API 类型 | 端点 | 用途 |
|----------|------|------|
| OpenAI 兼容 | `https://api.deepseek.com/v1` | 本工具内置聊天功能 |
| Anthropic 兼容 | `https://api.deepseek.com/anthropic` | Claude Code 直接接入 |

---

## 快速开始

> 前提：已安装 [Python 3.8+](https://www.python.org/downloads/)（安装时勾选 "Add Python to PATH"）

### Windows (推荐方式)

项目包含了一个无黑窗口的图形界面部署工具。

双击运行 **`启动工具.vbs`**。脚本会在后台静默启动极客风的 GUI 界面。在界面中输入 API Key 即可自动完成：

1. 检测系统环境（Python, Node.js 等）
2. 自动配置 npm 淘宝镜像并安装 Claude Code
3. **配置记忆**：自动记忆并加载您上次保存的 DeepSeek API Key 和模型偏好
4. **会话隔离启动**：点击“⚡ 启动 Claude Code”，工具会为您弹出一个独立的终端并自动注入环境变量，无需配置系统的全局变量。

*(备用选项：如果 `启动工具.vbs` 无法运行，您也可以双击 `install.bat` 运行)*

### macOS / Linux

```bash
chmod +x install.sh
./install.sh
```

### 纯 Python 启动 GUI

```bash
python launcher.py
```

---

## 详细安装

如需分步手动操作，或深入了解底层逻辑，请参考以下流程。

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

核心依赖：`pyyaml`、`requests`、`rich`、`click`、`openai`

### 2. 安装 Claude Code

```bash
# 使用国内镜像（推荐，无需 VPN）
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

也可使用 `scripts/install.sh` 或 `scripts/install.ps1` 脚本安装。

### 3. 配置 DeepSeek API

```bash
# 交互式配置向导
python -m src.main configure
```

按提示输入 API Key（在 [platform.deepseek.com](https://platform.deepseek.com) 申请）。

### 4. 启动 Claude Code

```bash
# 方式 A：一键设置当前终端环境变量
python -m src.main setup-env
claude

# 方式 B：手动设置环境变量
# Windows PowerShell:
$env:ANTHROPIC_API_KEY = "your-deepseek-api-key"
$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
claude

# Linux / macOS:
export ANTHROPIC_API_KEY="your-deepseek-api-key"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
claude
```

---

## 使用指南

### GUI 方式

| 启动命令 | 说明 |
|----------|------|
| `install.bat` / `./install.sh` | 全自动安装（推荐，双击运行） |
| `python launcher.py` | 启动 GUI 部署工具 |
| `python src/gui.py` | 启动 GUI（备选入口） |

### CLI 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `install` | 安装 Claude Code | `python -m src.main install` |
| `configure` | 配置 DeepSeek API | `python -m src.main configure` |
| `setup-env` | 一键设置当前终端环境变量 | `python -m src.main setup-env` |
| `configure-claude-code` | 生成 Claude Code 配置/启动脚本 | `python -m src.main configure-claude-code` |
| `show` | 显示当前配置 | `python -m src.main show` |
| `test` | 测试 API 连接 | `python -m src.main test` |
| `chat` | 启动交互式聊天 | `python -m src.main chat` |
| `chat --auto-model` | 启动智能模型选择聊天 | `python -m src.main chat --auto-model` |
| `status` | 显示系统状态 | `python -m src.main status` |

### 运行测试

```bash
# 使用 pytest
python -m pytest tests/ -v

# 使用 unittest
python -m unittest discover tests/ -v
```

---

## 项目结构

```
auto-cc-installment/
├── install.bat                 # Windows 一键安装脚本（双击运行）
├── install.sh                  # macOS/Linux 一键安装脚本
├── launcher.py                 # GUI 启动入口
├── src/                        # 核心源码
│   ├── __init__.py
│   ├── main.py                 # CLI 入口 (Click 命令组)
│   ├── installer.py            # Claude Code 安装器
│   ├── api_config.py           # API 配置管理 (YAML)
│   ├── deepseek_client.py      # DeepSeek API 客户端 (OpenAI SDK)
│   ├── model_selector.py       # 智能模型选择器
│   ├── gui.py                  # GUI 界面 (tkinter)
│   └── utils.py                # 工具函数
├── scripts/                    # 辅助安装脚本
│   ├── install.sh              # Linux/macOS npm 安装脚本
│   └── install.ps1             # Windows npm 安装脚本
├── tests/                      # 测试
│   ├── test_installation.py    # 安装模块测试
│   └── test_network.py         # 网络连接测试
├── config/                     # 配置目录 (运行时生成)
│   └── config.yaml             # 用户配置文件
├── requirements.txt            # Python 依赖
├── requirements-lock.txt       # 依赖锁定版本
├── .github/workflows/          # GitHub Actions CI
│   ├── ci.yml                  # 多平台测试 + lint
│   └── release.yml             # 发布流程
├── CLAUDE_CODE_CONFIG.md       # Claude Code 配置指南
├── NETWORK.md                  # 网络说明
├── SECURITY.md                 # 安全说明
└── TEST_REPORT.md              # 测试报告
```

---

## 配置说明

### 配置文件

配置文件位于 `config/config.yaml`，首次运行时自动创建：

```yaml
deepseek:
  api_key: "your-api-key"
  base_url_openai: "https://api.deepseek.com/v1"
  base_url_anthropic: "https://api.deepseek.com/anthropic"
  model: "deepseek-v4-flash"

claude_code:
  base_url: "https://api.deepseek.com/anthropic"
  model: "deepseek-v4-flash"

npm:
  registry: "https://registry.npmmirror.com"

general:
  log_level: "INFO"
  timeout: 30
  max_retries: 3
```

### 环境变量

可通过环境变量覆盖配置（优先级高于配置文件）：

| 变量名 | 说明 |
|--------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `ANTHROPIC_API_KEY` | Claude Code 使用的 API Key |
| `ANTHROPIC_BASE_URL` | Claude Code 使用的 API 端点 |

### npm 镜像源

| 镜像源 | 地址 | 备注 |
|--------|------|------|
| 淘宝镜像 | `https://registry.npmmirror.com` | 默认，推荐 |
| 阿里云镜像 | `https://npm.aliyun.com` | 备用 |
| 腾讯云镜像 | `https://mirrors.cloud.tencent.com/npm` | 备用 |
| 华为云镜像 | `https://repo.huaweicloud.com/repository/npm/` | 备用 |
| 官方源 | `https://registry.npmjs.org` | 需要 VPN |

---

## 智能模型选择

项目支持根据任务复杂度自动选择 DeepSeek 模型：

| 模型 | 速度 | 适用场景 |
|------|------|----------|
| `deepseek-v4-flash` | 快 | 日常编程、快速问答、格式转换、简单操作 |
| `deepseek-v4-pro` | 慢 | 复杂架构、代码重构、系统设计、调试排查 |

### 选择逻辑

- **Flash 模型触发**：短消息（< 10 词）、简单关键词（hello、help、run）、基本操作
- **Pro 模型触发**：长消息（> 20 词）、复杂关键词（architecture、refactor）、包含代码块、多行输入

### 使用方式

```bash
# 命令行
python -m src.main chat --auto-model

# GUI 中选择"自动 (智能选择)"
python launcher.py
```

---

## 可用模型

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| `deepseek-v4-flash` | 快速模型 | 日常编程、快速问答（推荐） |
| `deepseek-v4-pro` | 专业模型 | 复杂任务、代码生成 |

> **注意**: `deepseek-chat` 和 `deepseek-reasoner` 将于 2026/07/24 弃用，请使用上述模型。

---

## 前置要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 运行本工具 |
| Node.js | 18+ | 安装 Claude Code 需要 |
| npm | 随 Node.js | 安装 Claude Code 需要 |
| DeepSeek API Key | - | 在 [platform.deepseek.com](https://platform.deepseek.com) 申请 |

---

## 常见问题

### 已下载过旧版本，如何更新？

本项目曾重写 Git 历史以清除敏感信息，旧版本与远程仓库已分叉，`git pull` 会报错。请执行以下命令强制同步：

```bash
git fetch origin
git reset --hard origin/main
```

> **注意：** 如果你有本地未推送的修改，请先备份再执行上述命令。

### 如何获取 DeepSeek API Key？

访问 [platform.deepseek.com](https://platform.deepseek.com) 注册账号，在 API Keys 页面创建密钥。

### Claude Code 如何使用 DeepSeek API？

DeepSeek 提供 Anthropic 兼容端点，只需设置两个环境变量：

```bash
export ANTHROPIC_API_KEY="your-deepseek-api-key"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
```

或使用本工具一键配置：`python -m src.main setup-env`

### 需要使用 VPN 吗？

**不需要。** DeepSeek API 服务器位于中国，国内可直连。npm 安装使用国内镜像，同样无需 VPN。

### 环境变量设置后不生效？

环境变量仅在当前终端会话有效。如需永久生效：

- **Linux/macOS**: 将 `export` 命令添加到 `~/.bashrc` 或 `~/.zshrc`
- **Windows**: 通过"系统属性 → 环境变量"设置，或使用 `python -m src.main configure-claude-code` 生成启动脚本

### API 连接失败怎么办？

```bash
# 1. 测试网络连通性
curl -I https://api.deepseek.com

# 2. 检查 API Key 是否有效
python -m src.main test

# 3. 查看当前配置
python -m src.main show
```

常见原因：API Key 无效、余额不足、网络受限。详见 [NETWORK.md](NETWORK.md)。

---

## 网络说明

**本项目无需使用 VPN 或任何代理工具。**

- DeepSeek API 位于中国，国内用户可直接访问
- npm 安装使用国内镜像（淘宝镜像等）
- 所有网络请求均使用 HTTPS 直连

详细网络配置和故障排除请参考 [NETWORK.md](NETWORK.md)。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [CLAUDE_CODE_CONFIG.md](CLAUDE_CODE_CONFIG.md) | Claude Code 配置指南 |
| [NETWORK.md](NETWORK.md) | 网络配置和故障排除 |
| [SECURITY.md](SECURITY.md) | 安全措施说明 |
| [TEST_REPORT.md](TEST_REPORT.md) | 测试结果报告 |

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
