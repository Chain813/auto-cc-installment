#!/bin/bash
# Claude Code + DeepSeek API 一键安装脚本
# 无需 VPN，国内直连
# 使用方式: chmod +x install.sh && ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "       ${GREEN}$1 - OK${NC}"; }
info() { echo -e "       ${YELLOW}$1${NC}"; }
err()  { echo -e "       ${RED}[错误] $1${NC}"; }
step() { echo -e "${CYAN}[$1/5]${NC} $2"; }

echo
echo -e "${CYAN}${BOLD}"
echo "  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗"
echo " ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝"
echo " ██║     ██║     ███████║██║   ██║██║  ██║█████╗"
echo " ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝"
echo " ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗"
echo "  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝"
echo -e "${NC}"
echo -e "  ${BOLD}Claude Code + DeepSeek API 一键安装${NC}"
echo -e "  无需 VPN，国内直连"
echo
echo "========================================"
echo

# ============================================
# Step 1: 检查 Python
# ============================================
step "1" "检查 Python..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &>/dev/null; then
    PYTHON=python
    PIP=pip
else
    echo
    err "未找到 Python"
    echo "  macOS:          brew install python"
    echo "  Ubuntu/Debian:  sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL:    sudo yum install python3 python3-pip"
    echo
    exit 1
fi

PYVER=$($PYTHON --version 2>&1)
ok "$PYVER"
echo

# ============================================
# Step 2: 安装 Python 依赖
# ============================================
step "2" "安装 Python 依赖..."

if ! $PYTHON -c "import yaml, requests, rich, click, openai" 2>/dev/null; then
    if ! $PYTHON -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null; then
        if ! $PYTHON -m pip install --quiet --user -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null; then
            err "依赖安装失败，请手动执行: $PIP install -r requirements.txt"
            exit 1
        fi
    fi
fi
ok "依赖安装完成"
echo

# ============================================
# Step 3: 检查/安装 Node.js
# ============================================
step "3" "检查 Node.js..."

if ! command -v node &>/dev/null; then
    info "Node.js 未安装，尝试自动安装..."

    installed=false
    if [[ "$(uname)" == "Darwin" ]] && command -v brew &>/dev/null; then
        info "使用 Homebrew 安装..."
        if brew install node@18 2>/dev/null; then
            installed=true
        fi
    elif command -v apt &>/dev/null; then
        info "使用 apt 安装..."
        if sudo apt update -qq 2>/dev/null && sudo apt install -y -qq nodejs npm 2>/dev/null; then
            installed=true
        fi
    elif command -v yum &>/dev/null; then
        info "使用 yum 安装..."
        if sudo yum install -y nodejs npm 2>/dev/null; then
            installed=true
        fi
    elif command -v dnf &>/dev/null; then
        info "使用 dnf 安装..."
        if sudo dnf install -y nodejs npm 2>/dev/null; then
            installed=true
        fi
    fi

    if $installed; then
        ok "Node.js 安装完成"
    else
        echo
        err "自动安装失败，请手动安装 Node.js 18+"
        echo "  国内镜像: https://npmmirror.com/mirrors/node/"
        echo "  安装后重新运行本脚本"
        echo
        exit 1
    fi
else
    ok "Node.js $(node --version)"
fi
echo

# ============================================
# Step 4: 检查/安装 Claude Code
# ============================================
step "4" "检查 Claude Code..."

if ! command -v claude &>/dev/null; then
    info "Claude Code 未安装，正在通过 npm 安装..."
    info "使用淘宝镜像，无需 VPN"
    if npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com 2>/dev/null; then
        ok "Claude Code 安装完成"
    else
        echo
        err "Claude Code 安装失败，请检查网络连接"
        exit 1
    fi
else
    ok "Claude Code 已安装"
fi
echo

# ============================================
# Step 5: 配置 DeepSeek API
# ============================================
step "5" "配置 DeepSeek API..."
echo
echo -e "  请输入你的 ${BOLD}DeepSeek API Key${NC}"
echo "  获取地址: https://platform.deepseek.com"
echo
read -rp "  API Key: " API_KEY

if [[ -z "$API_KEY" ]]; then
    echo
    info "未输入 API Key，跳过配置"
    info "稍后可运行: python -m src.main configure"
else
    # 保存配置
    mkdir -p "$SCRIPT_DIR/config"
    $PYTHON -c "
import yaml, os
config = {
    'deepseek': {
        'api_key': '$API_KEY',
        'base_url_openai': 'https://api.deepseek.com/v1',
        'base_url_anthropic': 'https://api.deepseek.com/anthropic',
        'model': 'deepseek-v4-flash'
    },
    'claude_code': {
        'base_url': 'https://api.deepseek.com/anthropic',
        'model': 'deepseek-v4-flash'
    }
}
with open('$SCRIPT_DIR/config/config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
" 2>/dev/null

    # 测试连接
    echo
    info "测试 API 连接..."
    if $PYTHON -c "
from openai import OpenAI
c = OpenAI(api_key='$API_KEY', base_url='https://api.deepseek.com/v1')
c.chat.completions.create(model='deepseek-v4-flash', messages=[{'role':'user','content':'hi'}], max_tokens=5)
print('      API 连接成功')
" 2>/dev/null; then
        ok "API 连接成功"
    else
        info "[警告] API 连接测试失败，请检查 Key 是否正确"
    fi
fi

echo
echo "========================================"
echo
echo -e "  ${GREEN}${BOLD}安装完成！${NC}"
echo
echo "  使用方法:"
echo "    1. 设置环境变量:  python -m src.main setup-env"
echo "    2. 启动 Claude:   claude"
echo
echo "  其他命令:"
echo "    python -m src.main chat            交互式聊天"
echo "    python -m src.main chat --auto-model  智能模型聊天"
echo "    python -m src.main show            查看配置"
echo "    python -m src.main status          系统状态"
echo "    python launcher.py                 GUI 界面"
echo
echo "========================================"
echo
