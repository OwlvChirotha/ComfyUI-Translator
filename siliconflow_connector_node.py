import traceback
from typing import Tuple

from .llm_client import LLMClient
from .llm_connectors import SiliconFlowConnector


class SiliconFlowServiceConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "model_select": (
                    [
                        "deepseek-ai/DeepSeek-V3",
                        "THUDM/GLM-Z1-9B-0414",
                        "THUDM/GLM-4-32B-0414",
                        "Qwen/Qwen3-8B",
                        "moonshotai/Kimi-K2-Instruct",
                        "Custom",
                    ],
                    {"default": "THUDM/GLM-4-32B-0414"},
                ),
            },
            "optional": {
                "custom_model_id": (
                    "STRING",
                    {
                        "default": "",
                        "placeholder": "Enter custom model ID (used when model_select is 'Custom')",
                    },
                ),
            },
        }

    RETURN_TYPES = ("LLM",)
    RETURN_NAMES = ("llm",)
    FUNCTION = "execute"
    CATEGORY = "Text Processing/LLM"

    def execute(self, api_key: str, model_select: str, custom_model_id: str = "") -> Tuple[object]:
        try:
            # 确定最终使用的模型
            model = custom_model_id if model_select == "Custom" and custom_model_id.strip() else model_select
            
            # 创建 SiliconFlow Connector
            connector = SiliconFlowConnector(api_key, model)
            
            # 封装到 LLMClient
            config = {
                "provider": "SiliconFlow",
                "model": model,
                "api_key": api_key,
                "connector": connector,
            }
            client = LLMClient(kind="service", config=config)
            return (client,)
            
        except Exception as e:
            print("SiliconFlowServiceConnectorNode error:", e)
            print(traceback.format_exc())
            # 返回错误状态的客户端
            client = LLMClient(kind="service", config={"provider": "SiliconFlow", "model": model_select, "error": str(e)})
            return (client,)

