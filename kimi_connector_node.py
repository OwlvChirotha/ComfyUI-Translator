import traceback
from typing import Tuple

from .llm_client import LLMClient
from .llm_connectors import MoonshotConnector


class KimiServiceConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "model_select": (
                    [
                        "moonshot-v1-8k",
                        "moonshot-v1-32k",
                        "moonshot-v1-128k",
                        "kimi-v1",
                        "Custom",
                    ],
                    {"default": "moonshot-v1-32k"},
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
            
            # 创建 Moonshot Connector (Kimi)
            connector = MoonshotConnector(api_key, model)
            
            # 封装到 LLMClient
            config = {
                "provider": "Kimi",
                "model": model,
                "api_key": api_key,
                "connector": connector,
            }
            client = LLMClient(kind="service", config=config)
            return (client,)
            
        except Exception as e:
            print("KimiServiceConnectorNode error:", e)
            print(traceback.format_exc())
            client = LLMClient(kind="service", config={"provider": "Kimi", "model": model_select, "error": str(e)})
            return (client,)

