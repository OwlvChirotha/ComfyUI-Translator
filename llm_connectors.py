import requests


class GeneralLLMServiceConnector:
    """通用LLM服务连接器基类"""
    
    def __init__(self, api_url, api_token, model, timeout=30):
        self.api_url = api_url
        self.api_token = api_token
        self.model = model
        self.timeout = timeout

    def generate_payload(self, messages, **kwargs):
        """生成请求载荷，子类可重写以自定义参数"""
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "response_format": {"type": "text"},
        }

    def invoke(self, messages, **kwargs):
        """调用LLM API"""
        payload = self.generate_payload(messages, **kwargs)
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    return response_data["choices"][0]["message"]["content"]
                except KeyError:
                    raise ValueError("Unexpected response format: missing 'content'.")
            elif response.status_code == 401:
                raise Exception("Unauthorized: invalid or missing API token.")
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")

    def get_state(self):
        """返回用于比较状态的字符串表示（不包含token以避免泄露）"""
        return f"{self.api_url}|{self.model}"


class SiliconFlowConnector(GeneralLLMServiceConnector):
    """SiliconFlow API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://api.siliconflow.cn/v1/chat/completions", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 50),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
            "n": kwargs.get("n", 1),
            "response_format": {"type": "text"},
        }


class ZhiPuConnector(GeneralLLMServiceConnector):
    """智谱AI (ZhiPu) API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://open.bigmodel.cn/api/paas/v4/chat/completions", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
            "n": kwargs.get("n", 1),
            "response_format": {"type": "text"},
        }


class MoonshotConnector(GeneralLLMServiceConnector):
    """Moonshot (Kimi) API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://api.moonshot.cn/v1/chat/completions", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
            "n": kwargs.get("n", 1),
            "response_format": {"type": "text"},
        }


class DeepSeekConnector(GeneralLLMServiceConnector):
    """DeepSeek API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://api.deepseek.com/chat/completions", api_token, model)


class OpenAIConnector(GeneralLLMServiceConnector):
    """OpenAI API 连接器"""
    
    def __init__(self, api_token, model, api_base=None):
        url = api_base or "https://api.openai.com/v1/chat/completions"
        super().__init__(url, api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
        }


class AzureOpenAIConnector(GeneralLLMServiceConnector):
    """Azure OpenAI API 连接器"""
    
    def __init__(self, api_token, model, api_base):
        if not api_base:
            raise ValueError("Azure OpenAI requires api_base (endpoint URL)")
        super().__init__(api_base, api_token, model)
    
    def invoke(self, messages, **kwargs):
        """Azure使用api-key header而非Bearer token"""
        payload = self.generate_payload(messages, **kwargs)
        headers = {
            "api-key": self.api_token,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    return response_data["choices"][0]["message"]["content"]
                except KeyError:
                    raise ValueError("Unexpected response format: missing 'content'.")
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds.")


class QwenConnector(GeneralLLMServiceConnector):
    """通义千问 (Qwen) API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "max_tokens": kwargs.get("max_tokens", 512),
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
            }
        }

    def invoke(self, messages, **kwargs):
        """Qwen API 使用不同的响应格式"""
        payload = self.generate_payload(messages, **kwargs)
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    return response_data["output"]["text"]
                except KeyError:
                    raise ValueError("Unexpected response format: missing 'output.text'.")
            elif response.status_code == 401:
                raise Exception("Unauthorized: invalid or missing API token.")
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")


class ClaudeConnector(GeneralLLMServiceConnector):
    """Anthropic Claude API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://api.anthropic.com/v1/messages", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 512),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
        }

    def invoke(self, messages, **kwargs):
        """Claude API 使用不同的请求格式"""
        payload = self.generate_payload(messages, **kwargs)
        headers = {
            "x-api-key": self.api_token,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    return response_data["content"][0]["text"]
                except KeyError:
                    raise ValueError("Unexpected response format: missing 'content[0].text'.")
            elif response.status_code == 401:
                raise Exception("Unauthorized: invalid or missing API key.")
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")


class GrokConnector(GeneralLLMServiceConnector):
    """xAI Grok API 连接器"""
    
    def __init__(self, api_token, model):
        super().__init__("https://api.x.ai/v1/chat/completions", api_token, model)

    def generate_payload(self, messages, **kwargs):
        return {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
        }