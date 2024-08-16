import tkinter as tk
from datetime import datetime, time
import ctypes
import win32api
import os
import sys
import time as t
import winreg as reg
import threading
import keyboard  # 安装 keyboard 模块

# 添加程序到开机启动项
def add_to_startup():
    if getattr(sys, 'frozen', False):
        script_path = os.path.abspath(sys.executable)
    else:
        script_path = os.path.abspath(__file__)

    key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    key_value = 'MyAutoStartupScript'

    registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
    reg.SetValueEx(registry_key, key_value, 0, reg.REG_SZ, script_path)
    reg.CloseKey(registry_key)

# 定义关闭覆盖窗口的函数
def close_overlay(event=None):
    global overlay_running
    overlay_running = False
    if overlay and overlay.winfo_exists():
        overlay.destroy()

# 定义显示覆盖窗口的函数
def show_overlay():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    
    global overlay
    overlay = tk.Tk()
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-alpha', 0.2)
    overlay.config(bg='grey')

    global label
    label = tk.Label(overlay, text="", font=("simsun", 50), fg="red", bg="black", justify="center")
    label.pack(expand=True)

    overlay.bind("<Escape>", close_overlay)
    overlay.bind("<Button-3>", close_overlay)

    # 更新文本内容的线程
    def update_time():
        while overlay_running:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = f"{now}\n预约时间段：\n早上 8:50 - 中午 12:00\n下午12:00 - 下午16:50\n当前时间无法取号，请耐心等待！\n请使用身份证取号，谢谢配合！"
            label.config(text=text)
            t.sleep(1)

    overlay_running = True
    time_thread = threading.Thread(target=update_time, daemon=True)
    time_thread.start()

    overlay.mainloop()

# 定义自动关机函数
def shutdown_computer():
    os.system("shutdown /s /f /t 1")  # 强制立即关机

# 定义无限循环进行时间检查
def check_time():
    start_time = time(8, 50)  # 早上8点
    end_time = time(16, 50)   # 下午4点
    shutdown_time = time(17, 20)  # 关机时间5点

    while True:
        now = datetime.now().time()

        # 检查是否在非工作时间范围内，显示覆盖窗口
        if now < start_time or now > end_time:
            show_overlay()

        # 检查是否达到关机时间
        if now >= shutdown_time:
            shutdown_computer()
            break  # 关机后停止检查

        # 检测 Windows 键或 ESC 键退出程序
        if keyboard.is_pressed('win') or keyboard.is_pressed('esc'):
            close_overlay()
            break  # 退出覆盖窗口

        # 每分钟检查一次
        t.sleep(60)

# 启动时添加到开机启动项
add_to_startup()

# 开始时间检查
check_time()


##pyinstaller --onefile --noconsole your_script.py

