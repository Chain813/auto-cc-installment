#!/usr/bin/env python3
"""
Claude Code + DeepSeek 一键部署工具
启动入口
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 自动检查依赖
def check_deps():
    required = ["yaml", "requests", "rich", "click", "openai"]
    missing = []
    import importlib.util
    for lib in required:
        # 特殊处理 pyyaml
        search_name = "yaml" if lib == "yaml" else lib
        if importlib.util.find_spec(search_name) is None:
            missing.append(lib)
    
    if missing:
        import subprocess
        req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        if os.path.exists(req_file):
            subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "-r", req_file])

if __name__ == "__main__":
    check_deps()
    from src.gui import main
    main()
