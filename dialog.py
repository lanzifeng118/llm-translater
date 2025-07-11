import tkinter as tk
import pyperclip

# 确保在主线程执行UI操作
def create_dialog(original, suggestion):
    # # macOS 需要特殊处理主窗口
    # if platform.system() == "Darwin" and not self.root:
    #     self.root = tk.Tk()
    #     self.root.withdraw()

    dialog = tk.Toplevel()
    dialog.title("英语助手建议")
    dialog.geometry("600x400")
    dialog.resizable(True, True)

    # 原文框
    tk.Label(dialog, text="原文:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    original_frame = tk.Frame(dialog, borderwidth=1, bg="#ffffff")
    original_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(original_frame, text=original, wraplength=550, bg="#ffffff").pack(anchor="w", padx=10, pady=5)

    # 建议框
    tk.Label(dialog, text="建议:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    suggestion_frame = tk.Frame(dialog, borderwidth=0)
    suggestion_frame.pack(fill="both", expand=True, padx=0, pady=5)
    suggestion_text = tk.Text(suggestion_frame, wrap="word", height=10, bg="#ffffff")
    suggestion_text.insert("1.0", suggestion)
    suggestion_text.config(state="disabled")
    suggestion_text.pack(fill="both", expand=False, padx=5, pady=5)

    # 按钮区域
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(fill="x", padx=10, pady=10)

    def copy_suggestion():
        pyperclip.copy(suggestion)
        # dialog.destroy()

    def ignore_suggestion():
        dialog.destroy()

    tk.Button(btn_frame, text="复制建议", command=copy_suggestion, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="忽略", command=ignore_suggestion, width=10).pack(side="left", padx=5)

    # 确保窗口出现在最前面
    dialog.attributes('-topmost', True)
    dialog.update()
    dialog.attributes('-topmost', False)