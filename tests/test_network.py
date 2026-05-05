"""网络连接测试"""

import unittest
import requests
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNetworkConnection(unittest.TestCase):
    """网络连接测试"""

    DEEPSEEK_API_URL = "https://api.deepseek.com"
    NODEJS_URL = "https://nodejs.org"
    NPM_REGISTRY_URL = "https://registry.npmjs.org"

    def test_deepseek_api_accessible(self):
        """测试 DeepSeek API 是否可访问"""
        try:
            response = requests.get(self.DEEPSEEK_API_URL, timeout=10)
            # 只要能连接上就行，不检查状态码
            self.assertTrue(True)
        except requests.exceptions.RequestException as e:
            self.fail(f"无法访问 DeepSeek API: {e}")

    def test_nodejs_website_accessible(self):
        """测试 Node.js 官网是否可访问"""
        try:
            response = requests.get(self.NODEJS_URL, timeout=10)
            self.assertTrue(True)
        except requests.exceptions.RequestException as e:
            self.fail(f"无法访问 Node.js 官网: {e}")

    def test_npm_registry_accessible(self):
        """测试 npm 注册表是否可访问"""
        try:
            response = requests.get(self.NPM_REGISTRY_URL, timeout=10)
            self.assertTrue(True)
        except requests.exceptions.RequestException as e:
            self.fail(f"无法访问 npm 注册表: {e}")

    def test_no_proxy_environment(self):
        """测试没有设置代理环境变量"""
        import os
        proxy_vars = [
            'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
            'ALL_PROXY', 'all_proxy'
        ]
        for var in proxy_vars:
            value = os.environ.get(var)
            if value:
                print(f"警告: 检测到代理环境变量 {var}={value}")


if __name__ == "__main__":
    unittest.main()
