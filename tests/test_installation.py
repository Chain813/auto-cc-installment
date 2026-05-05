"""安装测试脚本"""

import sys
import unittest
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.installer import ClaudeCodeInstaller
from src.api_config import APIConfig
from src.utils import get_os_type, check_command_exists


class TestInstallation(unittest.TestCase):
    """安装测试"""

    def setUp(self):
        self.installer = ClaudeCodeInstaller()
        self.config = APIConfig()

    def test_os_detection(self):
        """测试操作系统检测"""
        os_type = get_os_type()
        self.assertIn(os_type, ["windows", "macos", "linux"])

    def test_nodejs_check(self):
        """测试 Node.js 检测"""
        # 这个测试依赖于系统环境
        result = self.installer.check_nodejs()
        self.assertIsInstance(result, bool)

    def test_npm_check(self):
        """测试 npm 检测"""
        result = self.installer.check_npm()
        self.assertIsInstance(result, bool)

    def test_config_load(self):
        """测试配置加载"""
        config = self.config.load_config()
        self.assertIsInstance(config, dict)
        self.assertIn("deepseek", config)
        self.assertIn("claude", config)
        self.assertIn("general", config)

    def test_config_defaults(self):
        """测试默认配置"""
        config = self.config.DEFAULT_CONFIG
        self.assertEqual(config["deepseek"]["base_url"], "https://api.deepseek.com/v1")
        self.assertEqual(config["deepseek"]["model"], "deepseek-chat")
        self.assertEqual(config["general"]["timeout"], 30)


if __name__ == "__main__":
    unittest.main()
