@echo off
chcp 65001 >nul 2>&1
title Claude Code + DeepSeek 一键安装

echo.
echo  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
echo ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
echo ██║     ██║     ███████║██║   ██║██║  ██║█████╗
echo ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
echo ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
echo  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
echo.
echo  Claude Code + DeepSeek API 一键安装
echo  无需 VPN，国内直连
echo.
echo ========================================
echo.

:: ============================================
:: Step 1: 检查 Python
:: ============================================
echo [1/5] 检查 Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [错误] 未找到 Python
    echo  请先安装 Python 3.8+: https://www.python.org/downloads/
    echo  安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo       Python %PYVER% - OK
echo.

:: ============================================
:: Step 2: 安装 Python 依赖
:: ============================================
echo [2/5] 安装 Python 依赖...
python -c "import yaml, requests, rich, click, openai" >nul 2>&1
if %errorlevel% neq 0 (
    python -m pip install --quiet -r "%~dp0requirements.txt" >nul 2>&1
    if %errorlevel% neq 0 (
        python -m pip install --quiet --user -r "%~dp0requirements.txt" >nul 2>&1
    )
    if %errorlevel% neq 0 (
        echo       [错误] 依赖安装失败
        pause
        exit /b 1
    )
)
echo       依赖安装完成 - OK
echo.

:: ============================================
:: Step 3: 检查/安装 Node.js
:: ============================================
echo [3/5] 检查 Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo       Node.js 未安装，尝试自动安装...
    where winget >nul 2>&1
    if %errorlevel% equ 0 (
        echo       使用 winget 安装 Node.js LTS...
        winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements >nul 2>&1
        if %errorlevel% equ 0 (
            echo       Node.js 安装完成 - OK
            echo.
            echo  [提示] Node.js 刚安装完成，PATH 可能未刷新
            echo  请关闭此窗口，重新打开运行本脚本
            pause
            exit /b 0
        )
    )
    where choco >nul 2>&1
    if %errorlevel% equ 0 (
        echo       使用 Chocolatey 安装 Node.js...
        choco install nodejs-lts -y >nul 2>&1
        if %errorlevel% equ 0 (
            echo       Node.js 安装完成 - OK
            echo.
            echo  [提示] 请关闭此窗口，重新打开运行本脚本
            pause
            exit /b 0
        )
    )
    echo.
    echo  [错误] 自动安装失败，请手动安装 Node.js 18+
    echo  国内镜像下载: https://npmmirror.com/mirrors/node/
    echo  安装后重新运行本脚本
    echo.
    pause
    exit /b 1
) else (
    for /f %%i in ('node --version') do echo       Node.js %%i - OK
)
echo.

:: ============================================
:: Step 4: 检查/安装 Claude Code
:: ============================================
echo [4/5] 检查 Claude Code...
where claude >nul 2>&1
if %errorlevel% neq 0 (
    echo       Claude Code 未安装，正在通过 npm 安装...
    echo       使用淘宝镜像，无需 VPN
    npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo  [错误] Claude Code 安装失败
        echo  请检查网络连接后重试
        pause
        exit /b 1
    )
    echo       Claude Code 安装完成 - OK
) else (
    echo       Claude Code 已安装 - OK
)
echo.

:: ============================================
:: Step 5: 配置 DeepSeek API
:: ============================================
echo [5/5] 配置 DeepSeek API...
echo.
echo  请输入你的 DeepSeek API Key
echo  获取地址: https://platform.deepseek.com
echo.
set /p API_KEY="API Key: "

if "%API_KEY%"=="" (
    echo.
    echo  [警告] 未输入 API Key，跳过配置
    echo  稍后可运行: python -m src.main configure
    goto :done
)

:: 保存配置
python -c "import os, yaml; config_dir=os.path.join('%~dp0','config'); os.makedirs(config_dir,exist_ok=True); yaml.dump({'deepseek':{'api_key':'%API_KEY%','base_url_openai':'https://api.deepseek.com/v1','base_url_anthropic':'https://api.deepseek.com/anthropic','model':'deepseek-v4-flash'},'claude_code':{'base_url':'https://api.deepseek.com/anthropic','model':'deepseek-v4-flash'}},open(os.path.join(config_dir,'config.yaml'),'w',encoding='utf-8'),default_flow_style=False,allow_unicode=True)" >nul 2>&1

:: 设置当前会话环境变量
set ANTHROPIC_API_KEY=%API_KEY%
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic

:: 测试连接
echo.
echo       测试 API 连接...
python -c "from openai import OpenAI; c=OpenAI(api_key='%API_KEY%',base_url='https://api.deepseek.com/v1'); c.chat.completions.create(model='deepseek-v4-flash',messages=[{'role':'user','content':'hi'}],max_tokens=5); print('      API 连接成功')" 2>nul
if %errorlevel% neq 0 (
    echo       [警告] API 连接测试失败，请检查 Key 是否正确
)

:done
echo.
echo ========================================
echo.
echo  安装完成！
echo.
echo  使用方法:
echo    1. 设置环境变量:  python -m src.main setup-env
echo    2. 启动 Claude:   claude
echo.
echo  其他命令:
echo    python -m src.main chat          交互式聊天
echo    python -m src.main chat --auto-model  智能模型聊天
echo    python -m src.main show          查看配置
echo    python -m src.main status        系统状态
echo    python launcher.py               GUI 界面
echo.
echo ========================================
echo.
pause
