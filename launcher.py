#!/usr/bin/env python3
"""
Claude Code + DeepSeek 一键部署工具
启动入口
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import main

if __name__ == "__main__":
    main()
