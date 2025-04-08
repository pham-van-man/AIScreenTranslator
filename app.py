import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageGrab
import requests
import os
import keyboard
import threading
import pystray
from pystray import MenuItem as item
import sys
import base64
import subprocess
import time
import psutil
from dotenv import load_dotenv
import winreg

result_window = None
icon = None
is_processing = False
exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
load_dotenv()
api_key = os.getenv("gemini_api_key")

def add_to_startup_registry(app_name, exe_path):
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)

def capture_and_process():
    try:
        image = ImageGrab.grabclipboard()
        if image is None:
            messagebox.showerror("Lỗi", "Không tìm thấy hình ảnh trong clipboard.")
            return
        image_path = os.path.join(exe_dir, "screenshot_clipboard.png")
        image.save(image_path)
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")
        if not image_data:
            messagebox.showinfo("Kết quả", "Không nhận diện được hình ảnh.")
        else:
            response = call_gemini_api(image_data)
            if response:
                display_result(response)
        if os.path.exists(image_path):
            os.remove(image_path)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xử lý ảnh: {str(e)}")

def call_gemini_api(image_data):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    rules_path = os.path.join(exe_dir, "rules.txt")
    if not os.path.exists(rules_path):
        messagebox.showerror("Lỗi", "Không tìm thấy file rules.txt trong thư mục ứng dụng.")
        return None
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = f.read()
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": image_data
                        }
                    },
                    {"text": f"{rules}"}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            try:
                error_detail = response.json()
                error_message = error_detail.get("error", {}).get("message", response.text)
            except Exception:
                error_message = response.text
            messagebox.showerror("Lỗi API", f"API trả về lỗi {response.status_code}:\n{error_message}")
            return None
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi gọi API: {str(e)}")
        return None

def display_result(text):
    global result_window
    if result_window is not None and result_window.winfo_exists():
        result_window.destroy()
        result_window = None
    result_window = tk.Toplevel(root)
    result_window.title("Kết quả")
    result_window.geometry("800x600")
    result_window.attributes('-topmost', True)
    result_window.resizable(True, True)
    result_window.minsize(400, 300)
    frame = tk.Frame(result_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Arial", 14), padx=10, pady=10)
    text_area.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, text)
    text_area.config(state='disabled')
    result_window.protocol("WM_DELETE_WINDOW", on_result_close)

def on_result_close():
    global result_window
    if result_window:
        result_window.destroy()
        result_window = None

def wait_until_process_exits(name, timeout=None):
    while True:
        if all(proc.info['name'] != name for proc in psutil.process_iter(['name'])):
            return True
        time.sleep(0.5)
        if timeout is not None:
            timeout -= 0.5
            if timeout <= 0:
                return False

def wait_until_process_exists(name, timeout=10):
    for _ in range(int(timeout * 2)):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                return True
        time.sleep(0.5)
    return False

def wait_for_screenclip():
    global is_processing
    if is_processing:
        print("Đang xử lý, vui lòng chờ...")
        return
    is_processing = True
    try:
        subprocess.Popen("explorer.exe ms-screenclip:", shell=True)
        if not wait_until_process_exists("ScreenClippingHost.exe", timeout=10):
            messagebox.showerror("Lỗi", "Không khởi động được công cụ cắt màn hình.")
            return
        if not wait_until_process_exits("ScreenClippingHost.exe"):
            messagebox.showerror("Lỗi", "Công cụ cắt chưa được đóng.")
            return
        time.sleep(1)
        capture_and_process()
    finally:
        is_processing = False

def quit_app():
    global icon, root
    if icon:
        icon.stop()
    root.quit()
    os._exit(0)

def setup_tray_icon():
    global icon
    try:
        icon_path = os.path.join(exe_dir, "icon.png")
        if not os.path.exists(icon_path):
            raise FileNotFoundError
        image = Image.open(icon_path)
        image = image.resize((32, 32), Image.Resampling.LANCZOS)
    except Exception:
        image = Image.new('RGB', (32, 32), color=(0, 255, 0))
    menu = (item('Thoát', quit_app),)
    icon = pystray.Icon("ScreenCapture", image, "Screen Capture", menu)
    threading.Thread(target=icon.run, daemon=True).start()

def run_app():
    global root
    root = tk.Tk()
    root.withdraw()
    setup_tray_icon()
    keyboard.on_press_key("x", lambda _: threading.Thread(target=wait_for_screenclip).start() if keyboard.is_pressed("ctrl+alt") else None)
    root.mainloop()

if __name__ == "__main__":
    app_name = "ScreenCapture"
    exe_path = os.path.abspath(sys.argv[0])
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )
        try:
            existing_path, _ = winreg.QueryValueEx(key, app_name)
            if existing_path != exe_path:
                add_to_startup_registry(app_name, exe_path)
        except FileNotFoundError:
            add_to_startup_registry(app_name, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Không thể thêm vào khởi động cùng Windows: {e}")
    run_app()
