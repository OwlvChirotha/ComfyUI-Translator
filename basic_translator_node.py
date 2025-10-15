from googletrans import Translator
import requests
import hashlib
import time
import traceback

class TranslatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "target_language": (["英语", "中文", "日语", "韩语", "法语", "德语", "西班牙语", "意大利语", "俄语", "葡萄牙语"], {
                    "default": "英语"
                }),
                "translator_service": (["Google翻译", "百度翻译", "有道翻译", "腾讯翻译"], {
                    "default": "Google翻译"
                }),
            },
            "optional": {
                "baidu_app_id": ("STRING", {"default": ""}),
                "baidu_secret_key": ("STRING", {"default": ""}),
                "youdao_app_id": ("STRING", {"default": ""}),
                "youdao_secret_key": ("STRING", {"default": ""}),
                "tencent_secret_id": ("STRING", {"default": ""}),
                "tencent_secret_key": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "Text Processing"
    
    def translate(self, text, target_language, translator_service, 
                  baidu_app_id="", baidu_secret_key="", 
                  youdao_app_id="", youdao_secret_key="", 
                  tencent_secret_id="", tencent_secret_key=""):
        # 语言映射字典 - 支持多个翻译服务的语言代码
        language_map = {
            "英语": {"google": "en", "baidu": "en", "youdao": "en", "tencent": "en"},
            "中文": {"google": "zh-cn", "baidu": "zh", "youdao": "zh-CHS", "tencent": "zh"},
            "日语": {"google": "ja", "baidu": "jp", "youdao": "ja", "tencent": "ja"},
            "韩语": {"google": "ko", "baidu": "kor", "youdao": "ko", "tencent": "ko"},
            "法语": {"google": "fr", "baidu": "fra", "youdao": "fr", "tencent": "fr"},
            "德语": {"google": "de", "baidu": "de", "youdao": "de", "tencent": "de"},
            "西班牙语": {"google": "es", "baidu": "spa", "youdao": "es", "tencent": "es"},
            "意大利语": {"google": "it", "baidu": "it", "youdao": "it", "tencent": "it"},
            "俄语": {"google": "ru", "baidu": "ru", "youdao": "ru", "tencent": "ru"},
            "葡萄牙语": {"google": "pt", "baidu": "pt", "youdao": "pt", "tencent": "pt"}
        }
        
        if not text or not text.strip():
            return ("",)
        
        try:
            # 获取目标语言代码
            target_lang = language_map.get(target_language, {
                "google": "en", "baidu": "en", "youdao": "en", "tencent": "en"
            })
            
            # 根据选择的翻译服务调用对应的方法
            if translator_service == "Google翻译":
                return self._google_translate(text, target_lang["google"])
            elif translator_service == "百度翻译":
                if not baidu_app_id or not baidu_secret_key:
                    return ("百度翻译需要填写App ID和密钥，请在可选参数中配置",)
                return self._baidu_translate(text, target_lang["baidu"], baidu_app_id, baidu_secret_key)
            elif translator_service == "有道翻译":
                if not youdao_app_id or not youdao_secret_key:
                    return ("有道翻译需要填写App ID和密钥，请在可选参数中配置",)
                return self._youdao_translate(text, target_lang["youdao"], youdao_app_id, youdao_secret_key)
            elif translator_service == "腾讯翻译":
                if not tencent_secret_id or not tencent_secret_key:
                    return ("腾讯翻译需要填写Secret ID和密钥，请在可选参数中配置",)
                return self._tencent_translate(text, target_lang["tencent"], tencent_secret_id, tencent_secret_key)
            else:
                return ("不支持的翻译服务",)
                
        except Exception as e:
            error_msg = f"翻译失败: {str(e)}"
            print(f"翻译节点错误: {error_msg}")
            print(f"错误详情: {traceback.format_exc()}")
            return (error_msg,)
    
    def _google_translate(self, text, target_lang):
        """Google翻译 - 适用于国际网络环境"""
        translator = Translator()
        result = translator.translate(text, dest=target_lang)
        return (result.text,)
    
    def _baidu_translate(self, text, target_lang, app_id, secret_key):
        """百度翻译 - 适用于中国大陆网络环境"""
        # 生成签名
        salt = str(int(time.time() * 1000))
        sign_str = app_id + text + salt + secret_key
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        # 构建请求
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        params = {
            'q': text,
            'from': 'auto',
            'to': target_lang,
            'appid': app_id,
            'salt': salt,
            'sign': sign
        }
        
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if 'trans_result' in result:
            return (result['trans_result'][0]['dst'],)
        else:
            error_code = result.get('error_code', '未知')
            error_msg = result.get('error_msg', '未知错误')
            return (f"百度翻译错误 [{error_code}]: {error_msg}",)
    
    def _youdao_translate(self, text, target_lang, app_id, secret_key):
        """有道翻译 - 适用于中国大陆网络环境"""
        # 生成签名
        salt = str(int(time.time() * 1000))
        curtime = str(int(time.time()))
        sign_str = app_id + self._truncate(text) + salt + curtime + secret_key
        sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
        
        # 构建请求
        url = "https://openapi.youdao.com/api"
        data = {
            'q': text,
            'from': 'auto',
            'to': target_lang,
            'appKey': app_id,
            'salt': salt,
            'sign': sign,
            'signType': 'v3',
            'curtime': curtime
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('errorCode') == '0':
            return (result['translation'][0],)
        else:
            error_code = result.get('errorCode', '未知')
            return (f"有道翻译错误代码: {error_code}",)
    
    def _tencent_translate(self, text, target_lang, secret_id, secret_key):
        """腾讯翻译 - 需要腾讯云SDK，当前为基础框架"""
        # 注意：完整实现需要腾讯云SDK和复杂的签名算法
        # 这里提供基础框架，实际使用建议安装 tencentcloud-sdk-python
        return ("腾讯翻译功能需要安装腾讯云SDK，建议使用百度或有道翻译",)
    
    def _truncate(self, q):
        """有道翻译签名需要的文本截断方法"""
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
