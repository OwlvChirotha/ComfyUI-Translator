import traceback
from typing import Tuple

from .llm_client import LLMClient
from .llm_connectors import ZhiPuConnector


class ZhiPuServiceConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "model_select": (
                    [
                        "glm-4",
                        "glm-4v",
                        "glm-3-turbo",
                        "Custom",
                    ],
                    {"default": "glm-4"},
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
            
            # 创建 ZhiPu Connector
            connector = ZhiPuConnector(api_key, model)
            
            # 封装到 LLMClient
            config = {
                "provider": "ZhiPu",
                "model": model,
                "api_key": api_key,
                "connector": connector,
            }
            client = LLMClient(kind="service", config=config)
            return (client,)
            
        except Exception as e:
            print("ZhiPuServiceConnectorNode error:", e)
            print(traceback.format_exc())
            client = LLMClient(kind="service", config={"provider": "ZhiPu", "model": model_select, "error": str(e)})
            return (client,)

