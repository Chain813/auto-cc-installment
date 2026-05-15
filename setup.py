from setuptools import setup, find_packages

setup(
    name="claude-deepseek",
    version="0.1.0",
    description="Claude Code 自动化安装 + DeepSeek API 接入工具",
    author="Chain",
    author_email="Chain813@users.noreply.github.com",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-deepseek=src.main:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
