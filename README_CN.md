# ComfyUI 翻译节点集合

这是一个为 ComfyUI 设计的自定义翻译节点集合，提供传统机器翻译和大语言模型翻译两种方案。

## 节点列表

### 1. Basic Translator （基础翻译器）
支持 Google/百度/有道/腾讯 的传统机器翻译服务

### 2. LLM Translator （大语言模型翻译器）
基于大语言模型的高质量翻译，需要配合以下节点使用：
- **Load LLM Model** - 加载本地大语言模型
- **General LLM Service Connector** - OpenAI兼容API网关连接器（支持私有网关）
- **专用服务商连接器** - 各服务商专用连接器：
  - SiliconFlow Service Connector
  - ZhiPu Service Connector（智谱AI）
  - DeepSeek Service Connector
  - Kimi Service Connector（月之暗面）
  - Gemini Service Connector（谷歌）
  - ChatGPT Service Connector（OpenAI）
- **Ollama LLM Connector** - 通过Ollama调用模型

## 功能特点

### Basic Translator
- **多翻译服务支持**：Google翻译、百度翻译、有道翻译、腾讯翻译
- **文本输入**：支持多行文本输入，可手动输入或连接上游节点
- **目标语言选择**：提供10种常用语言的下拉选择框
- **API密钥配置**：可选的API密钥输入，支持国内翻译服务
- **错误处理**：完善的异常处理机制

### LLM Translator
- **多服务商支持**：OpenAI、Claude、DeepSeek、Qwen、Grok等9个主流LLM服务商
- **本地模型支持**：可加载本地部署的大语言模型
- **Ollama集成**：支持通过Ollama调用本地或远程模型
- **灵活配置**：可自定义system prompt和模型参数

## 支持的语言

- 英语 (English)
- 中文 (Chinese)
- 日语 (Japanese) 
- 韩语 (Korean)
- 法语 (French)
- 德语 (German)
- 西班牙语 (Spanish)
- 意大利语 (Italian)
- 俄语 (Russian)
- 葡萄牙语 (Portuguese)

## 安装方法

1. 将整个文件夹复制到 ComfyUI 的 `custom_nodes` 目录下
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 重启 ComfyUI

## 使用方法

### Basic Translator 使用指南

1. 在 ComfyUI 的节点菜单中找到"Text Processing"分类
2. 添加"Basic Translator"节点到工作流
3. 输入需要翻译的文本（手动输入或连接上游节点）
4. 选择目标语言
5. 选择翻译服务
6. 执行工作流获取翻译结果

#### 翻译服务配置

##### Google翻译
- **适用环境**：国际网络环境
- **配置要求**：无需配置
- **注意事项**：在中国大陆需要网络代理

##### 百度翻译（推荐中国大陆用户）
- **适用环境**：中国大陆网络环境
- **免费额度**：每月200万字符
- **申请地址**：https://fanyi-api.baidu.com/
- **配置步骤**：
  1. 注册百度账号并登录
  2. 创建应用获取App ID和密钥
  3. 在节点填写`baidu_app_id`和`baidu_secret_key`

##### 有道翻译（推荐中国大陆用户）
- **适用环境**：中国大陆网络环境
- **免费额度**：每日免费调用额度
- **申请地址**：https://ai.youdao.com/
- **配置步骤**：
  1. 注册有道智云账号
  2. 创建应用获取App ID和Secret
  3. 在节点填写`youdao_app_id`和`youdao_secret_key`

### LLM Translator 使用指南

#### 方式一：使用云端LLM服务

**选项A：通用LLM服务连接器**（适用于私有网关和OpenAI兼容API）
1. 添加"General LLM Service Connector"节点
2. 输入API端点URL（默认：https://api.openai.com/v1/chat/completions）
   - 私有网关：http://your-gateway-url/v1/chat/completions
   - vLLM部署：http://localhost:8000/v1/chat/completions
   - 任何OpenAI兼容服务
3. 填写API密钥（密码框保护）
4. 从下拉框选择模型或输入自定义模型名称
5. 连接到"LLM Translator"节点

使用场景：
- 私有/企业内部LLM部署（vLLM、FastChat、Text Generation WebUI）
- 企业API网关
- OpenAI兼容的代理服务
- 自定义LLM端点

**选项B：专用服务商连接器**（推荐，更清晰）
1. 根据需要添加对应的专用连接器节点：
   - **ChatGPT Service Connector** - OpenAI GPT模型（gpt-4o, gpt-4o-mini, gpt-4-turbo, o1等）
   - **DeepSeek Service Connector** - DeepSeek模型（deepseek-chat, deepseek-v3, deepseek-r1等）
   - **Kimi Service Connector** - 月之暗面Kimi模型（moonshot-v1-8k/32k/128k, kimi-v1）
   - **ZhiPu Service Connector** - 智谱GLM模型（glm-4, glm-4v, glm-3-turbo）
   - **Gemini Service Connector** - 谷歌Gemini模型（gemini-1.5-pro/flash, gemini-2.0-flash-exp）
   - **SiliconFlow Service Connector** - 通过SiliconFlow API调用多种模型
2. 从该服务商专属的下拉列表中选择模型
3. （可选）输入自定义模型ID以使用列表外的模型
4. 填写API密钥（密码框保护）
5. 连接到"LLM Translator"节点
6. 输入文本和目标语言
7. 执行翻译

专用连接器的优势：
- 只显示该服务商支持的模型，避免混淆
- 模型选择更直观方便
- 工作流组织更清晰

#### 方式二：使用本地模型

1. 添加"Load LLM Model"节点
2. 选择模型来源：
   - ComfyUI models/LLM目录
   - 自定义目录（绝对路径）
3. 连接到"LLM Translator"节点
4. 执行翻译

#### 方式三：使用Ollama

1. 添加"Ollama LLM Connector"节点
2. 配置Ollama host（默认http://localhost:11434）
3. 指定模型名称（如llama3:8b, qwen2:7b）
4. 连接到"LLM Translator"节点
5. 执行翻译

## 技术实现

### Basic Translator
- **Google翻译**：使用googletrans库，免费但需国际网络
- **百度翻译**：官方API，MD5签名认证
- **有道翻译**：官方API，SHA256签名认证
- **自动检测源语言**，完善错误处理

### LLM Translator
- **统一接口**：支持9个主流LLM服务商
- **真实API调用**：集成各服务商官方API
- **本地模型支持**：预留本地模型加载接口
- **Ollama集成**：支持Ollama本地/远程调用

## 注意事项

### 网络环境
- **中国大陆用户**：Basic Translator建议使用百度/有道翻译；LLM建议使用DeepSeek/Qwen等国内服务
- **国际用户**：可使用Google翻译和OpenAI/Claude等国际服务
- **需要稳定的网络连接**

### API配置
- API密钥通过密码框输入，UI不明文显示
- 分享工作流前请清空API密钥，避免泄露
- 请妥善保管API密钥

### 使用限制
- 各翻译服务都有调用频率和额度限制
- 免费额度用完后可能需要付费
- 建议合理使用，避免频繁调用

## 许可证

本项目遵循 MIT 许可证。

