from typing import Any, Dict
import traceback


class LLMClient:
    """轻量LLM客户端。

    kind: local | service | ollama
    config: 保存与调用所需的最小配置信息
    """

    def __init__(self, kind: str, config: Dict[str, Any]):
        self.kind = kind
        self.config = config or {}

    def translate(self, text: str, target_language: str, system_prompt: str = "") -> str:
        """翻译文本到目标语言"""
        
        # Service类型：使用真实的API connector
        if self.kind == "service" and self.config.get("connector"):
            try:
                # 构建翻译指令的messages
                lang_map = {
                    "英语": "English",
                    "中文": "Chinese",
                    "日语": "Japanese",
                    "韩语": "Korean",
                    "法语": "French",
                    "德语": "German",
                    "西班牙语": "Spanish",
                    "意大利语": "Italian",
                    "俄语": "Russian",
                    "葡萄牙语": "Portuguese",
                }
                target_lang = lang_map.get(target_language, target_language)
                
                # 使用system_prompt（优先使用传入的，否则使用config中的）
                sys_prompt = system_prompt or self.config.get("system_prompt") or "You are a translation engine. Only output the translated text."
                
                messages = [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": f"Translate the following text to {target_lang}. Keep the meaning and style.\n\n{text}"}
                ]
                
                # 调用真实API
                return self.config["connector"].invoke(messages)
                
            except Exception as e:
                error_msg = f"LLM API调用失败: {str(e)}"
                print(error_msg)
                print(traceback.format_exc())
                return error_msg
        
        # Ollama类型：占位实现（可扩展为实际调用）
        elif self.kind == "ollama":
            # TODO: 实现Ollama API调用
            host = self.config.get("host", "localhost:11434")
            model = self.config.get("model", "unknown")
            return f"[Ollama {host}/{model}] -> {target_language}: {text}"
        
        # Local类型：占位实现（可扩展为实际模型加载）
        elif self.kind == "local":
            # TODO: 实现本地模型加载与推理
            path = self.config.get("path", "unknown")
            return f"[Local {path}] -> {target_language}: {text}"
        
        # 未知类型或无connector：返回占位结果
        else:
            provider = self.config.get("provider") or self.kind
            model = self.config.get("model") or self.config.get("path") or self.config.get("host") or "unknown"
            return f"[LLM {provider}/{model}] -> {target_language}: {text}"



