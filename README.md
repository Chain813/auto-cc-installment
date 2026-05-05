# Claude Code + DeepSeek API 自动化工具

[![CI](https://github.com/Chain813/auto-cc-installment/actions/workflows/ci.yml/badge.svg)](https://github.com/Chain813/auto-cc-installment/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

自动化安装 Claude Code CLI 并配置 DeepSeek API 的跨平台工具。

## 功能特性

- 🚀 **自动安装 Claude Code** - 检测并自动安装 Node.js 和 Claude Code
- 🔑 **DeepSeek API 集成** - 直接在 Claude Code 中使用 DeepSeek API
- 💬 **交互式聊天** - 使用 DeepSeek API 进行对话
- 🖥️ **跨平台支持** - 支持 Windows、macOS 和 Linux
- ⚙️ **简单配置** - 命令行配置向导
- 🌐 **无需 VPN** - 使用国内镜像，直连 DeepSeek API
- 🔄 **API 兼容** - DeepSeek 提供 Anthropic 兼容端点
- 🎨 **GUI 界面** - 一键部署，只需输入 API Key
- ⚡ **一键设置环境变量** - 快速配置当前终端会话
- 🧠 **智能模型选择** - 根据任务复杂度自动选择 flash/pro 模型

## 快速开始（GUI 一键部署）

```bash
# 启动 GUI 一键部署工具
python launcher.py
```

只需输入 DeepSeek API Key，点击"开始部署"即可自动完成所有配置！

---

## 命令行方式

### 1. 一键安装

**Linux/macOS:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\install.ps1
```

### 2. 手动安装

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Claude Code（使用国内镜像，无需 VPN）
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

### 3. 配置 DeepSeek API

```bash
python -m src.main configure
```

按提示输入你的 DeepSeek API Key。可以在 [DeepSeek Platform](https://platform.deepseek.com) 获取。

### 4. 在 Claude Code 中使用 DeepSeek

```bash
# 方式 1: 环境变量配置（推荐）
# Windows PowerShell:
$env:ANTHROPIC_API_KEY = "your-deepseek-api-key"
$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
claude

# Linux/macOS:
export ANTHROPIC_API_KEY="your-deepseek-api-key"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
claude

# 方式 2: 使用本工具自动生成配置
python -m src.main configure-claude-code
```

## 命令列表

### GUI 方式

| 启动方式 | 说明 |
|----------|------|
| `python launcher.py` | 启动 GUI 一键部署工具 |
| `python src/gui.py` | 启动 GUI（备选） |

### CLI 方式

| 命令 | 说明 |
|------|------|
| `install` | 安装 Claude Code |
| `configure` | 配置 DeepSeek API |
| `setup-env` | 一键设置环境变量（当前终端） |
| `configure-claude-code` | 配置 Claude Code 使用 DeepSeek |
| `show` | 显示当前配置 |
| `test` | 测试 API 连接 |
| `chat` | 启动交互式聊天 |
| `chat --auto-model` | 启动智能模型选择聊天 |
| `status` | 显示系统状态 |

## DeepSeek API 接入原理

DeepSeek 提供 **Anthropic 兼容端点**，无需代理即可直接在 Claude Code 中使用：

```
┌─────────────────┐                    ┌─────────────────┐
│   Claude Code   │ ──────────────────→│   DeepSeek API  │
│                 │   Anthropic 格式   │                 │
│   /v1/messages  │                    │   /anthropic    │
└─────────────────┘                    └─────────────────┘
```

### API 端点

| API 类型 | 端点 | 用途 |
|----------|------|------|
| OpenAI 兼容 | `https://api.deepseek.com/v1` | 本工具聊天功能 |
| Anthropic 兼容 | `https://api.deepseek.com/anthropic` | Claude Code 直接接入 |

### 可用模型

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| `deepseek-v4-flash` | 快速模型 | 日常编程、快速问答 |
| `deepseek-v4-pro` | 专业模型 | 复杂任务、代码生成 |

> ⚠️ `deepseek-chat` 和 `deepseek-reasoner` 将于 2026/07/24 弃用

## 配置文件

配置文件位于 `config/config.yaml`，首次运行时会自动创建。

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
```

## 环境变量

可以通过环境变量覆盖配置：

- `DEEPSEEK_API_KEY` - DeepSeek API 密钥
- `ANTHROPIC_API_KEY` - Claude Code 使用的 API Key
- `ANTHROPIC_BASE_URL` - Claude Code 使用的 API 端点

## 网络说明

**本项目无需使用 VPN 或任何代理工具。**

- DeepSeek API 位于中国，国内用户可直接访问
- npm 安装使用国内镜像（淘宝镜像）
- 所有网络请求均使用直连方式

## 智能模型选择

项目支持根据任务复杂度自动选择模型：

| 模型 | 适用场景 | 速度 |
|------|----------|------|
| `deepseek-v4-flash` | 简单问答、快速操作、格式转换 | 快 |
| `deepseek-v4-pro` | 复杂架构、代码重构、系统设计 | 慢 |

### 使用方法

```bash
# 启用智能模型选择的聊天
python -m src.main chat --auto-model

# 或在 GUI 中选择"自动 (智能选择)"
python launcher.py
```

### 选择逻辑

- **Flash 模型**: 短消息、简单关键词、基本操作
- **Pro 模型**: 长消息、复杂关键词、代码块、多行输入

## 前置要求

- Python 3.8+
- Node.js 18+ (安装 Claude Code 需要)
- npm (随 Node.js 安装)
- DeepSeek API Key (在 [platform.deepseek.com](https://platform.deepseek.com) 申请)

## 常见问题

### 如何获取 DeepSeek API Key？

访问 https://platform.deepseek.com 注册并获取 API Key。

### Claude Code 如何使用 DeepSeek API？

DeepSeek 提供 Anthropic 兼容端点，只需设置环境变量：
```bash
export ANTHROPIC_API_KEY="your-key"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
```

### 需要使用 VPN 吗？

**不需要。** DeepSeek API 位于中国，国内可直接访问。

### 支持哪些模型？

- `deepseek-v4-flash` - 快速模型（推荐）
- `deepseek-v4-pro` - 专业模型

## 详细文档

- [网络说明](NETWORK.md) - 网络配置和故障排除
- [Claude Code 配置指南](CLAUDE_CODE_CONFIG.md) - 详细配置说明
- [测试报告](TEST_REPORT.md) - 测试结果

## 许可证

MIT License
