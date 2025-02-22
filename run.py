from openai import OpenAI, APIError, AuthenticationError, APIConnectionError
import readline
import os
import logging

logging.basicConfig(filename='deepseek_chat.log', level=logging.ERROR)

# API密钥
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxx"
if not DEEPSEEK_API_KEY:
    raise ValueError("未找到变量 DEEPSEEK_API_KEY，请先申请并设置API密钥")

class DeepSeekChat:
    def __init__(self, system_prompt="你需要扮演可莉，模仿她的语气进行线上的日常对话。【遇到复杂问题时能迅速切换至'轰轰火花模式'，用专业术语给出清晰解答后再恢复可爱语气】禁止使用括号描述动作和心理。只输出语言，除非用户问你的动作。"):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"  # 或兼容性路径 https://api.deepseek.com/v1
        )
        self.system_prompt = system_prompt
        self.reset_session()
    
    def reset_session(self, system_prompt=None):
        """重置会话，可更新系统提示"""
        if system_prompt is not None:
            self.system_prompt = system_prompt
        self.messages = []
        if self.system_prompt:
            self.messages.append({
                "role": "system", 
                "content": self.system_prompt
            })
    # 温度设置，是否流式处理
    def chat(self, prompt, model="deepseek-chat", temperature=1.5, timeout=12, stream=True):
        """发送消息并获取回复"""
        if not prompt.strip():
            return "错误：输入内容不能为空"
        
        # 临时消息副本（用于错误回滚）
        temp_messages = self.messages.copy()
        temp_messages.append({"role": "user", "content": prompt})
        
        try:
            # 参数验证
            if not 0 <= temperature <= 2:
                return "错误：temperature 参数需在0到2之间"
            
            # API调用
            response = self.client.chat.completions.create(
                model=model,
                messages=temp_messages,
                temperature=temperature,
                stream=stream,
                timeout=timeout
            )
            
            # 处理响应
            if stream:
                # 流式处理逻辑示例（需迭代返回内容）
                return self._handle_stream_response(response, temp_messages)
            else:
                return self._handle_normal_response(response, temp_messages)
        
        except AuthenticationError:
            return "[DeepSeek] 认证失败：请检查API密钥是否正确"
        except APIConnectionError:
            return "[DeepSeek] 连接错误：请检查网络连接"
        except APIError as e:
            return f"[DeepSeek] API错误：{e.message}"
        except Exception as e:
            logging.error(f"未知错误：{str(e)}")
            return f"错误：{str(e)}"
    
    def _handle_normal_response(self, response, temp_messages):
        """处理非流式响应"""
        if not response.choices:
            return "错误：未收到有效响应"
        
        message = response.choices[0].message
        if not message.content:
            return "错误：响应内容为空"
        
        # 更新正式消息历史
        self.messages = temp_messages
        self.messages.append({
            "role": "assistant",
            "content": message.content
        })
        return message.content
    
    def _handle_stream_response(self, response, temp_messages):
        """处理流式响应（示例骨架）"""
        collected_content = []
        try:
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    # print(content, end="", flush=True)
                    print(f"可莉：{content}", end="", flush=True) 
                    collected_content.append(content)
            print()
            
            # 更新消息历史
            full_content = "".join(collected_content)
            self.messages = temp_messages
            self.messages.append({
                "role": "assistant",
                "content": full_content
            })
            # return full_content
            return None
        except Exception as e:
            return f"流式传输中断：{str(e)}"

def main():
    print("DeepSeek Chat 命令行交互（当前扮演的是【可莉】；输入 /help 获取命令帮助）")
    ds_chat = DeepSeekChat()  # 初始无系统消息
    
    help_text = """
命令列表：
/help   - 显示本帮助
/reset  - 重置当前会话（保留系统提示）
/new    - 创建新会话（可修改系统提示）
/exit   - 退出程序
"""
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            if not user_input:
                print("提示：输入内容不能为空")
                continue
            
            # 命令处理
            if user_input.startswith("/"):
                if user_input == "/exit":
                    print("会话结束")
                    break
                elif user_input == "/help":
                    print(help_text)
                elif user_input == "/reset":
                    ds_chat.reset_session()
                    print("会话已重置，当前系统提示：", 
                          ds_chat.system_prompt or "无")
                elif user_input == "/new":
                    new_prompt = input("输入新系统提示（留空则不使用）: ").strip()
                    ds_chat.reset_session(new_prompt if new_prompt else None)
                    print(f"新会话已创建，系统提示: {new_prompt or '无'}")
                else:
                    print("未知命令，输入 /help 查看可用命令")
                continue
            
            # 发送消息
            response = ds_chat.chat(user_input)
            if response is not None:
                print("\n可莉:", response)
        
        except KeyboardInterrupt:
            confirm = input("\n确定要退出吗？(y/n) ").lower()
            if confirm == 'y':
                break
        except Exception as e:
            print(f"运行时错误：{str(e)}")

if __name__ == "__main__":
    main()