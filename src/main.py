import pyperclip
import time
import tkinter as tk
import threading
import platform
from src.util import create_dialog, chat, is_in_wechat

class EnglishAssistant:
    def __init__(self):
        self.last_clipboard = ""
        self.running = True
        self.root = None  # Tkinter 根窗口
        self.app_situation = 0 # 0 不在微信 1 回到微信 2 已在微信

    def get_ai_suggestion(self, text):
        """使用 OpenAI API 获取语法检查或翻译建议"""
        try:
            system_prompt = """要求：输出为日常聊天用语, 请根据以下规则处理我的输入：
            1. 如果输入是 **纯中文** → 翻译成自然流畅的英文, 
            2. 如果输入是 **纯英文** → 做三件事，检查语法/拼写错误并优化表达、翻译成中文、如何回复这句话,
            3. 如果输入是 **中英混合** → 将所有内容统一翻译成英文,
            4. 保持口语化，无需解释过程，直接输出结果"""

            response = chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ API调用出错: {str(e)}"

    def show_suggestion(self, original, suggestion):
        """显示建议的弹窗 - 确保在主线程执行"""

        def show():
            create_dialog(original, suggestion)

        # 在主线程执行UI操作
        if self.root:
            self.root.after(0, show)
        else:
            show()

    def clipboard_monitor(self):
        """剪贴板监听主循环"""
        print("英语助手已启动! ")
        print("在微信输入文本后，按 Ctrl+C 复制即可触发检查")

        try:
            while self.running:
                current_clipboard = pyperclip.paste()

                if is_in_wechat():
                    if self.app_situation == 0:
                        self.app_situation = 1
                        self.last_clipboard = current_clipboard
                    elif self.app_situation == 1:
                        self.app_situation = 2
                else:
                    self.app_situation = 0


                # 忽略空内容和未变化的内容
                if self.app_situation == 2 and current_clipboard and current_clipboard.strip() and current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard

                    print(f"\n检测到新文本: {current_clipboard}")

                    # 在新线程中处理API请求
                    def process_request():
                        suggestion = self.get_ai_suggestion(current_clipboard)
                        print("AI建议:", suggestion)
                        self.show_suggestion(current_clipboard, suggestion)

                    threading.Thread(target=process_request, daemon=True).start()


                time.sleep(0.5)  # 降低CPU使用率

        except KeyboardInterrupt:
            print("\n助手已退出")
            self.running = False

    def start(self):
        """启动助手"""
        # 在macOS上需要创建隐藏的主窗口
        if platform.system() == "Darwin":
            self.root = tk.Tk()
            self.root.withdraw()

        # 启动剪贴板监听线程
        monitor_thread = threading.Thread(target=self.clipboard_monitor, daemon=True)
        monitor_thread.start()

        # macOS需要运行Tk事件循环
        if platform.system() == "Darwin" and self.root:
            self.root.mainloop()
        else:
            monitor_thread.join()


if __name__ == "__main__":
    assistant = EnglishAssistant()
    assistant.start()