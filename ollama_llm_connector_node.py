import traceback
from typing import Tuple

from .llm_client import LLMClient


class OllamaLLMConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "host": ("STRING", {"default": "http://localhost:11434"}),
                "model": ("STRING", {"default": "llama3:8b"}),
            },
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "system_prompt": ("STRING", {"default": "You are a translation engine. Only output the translated text.", "multiline": True}),
            }
        }

    RETURN_TYPES = ("LLM",)
    RETURN_NAMES = ("llm",)
    FUNCTION = "connect"
    CATEGORY = "Text Processing/LLM"

    def connect(self, host: str, model: str, api_key: str = "", system_prompt: str = "") -> Tuple[object]:
        try:
            config = {
                "host": host,
                "model": model,
                "api_key": api_key,
                "system_prompt": system_prompt,
            }
            client = LLMClient(kind="ollama", config=config)
            return (client,)
        except Exception as e:
            print("OllamaLLMConnectorNode error:", e)
            print(traceback.format_exc())
            client = LLMClient(kind="ollama", config={"host": host, "model": model, "error": str(e)})
            return (client,)



