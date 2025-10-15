import traceback
from typing import Tuple


class LLMTranslatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm": ("LLM", {}),
                "text": ("STRING", {"multiline": True, "default": ""}),
                "target_language": (["英语", "中文", "日语", "韩语", "法语", "德语", "西班牙语", "意大利语", "俄语", "葡萄牙语"], {"default": "英语"}),
            },
            "optional": {
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a translation engine. Only output the translated text."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "Text Processing/LLM"

    def translate(self, llm, text: str, target_language: str, system_prompt: str = "") -> Tuple[str]:
        if not text or not text.strip():
            return ("",)

        try:
            result = llm.translate(text=text, target_language=target_language, system_prompt=system_prompt)
            return (result,)
        except Exception as e:
            print("LLMTranslatorNode error:", e)
            print(traceback.format_exc())
            return (f"LLM 翻译失败: {e}",)


