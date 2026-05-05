"""DeepSeek API 客户端模块"""

from typing import Optional, List, Dict, Generator
from openai import OpenAI
from rich.console import Console
from .api_config import APIConfig
from .model_selector import auto_select_model, ModelSelector
from .utils import print_error, print_success, print_info

console = Console()


class DeepSeekClient:
    """DeepSeek API 客户端"""

    def __init__(self, config: Optional[APIConfig] = None):
        self.config = config or APIConfig()
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """初始化 OpenAI 客户端"""
        api_key = self.config.get_api_key()
        base_url = self.config.get_base_url()

        if not api_key:
            print_error("DeepSeek API Key 未配置")
            print_info("请运行 'python -m src.main configure' 进行配置")
            return

        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except Exception as e:
            print_error(f"客户端初始化失败: {e}")

    def get_available_models(self) -> dict:
        """获取可用模型列表"""
        return {
            "flash": "deepseek-v4-flash",
            "pro": "deepseek-v4-pro"
        }

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return self.client is not None

    def test_connection(self) -> bool:
        """测试 API 连接"""
        if not self.is_configured():
            return False

        try:
            self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print_success("API 连接测试成功")
            return True
        except Exception as e:
            print_error(f"API 连接测试失败: {e}")
            return False

    def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        stream: bool = False
    ) -> Optional[str]:
        """发送聊天消息"""
        if not self.is_configured():
            print_error("客户端未初始化")
            return None

        messages = history or []
        messages.append({"role": "user", "content": message})

        try:
            if stream:
                return self._chat_stream(messages)
            else:
                return self._chat_sync(messages)
        except Exception as e:
            print_error(f"请求失败: {e}")
            return None

    def _chat_sync(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """同步聊天"""
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=messages,
                max_tokens=2048,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print_error(f"请求失败: {e}")
            return None

    def _chat_stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """流式聊天"""
        try:
            stream = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print_error(f"流式请求失败: {e}")

    def _chat_stream_with_model(self, messages: List[Dict[str, str]], model: str) -> Generator[str, None, None]:
        """使用指定模型的流式聊天"""
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print_error(f"流式请求失败: {e}")

    def interactive_chat(self):
        """交互式聊天"""
        if not self.is_configured():
            print_error("请先配置 API Key")
            print_info("运行 'python -m src.main configure' 进行配置")
            return

        console.print("\n[bold blue]=== DeepSeek 交互式聊天 ===[/bold blue]")
        console.print("[dim]输入 'quit' 或 'exit' 退出[/dim]\n")

        history = []

        while True:
            try:
                user_input = console.input("[bold green]你: [/bold green]")

                if user_input.lower() in ["quit", "exit", "q"]:
                    console.print("\n[dim]再见！[/dim]")
                    break

                if not user_input.strip():
                    continue

                history.append({"role": "user", "content": user_input})

                console.print("\n[bold cyan]助手: [/bold cyan]", end="")

                # 使用流式输出
                full_response = ""
                for chunk in self._chat_stream(history):
                    console.print(chunk, end="")
                    full_response += chunk

                console.print("\n")
                history.append({"role": "assistant", "content": full_response})

            except KeyboardInterrupt:
                console.print("\n\n[dim]再见！[/dim]")
                break
            except Exception as e:
                print_error(f"\n错误: {e}")

    def interactive_chat_with_auto_model(self):
        """交互式聊天（智能模型选择）"""
        if not self.is_configured():
            print_error("请先配置 API Key")
            print_info("运行 'python -m src.main configure' 进行配置")
            return

        console.print("\n[bold blue]=== DeepSeek 智能聊天 ===[/bold blue]")
        console.print("[dim]输入 'quit' 或 'exit' 退出[/dim]")
        console.print("[dim]系统将根据任务复杂度自动选择 flash/pro 模型[/dim]\n")

        history = []
        total_tokens = {"flash": 0, "pro": 0}

        while True:
            try:
                user_input = console.input("[bold green]你: [/bold green]")

                if user_input.lower() in ["quit", "exit", "q"]:
                    console.print("\n[dim]再见！[/dim]")
                    # 显示统计
                    if total_tokens["flash"] + total_tokens["pro"] > 0:
                        console.print("\n[dim]本次会话模型使用统计:[/dim]")
                        console.print(f"[dim]  Flash: {total_tokens['flash']} 次[/dim]")
                        console.print(f"[dim]  Pro:   {total_tokens['pro']} 次[/dim]")
                    break

                if not user_input.strip():
                    continue

                # 智能选择模型
                model, reason = auto_select_model(user_input)
                model_info = ModelSelector.get_model_info(model)

                # 显示选择的模型（灰色小字）
                console.print(f"[dim]  -> 使用模型: {model_info['name']} ({reason})[/dim]")

                history.append({"role": "user", "content": user_input})

                console.print("[bold cyan]助手: [/bold cyan]", end="")

                # 使用指定模型的流式输出
                full_response = ""
                for chunk in self._chat_stream_with_model(history, model):
                    console.print(chunk, end="")
                    full_response += chunk

                console.print("\n")
                history.append({"role": "assistant", "content": full_response})

                # 更新统计
                if "flash" in model:
                    total_tokens["flash"] += 1
                else:
                    total_tokens["pro"] += 1

            except KeyboardInterrupt:
                console.print("\n\n[dim]再见！[/dim]")
                break
            except Exception as e:
                print_error(f"\n错误: {e}")
