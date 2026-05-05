"""智能模型选择器 - 根据任务复杂度自动选择模型"""

from typing import Tuple


class ModelSelector:
    """智能模型选择器"""

    # Flash 模型特征（简单任务）
    FLASH_KEYWORDS = [
        # 简单问答
        "hello", "hi", "hey", "你好", "嗨",
        "what is", "what's", "是什么",
        "yes", "no", "ok", "好的", "是", "否",
        # 简单操作
        "print", "echo", "输出", "显示",
        "run", "execute", "运行", "执行",
        # 格式转换
        "convert", "format", "转换", "格式",
        "json", "csv", "xml", "yaml",
        # 简单代码
        "fix typo", "rename", "rename variable",
        "修复拼写", "重命名",
        # 查询
        "help", "帮助", "usage", "用法",
        "version", "版本",
    ]

    # Pro 模型特征（复杂任务）
    PRO_KEYWORDS = [
        # 架构设计
        "architecture", "design", "架构", "设计",
        "refactor", "重构", "optimize", "优化",
        "implement", "实现",
        # 复杂逻辑
        "algorithm", "算法", "complex", "复杂",
        "recursive", "递归", "dynamic programming", "动态规划",
        # 系统设计
        "database", "数据库", "api design", "API设计",
        "microservice", "微服务", "distributed", "分布式",
        # 代码审查
        "review", "审查", "security", "安全",
        "performance", "性能", "bottleneck", "瓶颈",
        # 多文件操作
        "refactor all", "重构所有",
        "multiple files", "多个文件",
        "entire project", "整个项目",
        # 调试
        "debug", "调试", "troubleshoot", "排查",
        "root cause", "根本原因", "investigate", "调查",
        # 文档生成
        "documentation", "文档", "readme", "changelog",
        "write tests", "编写测试", "test suite", "测试套件",
    ]

    @classmethod
    def select_model(cls, message: str) -> Tuple[str, str]:
        """
        根据用户消息选择合适的模型

        Args:
            message: 用户输入的消息

        Returns:
            Tuple[model_name, reason]: 模型名称和选择原因
        """
        message_lower = message.lower().strip()

        # 计算匹配分数
        flash_score = 0
        pro_score = 0

        # 检查 Flash 特征
        for keyword in cls.FLASH_KEYWORDS:
            if keyword in message_lower:
                flash_score += 1

        # 检查 Pro 特征
        for keyword in cls.PRO_KEYWORDS:
            if keyword in message_lower:
                pro_score += 1

        # 基于消息长度的启发式规则
        word_count = len(message.split())

        # 短消息倾向于使用 Flash
        if word_count <= 5:
            flash_score += 2
        elif word_count <= 10:
            flash_score += 1

        # 长消息倾向于使用 Pro
        if word_count > 30:
            pro_score += 3
        elif word_count > 20:
            pro_score += 2
        elif word_count > 15:
            pro_score += 1

        # 检查是否包含代码块
        if "```" in message or "def " in message or "class " in message:
            pro_score += 2

        # 检查是否是多行消息
        line_count = message.count('\n') + 1
        if line_count > 10:
            pro_score += 2
        elif line_count > 5:
            pro_score += 1

        # 检查问号数量（复杂问题）
        question_marks = message.count('?') + message.count('？')
        if question_marks > 2:
            pro_score += 1

        # 决策
        if pro_score > flash_score:
            return "deepseek-v4-pro", f"复杂任务 (复杂度评分: {pro_score})"
        else:
            return "deepseek-v4-flash", f"简单任务 (复杂度评分: {flash_score})"

    @classmethod
    def get_model_info(cls, model: str) -> dict:
        """获取模型信息"""
        models = {
            "deepseek-v4-flash": {
                "name": "DeepSeek V4 Flash",
                "description": "快速模型，适合简单任务",
                "speed": "快",
                "capability": "基础"
            },
            "deepseek-v4-pro": {
                "name": "DeepSeek V4 Pro",
                "description": "专业模型，适合复杂任务",
                "speed": "慢",
                "capability": "高级"
            }
        }
        return models.get(model, models["deepseek-v4-flash"])


def auto_select_model(message: str) -> Tuple[str, str]:
    """
    便捷函数：自动选择模型

    Args:
        message: 用户消息

    Returns:
        Tuple[model_name, reason]
    """
    return ModelSelector.select_model(message)


if __name__ == "__main__":
    # 测试
    test_cases = [
        "hello",
        "what is Python?",
        "请帮我重构整个项目的架构，包括数据库设计和API设计",
        "fix typo in variable name",
        "请帮我写一个复杂的分布式系统，需要处理并发和容错",
        "run the tests",
        "请帮我调试这个bug，根本原因是什么？",
        "ok",
        "请帮我实现一个递归算法，解决动态规划问题",
        "help",
    ]

    print("=" * 60)
    print("智能模型选择器测试")
    print("=" * 60)
    print()

    for msg in test_cases:
        model, reason = auto_select_model(msg)
        print(f"输入: {msg[:40]}...")
        print(f"选择: {model}")
        print(f"原因: {reason}")
        print("-" * 40)
