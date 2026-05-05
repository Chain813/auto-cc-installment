# Claude Code + DeepSeek API 一键安装脚本 (Windows PowerShell)
# 无需 VPN，使用国内镜像

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Claude Code + DeepSeek API 安装" -ForegroundColor Cyan
Write-Host "  无需 VPN，使用国内镜像" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 打印函数
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor Blue }

# npm 镜像源（国内镜像，无需 VPN）
$NPM_REGISTRY = "https://registry.npmmirror.com"

# 检查命令是否存在
function Test-Command {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# 安装 Node.js
function Install-NodeJS {
    Write-Info "正在安装 Node.js..."
    Write-Host ""
    Write-Info "下载地址（任选其一）:"
    Write-Host "  1. 国内镜像: https://npmmirror.com/mirrors/node/ (推荐)"
    Write-Host "  2. 腾讯镜像: https://mirrors.cloud.tencent.com/nodejs-release/"
    Write-Host "  3. 官方网站: https://nodejs.org (可能需要 VPN)"
    Write-Host ""

    if (Test-Command "winget") {
        Write-Info "使用 winget 安装..."
        winget install OpenJS.NodeJS.LTS
    } elseif (Test-Command "choco") {
        Write-Info "使用 Chocolatey 安装..."
        choco install nodejs-lts -y
    } elseif (Test-Command "scoop") {
        Write-Info "使用 Scoop 安装..."
        scoop install nodejs-lts
    } else {
        Write-Warning "无法自动安装，请手动下载安装"
        Write-Info "推荐使用国内镜像下载，无需 VPN"
        exit 1
    }

    Write-Success "Node.js 安装完成"
    Write-Warning "请重新打开 PowerShell 窗口以使 PATH 生效"
}

# 检查 Node.js
function Test-NodeJS {
    if (Test-Command "node") {
        $nodeVersion = node --version
        Write-Success "Node.js 已安装: $nodeVersion"
        return $true
    } else {
        Write-Warning "Node.js 未安装"
        $response = Read-Host "是否自动安装? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            Install-NodeJS
            return $true
        } else {
            Write-Error "请手动安装 Node.js 18+"
            Write-Info "国内镜像下载: https://npmmirror.com/mirrors/node/"
            exit 1
        }
    }
}

# 检查 npm
function Test-Npm {
    if (Test-Command "npm") {
        $npmVersion = npm --version
        Write-Success "npm 已安装: $npmVersion"
        return $true
    } else {
        Write-Error "npm 未安装"
        exit 1
    }
}

# 安装 Claude Code
function Install-ClaudeCode {
    Write-Info "正在安装 Claude Code..."
    Write-Info "使用镜像源: $NPM_REGISTRY"
    npm install -g @anthropic-ai/claude-code --registry=$NPM_REGISTRY
    Write-Success "Claude Code 安装完成"
}

# 安装 Python 依赖
function Install-PythonDeps {
    Write-Info "正在安装 Python 依赖..."

    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    $projectDir = Split-Path -Parent $scriptDir

    if (Test-Command "pip3") {
        pip3 install -r "$projectDir\requirements.txt"
    } elseif (Test-Command "pip") {
        pip install -r "$projectDir\requirements.txt"
    } else {
        Write-Error "pip 未安装"
        exit 1
    }

    Write-Success "Python 依赖安装完成"
}

# 主安装流程
function Main {
    Write-Host ""
    Write-Info "检测操作系统: Windows"
    Write-Host ""

    # 检查 Node.js
    Test-NodeJS
    Test-Npm

    # 安装 Claude Code
    Install-ClaudeCode

    # 安装 Python 依赖
    Install-PythonDeps

    Write-Host ""
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Success "安装完成！"
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Info "使用方法:"
    Write-Host "  1. 配置 API: python -m src.main configure"
    Write-Host "  2. 测试连接: python -m src.main test"
    Write-Host "  3. 开始聊天: python -m src.main chat"
    Write-Host "  4. 查看状态: python -m src.main status"
    Write-Host ""
}

# 运行主程序
Main
