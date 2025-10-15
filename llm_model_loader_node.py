import os
import traceback
from typing import Tuple

from .llm_client import LLMClient


class LLMLocalModelLoaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source": (["ComfyUI models/LLM", "自定义目录"], {"default": "ComfyUI models/LLM"}),
                "custom_path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("LLM",)
    RETURN_NAMES = ("llm",)
    FUNCTION = "load"
    CATEGORY = "Text Processing/LLM"

    def load(self, source: str, custom_path: str) -> Tuple[object]:
        try:
            if source == "自定义目录" and custom_path and custom_path.strip():
                model_dir = custom_path.strip()
            else:
                # 定位到 ComfyUI 根目录，再拼接 models/LLM
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
                model_dir = os.path.join(base_dir, "models", "LLM")

            # 仅做存在性检查
            exists = os.path.isdir(model_dir)
            config = {"path": model_dir, "exists": exists}
            client = LLMClient(kind="local", config=config)
            return (client,)
        except Exception as e:
            print("LLMLocalModelLoaderNode error:", e)
            print(traceback.format_exc())
            # 返回一个占位对象，避免阻塞流程
            client = LLMClient(kind="local", config={"path": custom_path or "", "error": str(e)})
            return (client,)



