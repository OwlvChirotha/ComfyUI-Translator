import traceback
from typing import Tuple

from .llm_client import LLMClient
from .llm_connectors import GeneralLLMServiceConnector


class GeneralLLMServiceConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_url": ("STRING", {
                    "default": "https://api.openai.com/v1/chat/completions",
                    "placeholder": "Enter OpenAI-compatible API endpoint URL"
                }),
                "api_key": ("STRING", {"default": "", "password": True}),
                "model": (["Custom Model", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "o1", "o1-mini", "claude-3-5-sonnet", "claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "deepseek-chat", "deepseek-coder", "deepseek-v3", "deepseek-r1", "moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k", "kimi-v1", "glm-4", "glm-4v", "glm-3-turbo", "qwen-turbo", "qwen-plus", "qwen-max", "qwen2.5-7b", "qwen2.5-14b", "qwen2.5-32b", "qwen2.5-72b", "grok-2", "grok-1"], {"default": "gpt-4o-mini"}),
            },
            "optional": {
                "custom_model": ("STRING", {
                    "default": "",
                    "placeholder": "Enter custom model name (used when model is 'Custom Model')"
                }),
            }
        }

    RETURN_TYPES = ("LLM",)
    RETURN_NAMES = ("llm",)
    FUNCTION = "connect"
    CATEGORY = "Text Processing/LLM"

    def connect(self, api_url: str, api_key: str, model: str, custom_model: str = "") -> Tuple[object]:
        try:
            # 确定最终使用的模型名称
            final_model = custom_model.strip() if model == "Custom Model" and custom_model.strip() else model
            
            # 创建通用的OpenAI兼容连接器
            connector = GeneralLLMServiceConnector(api_url, api_key, final_model)
            
            config = {
                "provider": "General",
                "model": final_model,
                "api_url": api_url,
                "api_key": api_key,
                "connector": connector,
            }
            client = LLMClient(kind="service", config=config)
            return (client,)
            
        except Exception as e:
            print("GeneralLLMServiceConnectorNode error:", e)
            print(traceback.format_exc())
            client = LLMClient(kind="service", config={"provider": "General", "model": final_model, "error": str(e)})
            return (client,)



