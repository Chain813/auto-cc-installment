#!/bin/bash
# Claude Code + DeepSeek API 一键安装脚本 (Linux/macOS)
# 无需 VPN，使用国内镜像

set -e

echo "=================================="
echo " Claude Code + DeepSeek API 安装"
echo "  无需 VPN，使用国内镜像"
echo "=================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ $1${NC}"; }

# npm 镜像源（国内镜像，无需 VPN）
NPM_REGISTRY="https://registry.npmmirror.com"

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 安装 Node.js
install_nodejs() {
    print_info "正在安装 Node.js..."

    if [[ "$OS" == "macos" ]]; then
        if command_exists brew; then
            brew install node@18
        else
            print_error "请先安装 Homebrew"
            print_info '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            exit 1
        fi
    elif [[ "$OS" == "linux" ]]; then
        if command_exists apt; then
            sudo apt update
            sudo apt install -y nodejs npm
        elif command_exists yum; then
            sudo yum install -y nodejs npm
        elif command_exists dnf; then
            sudo dnf install -y nodejs npm
        else
            print_error "无法自动安装 Node.js，请手动安装"
            print_info "国内镜像下载: https://npmmirror.com/mirrors/node/"
            exit 1
        fi
    fi

    print_success "Node.js 安装完成"
}

# 检查 Node.js
check_nodejs() {
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_success "Node.js 已安装: $NODE_VERSION"
        return 0
    else
        print_warning "Node.js 未安装"
        read -p "是否自动安装? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_nodejs
        else
            print_error "请手动安装 Node.js 18+"
            print_info "国内镜像下载: https://npmmirror.com/mirrors/node/"
            exit 1
        fi
    fi
}

# 检查 npm
check_npm() {
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_success "npm 已安装: $NPM_VERSION"
    else
        print_error "npm 未安装"
        exit 1
    fi
}

# 安装 Claude Code
install_claude_code() {
    print_info "正在安装 Claude Code..."
    print_info "使用镜像源: $NPM_REGISTRY"
    npm install -g @anthropic-ai/claude-code --registry=$NPM_REGISTRY
    print_success "Claude Code 安装完成"
}

# 安装 Python 依赖
install_python_deps() {
    print_info "正在安装 Python 依赖..."

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

    if command_exists pip3; then
        pip3 install -r "$PROJECT_DIR/requirements.txt"
    elif command_exists pip; then
        pip install -r "$PROJECT_DIR/requirements.txt"
    else
        print_error "pip 未安装"
        exit 1
    fi

    print_success "Python 依赖安装完成"
}

# 主安装流程
main() {
    echo ""
    print_info "检测操作系统: $OS"
    echo ""

    # 检查 Node.js
    check_nodejs
    check_npm

    # 安装 Claude Code
    install_claude_code

    # 安装 Python 依赖
    install_python_deps

    echo ""
    echo "=================================="
    print_success "安装完成！"
    echo "=================================="
    echo ""
    print_info "使用方法:"
    echo "  1. 配置 API: python -m src.main configure"
    echo "  2. 测试连接: python -m src.main test"
    echo "  3. 开始聊天: python -m src.main chat"
    echo "  4. 查看状态: python -m src.main status"
    echo ""
}

# 运行主程序
main
