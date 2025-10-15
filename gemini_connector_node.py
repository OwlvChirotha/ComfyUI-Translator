import traceback
import requests
from typing import Tuple

from .llm_client import LLMClient
from .llm_connectors import GeneralLLMServiceConnector


class GeminiConnector(GeneralLLMServiceConnector):
    """Google Gemini API 连接器"""
    
    def __init__(self, api_token, model):
        # Gemini API URL 格式特殊，需要包含 API key
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_token}"
        super().__init__(url, api_token, model)

    def generate_payload(self, messages, **kwargs):
        # 将 messages 转换为 Gemini 格式
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        return {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", 512),
                "temperature": kwargs.get("temperature", 0.7),
                "topP": kwargs.get("top_p", 0.9),
            }
        }

    def invoke(self, messages, **kwargs):
        """Gemini API 使用不同的请求格式"""
        payload = self.generate_payload(messages, **kwargs)
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    return response_data["candidates"][0]["content"]["parts"][0]["text"]
                except KeyError:
                    raise ValueError("Unexpected response format: missing 'candidates[0].content.parts[0].text'.")
            elif response.status_code == 401:
                raise Exception("Unauthorized: invalid or missing API key.")
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")


class GeminiServiceConnectorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "model_select": (
                    [
                        "gemini-1.5-pro",
                        "gemini-1.5-flash",
                        "gemini-2.0-flash-exp",
                        "Custom",
                    ],
                    {"default": "gemini-1.5-flash"},
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
            
            # 创建 Gemini Connector
            connector = GeminiConnector(api_key, model)
            
            # 封装到 LLMClient
            config = {
                "provider": "Gemini",
                "model": model,
                "api_key": api_key,
                "connector": connector,
            }
            client = LLMClient(kind="service", config=config)
            return (client,)
            
        except Exception as e:
            print("GeminiServiceConnectorNode error:", e)
            print(traceback.format_exc())
            client = LLMClient(kind="service", config={"provider": "Gemini", "model": model_select, "error": str(e)})
            return (client,)

