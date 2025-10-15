from .basic_translator_node import TranslatorNode
from .llm_translator_node import LLMTranslatorNode
from .llm_model_loader_node import LLMLocalModelLoaderNode
from .general_llm_service_connector_node import GeneralLLMServiceConnectorNode
from .ollama_llm_connector_node import OllamaLLMConnectorNode
# 专用服务商连接器
from .siliconflow_connector_node import SiliconFlowServiceConnectorNode
from .zhipu_connector_node import ZhiPuServiceConnectorNode
from .deepseek_connector_node import DeepSeekServiceConnectorNode
from .kimi_connector_node import KimiServiceConnectorNode
from .gemini_connector_node import GeminiServiceConnectorNode
from .chatgpt_connector_node import ChatGPTServiceConnectorNode

def brand(name: str) -> str:
    return f"{name} 🦉| OwlV"

NODE_CLASS_MAPPINGS = {
    "TranslatorNode": TranslatorNode,
    "LLMTranslatorNode": LLMTranslatorNode,
    "LLMLocalModelLoaderNode": LLMLocalModelLoaderNode,
    "GeneralLLMServiceConnectorNode": GeneralLLMServiceConnectorNode,
    "OllamaLLMConnectorNode": OllamaLLMConnectorNode,
    # 专用服务商连接器
    "SiliconFlowServiceConnectorNode": SiliconFlowServiceConnectorNode,
    "ZhiPuServiceConnectorNode": ZhiPuServiceConnectorNode,
    "DeepSeekServiceConnectorNode": DeepSeekServiceConnectorNode,
    "KimiServiceConnectorNode": KimiServiceConnectorNode,
    "GeminiServiceConnectorNode": GeminiServiceConnectorNode,
    "ChatGPTServiceConnectorNode": ChatGPTServiceConnectorNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TranslatorNode": brand("Basic Translator"),
    "LLMTranslatorNode": brand("LLM Translator"),
    "LLMLocalModelLoaderNode": brand("Load LLM Model"),
    "GeneralLLMServiceConnectorNode": brand("General LLM Service Connector"),
    "OllamaLLMConnectorNode": brand("Ollama LLM Connector"),
    # 专用服务商连接器
    "SiliconFlowServiceConnectorNode": brand("SiliconFlow Service Connector"),
    "ZhiPuServiceConnectorNode": brand("ZhiPu Service Connector"),
    "DeepSeekServiceConnectorNode": brand("DeepSeek Service Connector"),
    "KimiServiceConnectorNode": brand("Kimi Service Connector"),
    "GeminiServiceConnectorNode": brand("Gemini Service Connector"),
    "ChatGPTServiceConnectorNode": brand("ChatGPT Service Connector"),
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
