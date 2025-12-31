import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import threading
import pyautogui
import time
import os
import sys
import keyboard
import subprocess
import ctypes 
from PIL import Image, ImageTk, ImageGrab 
import pygetwindow as gw 
from tkinterdnd2 import DND_FILES, TkinterDnD
import webbrowser # === [新增 1] 匯入網頁瀏覽器模組 ===

# ==========================================
#  [多語言字典]
# ==========================================
TRANSLATIONS = {
    "en": {
        "title": "Inazuma Chronicle Bot v0.1.3",  # <--- 修改這裡
        "tab_main": "Dashboard",
        "tab_logs": "Logs",
        "tab_stats": "Stats",
        "status_ready": "Status: Ready",
        "status_running": "Status: Running...",
        "status_paused": "Status: Paused",
        "loops_fmt": "Loops Completed: {} ",
        "time_fmt": "Last Duration: {} s",
        "btn_start": "Start Bot",
        "btn_stop": "Stop Bot",
        "btn_settings": "⚙️ Image Settings",
        "instruction": "[F9] Start/New Loop\n[F10] Pause | [ESC] Stop",
        "col_id": "#",
        "col_time": "Time",
        "col_duration": "Duration (s)",
        "col_avg": "Avg (s)",
        "setup_title": "Initial Setup Wizard",
        "setup_header": "👋 Welcome to Inazuma Bot",
        "setup_sub": "Drag screenshots to the box below.",
        "setup_list_header": "1. Select Image:",
        "setup_drop_header": "2. Drop or Paste (Ctrl+V)",
        "setup_drop_text": "Select an item above first",
        "setup_drop_active": "Drop {0} here\nor Ctrl+V",
        "btn_paste": "📋 Paste (Ctrl+V)",
        "btn_open_folder": "📂 Open Folder",
        "btn_done": "✅ Done",
        "err_no_img": "No image in clipboard!",
        "err_paste_fail": "Paste failed:\n{0}",
        "author": "v0.1.3 | Author: Kartol",      # <--- 修改這裡
        "desc_Picture1.png": "Target Level",
        "desc_Picture2.png": "Difficulty",
        "desc_Picture3.png": "Match Start",
        "desc_Picture4.png": "Yes/Confirm",
        "desc_Picture5.png": "Click (Left)",
        "desc_Picture6.png": "End Team Edit",
        "desc_Picture7.png": "NEXT",
        "desc_Picture8.png": "Kick Off"
    },
    "zh_TW": {
        "title": "閃十一編年史機器人 v0.1.3",    # <--- 修改這裡
        "tab_main": "主控制台",
        "tab_logs": "詳細日誌",
        "tab_stats": "循環紀錄",
        "status_ready": "狀態: 就緒",
        "status_running": "狀態: 執行中...",
        "status_paused": "狀態: 暫停中",
        "loops_fmt": "已完成循環: {} 次",
        "time_fmt": "上回耗時: {} 秒",
        "btn_start": "開始執行",
        "btn_stop": "停止執行",
        "btn_settings": "⚙️ 圖片設定",
        "instruction": "[F9] 啟動機器人 / 新循環\n[F10] 暫停 | [ESC] 停止",
        "col_id": "#",
        "col_time": "完成時間",
        "col_duration": "耗時 (秒)",
        "col_avg": "平均耗時 (秒)",
        "setup_title": "初次設定指引",
        "setup_header": "👋 歡迎使用閃十一編年史機器人",
        "setup_sub": "請依照右方「範例圖片」，將您的截圖拖曳至下方框框",
        "setup_list_header": "1. 點選要設定的圖片：",
        "setup_drop_header": "2. 拖曳或貼上圖片",
        "setup_drop_text": "請先從上方選擇項目",
        "setup_drop_active": "請將【{0}】的截圖拖曳至此\n或按 Ctrl+V 貼上",
        "btn_paste": "📋 貼上剪貼簿 (Ctrl+V)",
        "btn_open_folder": "📂 打開 steps 資料夾",
        "btn_done": "✅ 設定完成",
        "err_no_img": "剪貼簿內沒有圖片！\n請先截圖或複製圖片後再試一次。",
        "err_paste_fail": "貼上失敗：\n{0}",
        "author": "v0.1.3 | 作者: Kartol",        # <--- 修改這裡
        "desc_Picture1.png": "要挑戰的關卡",
        "desc_Picture2.png": "要挑戰的難度",
        "desc_Picture3.png": "比賽開始",
        "desc_Picture4.png": "是",
        "desc_Picture5.png": "按(左鍵)",
        "desc_Picture6.png": "結束編組",
        "desc_Picture7.png": "NEXT",
        "desc_Picture8.png": "開球"
    }
}

# ==========================================
#  [輔助] 資源路徑
# ==========================================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==========================================
#  [視覺元件] 圓角框架
# ==========================================
class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, radius=20, bg_color="#252526", border_color="#FFFFFF", border_width=2):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0)
        self.radius = radius
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.width = width
        self.height = height
        self.draw_background()

    def draw_background(self):
        self.delete("bg_shape") 
        offset = self.border_width / 2
        self.create_rounded_rect(
            offset, offset, self.width - offset, self.height - offset,
            self.radius, fill=self.bg_color, outline=self.border_color, width=self.border_width,
            tags="bg_shape"
        )
        self.tag_lower("bg_shape")

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def add_widget(self, widget, x, y, anchor="center"):
        return self.create_window(x, y, window=widget, anchor=anchor)

    def update_colors(self, bg_color, border_color, parent_bg):
        self.bg_color = bg_color
        self.border_color = border_color
        self.config(bg=parent_bg)
        self.itemconfig("bg_shape", fill=bg_color, outline=border_color)

# ==========================================
#  [視覺元件] 圓角按鈕
# ==========================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, radius=20, 
                 bg_color="#4CAF50", fg_color="white", hover_color="#45a049", state="normal",
                 border_color=None, border_width=0):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0, cursor="hand2")
        self.command = command
        self.text = text
        self.radius = radius
        self.base_bg = bg_color
        self.hover_bg = hover_color
        self.fg = fg_color
        self.state = state
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_width = border_width
        
        if self.state == "normal":
            self.bind("<Button-1>", self.on_click)
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)
        self.draw()

    def draw(self):
        self.delete("all")
        if self.state == "disabled":
            fill_color = "#444444" 
            self.config(cursor="arrow")
        else:
            fill_color = self.base_bg
            self.config(cursor="hand2")
        
        outline = self.border_color if self.border_color else ""
        offset = self.border_width / 2 if self.border_color else 0
        self.create_rounded_rect(offset, offset, self.width-offset, self.height-offset, self.radius, fill=fill_color, outline=outline, width=self.border_width)
        self.create_text(self.width/2, self.height/2, text=self.text, fill=self.fg, font=("微軟正黑體", 12, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        if self.state == "normal" and self.command:
            self.command()

    def on_enter(self, event):
        if self.state == "normal":
            self.delete("all")
            outline = self.border_color if self.border_color else ""
            offset = self.border_width / 2 if self.border_color else 0
            self.create_rounded_rect(offset, offset, self.width-offset, self.height-offset, self.radius, fill=self.hover_bg, outline=outline, width=self.border_width)
            self.create_text(self.width/2, self.height/2, text=self.text, fill=self.fg, font=("微軟正黑體", 12, "bold"))

    def on_leave(self, event):
        if self.state == "normal":
            self.draw()

    def set_state(self, state):
        self.state = state
        if state == "normal":
            self.bind("<Button-1>", self.on_click)
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)
        else:
            self.unbind("<Button-1>")
            self.unbind("<Enter>")
            self.unbind("<Leave>")
        self.draw()
    
    def update_colors(self, bg_color, hover_color, parent_bg, border_color=None, fg_color=None):
        self.base_bg = bg_color
        self.hover_bg = hover_color
        self.border_color = border_color
        if fg_color: self.fg = fg_color
        self.config(bg=parent_bg) 
        self.draw()

# ==========================================
#  [視覺元件] 擬真滑動開關
# ==========================================
class ModernToggle(tk.Canvas):
    def __init__(self, parent, command=None, width=90, height=40, bg_color="#F0F0F0"):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0, bd=0, cursor="hand2")
        self.command = command
        self.is_dark = False 
        self.w = width
        self.h = height
        self.bind("<Button-1>", self.toggle)
        self.draw_switch()

    def toggle(self, event=None):
        self.is_dark = not self.is_dark
        self.draw_switch()
        if self.command: self.command()

    def update_bg(self, color):
        self.config(bg=color)

    def draw_switch(self):
        self.delete("all")
        padding = 4
        d = self.h - 2 * padding
        
        if self.is_dark: 
            self.create_rounded_rect(0, 0, self.w, self.h, radius=self.h/2, fill="#2c3e50", outline="")
            stars = [(15, 12), (35, 10), (25, 25), (10, 22), (40, 28)]
            for x, y in stars: self.create_text(x, y, text="✦", fill="white", font=("Arial", 8))
            x0 = self.w - d - padding
            y0 = padding
            self.create_oval(x0, y0, x0+d, y0+d, fill="#D3D3D3", outline="#C0C0C0")
            self.create_oval(x0+8, y0+10, x0+14, y0+16, fill="#A9A9A9", outline="")
            self.create_oval(x0+18, y0+20, x0+22, y0+24, fill="#A9A9A9", outline="")
        else: 
            self.create_rounded_rect(0, 0, self.w, self.h, radius=self.h/2, fill="#87CEEB", outline="")
            self.create_oval(self.w-45, 15, self.w-25, 35, fill="#E0F7FA", outline="")
            self.create_oval(self.w-35, 8, self.w-15, 28, fill="#E0F7FA", outline="")
            x0 = padding
            y0 = padding
            self.create_oval(x0, y0, x0+d, y0+d, fill="#FFD700", outline="#FFA000", width=1) 

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

# ==========================================
#  [功能] 設定引導 (Setup Wizard)
# ==========================================
class SetupWizard(tk.Toplevel):
    def __init__(self, parent, steps_folder, examples_folder, missing_files, is_dark=False, lang_code="en"):
        super().__init__(parent)
        self.lang_code = lang_code
        self.text = TRANSLATIONS[self.lang_code]
        self.title(self.text["setup_title"])
        self.geometry("800x650")
        self.steps_folder = steps_folder       
        self.examples_folder = examples_folder 
        self.missing_files = missing_files
        self.is_dark = is_dark
        self.all_files = [
            "Picture1.png", "Picture2.png", "Picture3.png", "Picture4.png",
            "Picture5.png", "Picture6.png", "Picture7.png", "Picture8.png"
        ]
        self.selected_file = None
        self.img_cache = None 
        
        self.descriptions = {}
        for f in self.all_files:
            self.descriptions[f] = self.text.get(f"desc_{f}", f)

        if self.is_dark:
            self.bg_color = "#121212"
            self.fg_color = "#FFFFFF"
            self.list_bg = "#1E1E1E"
            self.list_fg = "#E0E0E0"
            self.drop_bg = "#252526"
            self.drop_fg = "#AAAAAA"
            self.accent_color = "#4FC3F7"
        else:
            self.bg_color = "#F0F0F0"
            self.fg_color = "#000000"
            self.list_bg = "#FFFFFF"
            self.list_fg = "#000000"
            self.drop_bg = "#F0F0F0"
            self.drop_fg = "gray"
            self.accent_color = "#007ACC"

        self.config(bg=self.bg_color)
        self.create_widgets()
        
        self.bind('<Control-v>', self.paste_from_clipboard)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.attributes('-topmost', True) 
        self.focus_force()

    def create_widgets(self):
        top_frame = tk.Frame(self, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=10)
        tk.Label(top_frame, text=self.text["setup_header"], font=("微軟正黑體", 16, "bold"), fg=self.accent_color, bg=self.bg_color).pack()
        tk.Label(top_frame, text=self.text["setup_sub"], font=("微軟正黑體", 11), fg=self.fg_color, bg=self.bg_color).pack()

        main_content = tk.Frame(self, bg=self.bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        left_panel = tk.Frame(main_content, bg=self.bg_color)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_panel, text=self.text["setup_list_header"], font=("微軟正黑體", 10, "bold"), anchor="w", bg=self.bg_color, fg=self.fg_color).pack(fill=tk.X)
        
        list_frame = tk.Frame(left_panel, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, font=("微軟正黑體", 10), height=8, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, 
                                  bg=self.list_bg, fg=self.list_fg, highlightthickness=0, bd=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.drop_frame = tk.LabelFrame(left_panel, text=self.text["setup_drop_header"], font=("微軟正黑體", 12, "bold"), 
                                        fg=self.fg_color, bg=self.bg_color, height=180)
        self.drop_frame.pack(fill=tk.X, pady=(10, 0))
        self.drop_frame.pack_propagate(False)
        
        self.drop_label = tk.Label(self.drop_frame, text=self.text["setup_drop_text"], font=("微軟正黑體", 12), 
                                   fg=self.drop_fg, bg=self.drop_bg)
        self.drop_label.pack(expand=True, fill=tk.BOTH, padx=5, pady=(5, 0))
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)

        self.btn_paste = tk.Button(self.drop_frame, text=self.text["btn_paste"], font=("微軟正黑體", 10),
                                   bg=self.list_bg, fg=self.fg_color, bd=1, command=self.paste_from_clipboard)
        self.btn_paste.pack(fill=tk.X, padx=10, pady=5)

        right_panel = tk.LabelFrame(main_content, text="範例參考 (Reference)", font=("微軟正黑體", 10, "bold"), 
                                    padx=10, pady=10, bg=self.bg_color, fg=self.fg_color)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.preview_label = tk.Label(right_panel, text="請點選左側列表\n查看範例圖片", font=("微軟正黑體", 10), 
                                      fg=self.drop_fg, bg=self.bg_color)
        self.preview_label.pack(expand=True, fill=tk.BOTH)

        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text=self.text["btn_open_folder"], bg="#FFC107", fg="black", font=("微軟正黑體", 11), 
                  command=self.open_folder, bd=0).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text=self.text["btn_done"], bg="#4CAF50", fg="white", font=("微軟正黑體", 11, "bold"), 
                  command=self.destroy, bd=0).pack(side=tk.LEFT, padx=10)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for file in self.all_files:
            path = os.path.join(self.steps_folder, file)
            exists = os.path.exists(path)
            status = "✅" if exists else "❌"
            desc = self.descriptions.get(file, "")
            self.listbox.insert(tk.END, f"{status} {file} - {desc}")
            
            if exists:
                self.listbox.itemconfig(tk.END, {'fg': '#4CAF50' if self.is_dark else 'green'})
            else:
                self.listbox.itemconfig(tk.END, {'fg': '#F44336' if self.is_dark else 'red'})

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            text = self.listbox.get(index)
            self.selected_file = text.split(' ')[1] 
            
            self.drop_frame.config(text=f"Setting: {self.selected_file}", fg=self.accent_color)
            target_bg = "#2D2D30" if self.is_dark else "#E3F2FD"
            target_fg = "#FFFFFF" if self.is_dark else "black"
            
            msg = self.text["setup_drop_active"].format(self.selected_file)
            self.drop_label.config(text=msg, fg=target_fg, bg=target_bg)
            self.btn_paste.config(state="normal", bg=self.accent_color, fg="white")
            
            example_path = os.path.join(self.examples_folder, self.selected_file)
            if os.path.exists(example_path):
                try:
                    img = Image.open(example_path)
                    img.thumbnail((300, 300))
                    self.img_cache = ImageTk.PhotoImage(img)
                    self.preview_label.config(image=self.img_cache, text="")
                except Exception:
                    self.preview_label.config(image="", text="[Image Error]")
            else:
                self.preview_label.config(image="", text="[No Example]")
        else:
            self.btn_paste.config(state="disabled")

    def on_drop(self, event):
        if not self.selected_file: return
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'): file_path = file_path[1:-1]
        try:
            img = Image.open(file_path)
            self.save_image(img)
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def paste_from_clipboard(self, event=None):
        if not self.selected_file: return
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                self.save_image(img)
            else:
                messagebox.showerror("Error", self.text["err_no_img"])
        except Exception as e:
            messagebox.showerror("Error", self.text["err_paste_fail"].format(e))

    def save_image(self, img):
        target_path = os.path.join(self.steps_folder, self.selected_file)
        img.save(target_path, "PNG")
        
        success_bg = "#1B5E20" if self.is_dark else "#C8E6C9"
        self.drop_label.config(text=f"✅ OK!", bg=success_bg)
        self.refresh_list()
        for i, f in enumerate(self.all_files):
            if f == self.selected_file:
                self.listbox.select_set(i)
                break
        self.after(1500, lambda: self.reset_drop_zone())

    def reset_drop_zone(self):
        if self.selected_file:
             target_bg = "#2D2D30" if self.is_dark else "#E3F2FD"
             target_fg = "#FFFFFF" if self.is_dark else "black"
             msg = self.text["setup_drop_active"].format(self.selected_file)
             self.drop_label.config(text=msg, bg=target_bg, fg=target_fg)
        else:
             self.drop_label.config(text=self.text["setup_drop_text"], bg=self.drop_bg, fg=self.drop_fg)

    def open_folder(self):
        if not os.path.exists(self.steps_folder): os.makedirs(self.steps_folder)
        try:
            os.startfile(self.steps_folder)
        except AttributeError:
            subprocess.call(['open', self.steps_folder])

# ==========================================
#  主程式
# ==========================================
class AutomationBotGUI:
    def __init__(self, root):
        self.root = root
        self.lang_code = "en"
        self.text = TRANSLATIONS[self.lang_code]
        
        self.root.title(self.text["title"])
        self.root.geometry("650x650") 
        
        icon_path = resource_path("app.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path) 
            except Exception as e:
                print(f"Icon Error: {e}")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.is_running = False
        self.is_paused = False
        self.bot_thread = None
        self.image_refs = [] 
        self.loop_count = 0
        self.loop_start_timestamp = 0
        self.loop_durations = []
        self.is_dark_mode = False 

        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
            self.internal_path = sys._MEIPASS              
        else:
            self.base_path = os.path.dirname(__file__)
            self.internal_path = self.base_path

        self.steps_folder = os.path.join(self.base_path, "steps")
        self.templates_folder = os.path.join(self.internal_path, "templates")
        
        if not os.path.exists(self.steps_folder): os.makedirs(self.steps_folder)
        
        self.root.after(500, self.check_missing_files) 

        try:
            keyboard.add_hotkey('F9', self.on_f9_global)
        except Exception:
            pass

        # === 頂部控制區 ===
        self.toggle_switch = ModernToggle(root, command=self.toggle_theme, width=80, height=35)
        self.toggle_switch.place(relx=0.95, rely=0.02, anchor="ne")
        
        self.btn_lang = tk.Button(root, text="🌐 EN/中", font=("Arial", 9), cursor="hand2",
                                  command=self.toggle_language, bd=1)
        self.btn_lang.place(relx=0.80, rely=0.02, anchor="ne", width=70, height=35)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=(50, 10))

        self.tab_main = tk.Frame(self.notebook)
        self.tab_logs = tk.Frame(self.notebook)
        self.tab_stats = tk.Frame(self.notebook)

        self.notebook.add(self.tab_main, text=self.text["tab_main"])
        self.notebook.add(self.tab_logs, text=self.text["tab_logs"])
        self.notebook.add(self.tab_stats, text=self.text["tab_stats"])

        # === Tab 1 ===
        self.tab_main.config(bd=0, highlightthickness=0)
        
        self.card_info = RoundedFrame(self.tab_main, width=580, height=200, radius=15)
        self.card_info.pack(pady=(20, 10))

        self.lbl_clock = tk.Label(self.tab_main, text="", font=("Consolas", 11), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_clock, 290, 30)
        self.update_clock() 

        self.lbl_status = tk.Label(self.tab_main, text=self.text["status_ready"], font=("微軟正黑體", 18, "bold"), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_status, 290, 80)
        
        self.lbl_count = tk.Label(self.tab_main, text=self.text["loops_fmt"].format(0), font=("微軟正黑體", 15, "bold"), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_count, 290, 120)
        
        self.lbl_last_time = tk.Label(self.tab_main, text=self.text["time_fmt"].format("--"), font=("微軟正黑體", 13), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_last_time, 290, 160)

        self.card_ctrl = RoundedFrame(self.tab_main, width=580, height=150, radius=15)
        self.card_ctrl.pack(pady=10)

        self.btn_start = RoundedButton(self.tab_main, text=self.text["btn_start"], width=180, height=50, radius=25, 
                                     bg_color="#4CAF50", hover_color="#45a049", command=self.start_bot)
        self.card_ctrl.add_widget(self.btn_start, 290, 40)
        
        self.btn_stop = RoundedButton(self.tab_main, text=self.text["btn_stop"], width=180, height=50, radius=25, 
                                    bg_color="#F44336", hover_color="#d32f2f", command=self.stop_bot, state="disabled")
        self.card_ctrl.add_widget(self.btn_stop, 290, 100)

        self.lbl_instruction = tk.Label(self.tab_main, text=self.text["instruction"], font=("微軟正黑體", 11), justify=tk.CENTER)
        self.lbl_instruction.pack(side=tk.BOTTOM, pady=40)
        
        self.btn_help = RoundedButton(self.tab_main, text=self.text["btn_settings"], width=100, height=30, radius=15,
                                      bg_color="#444444", hover_color="#555555", fg_color="white",
                                      command=lambda: self.check_missing_files(force_show=True))
        self.btn_help.place(relx=0.03, rely=0.97, anchor="sw")

        # === [新增 2] 設定作者標籤的游標和點擊事件 ===
        self.lbl_version = tk.Label(self.tab_main, text=self.text["author"], font=("微軟正黑體", 9), cursor="hand2")
        self.lbl_version.place(relx=0.97, rely=0.97, anchor="se")
        self.lbl_version.bind("<Button-1>", self.open_github) # 綁定點擊事件

        self.log_area = scrolledtext.ScrolledText(self.tab_logs, width=70, height=25, font=("Consolas", 10), bd=0, highlightthickness=0)
        self.log_area.pack(expand=True, fill='both', padx=2, pady=2) 
        self.log_area.config(state='disabled') 

        columns = ("id", "time", "duration", "avg")
        self.tree = ttk.Treeview(self.tab_stats, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text=self.text["col_id"]); self.tree.column("id", width=50, anchor="center")
        self.tree.heading("time", text=self.text["col_time"]); self.tree.column("time", width=150, anchor="center")
        self.tree.heading("duration", text=self.text["col_duration"]); self.tree.column("duration", width=100, anchor="center")
        self.tree.heading("avg", text=self.text["col_avg"]); self.tree.column("avg", width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.tab_stats, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.apply_theme()

    def update_clock(self):
        now = time.strftime("%Y/%m/%d\n%H:%M:%S")
        self.lbl_clock.config(text=now)
        self.root.after(1000, self.update_clock)

    def on_f9_global(self):
        if not self.is_running:
            self.root.after(0, self.start_bot)

    def check_missing_files(self, force_show=False):
        required_files = [
            "Picture1.png", "Picture2.png", "Picture3.png", "Picture4.png",
            "Picture5.png", "Picture6.png", "Picture7.png", "Picture8.png"
        ]
        missing = [f for f in required_files if not os.path.exists(os.path.join(self.steps_folder, f))]
        
        if missing or force_show:
            SetupWizard(self.root, self.steps_folder, self.templates_folder, missing, is_dark=self.is_dark_mode, lang_code=self.lang_code)

    def toggle_language(self):
        self.lang_code = "zh_TW" if self.lang_code == "en" else "en"
        self.text = TRANSLATIONS[self.lang_code]
        self.update_ui_text()

    def update_ui_text(self):
        self.root.title(self.text["title"])
        self.notebook.tab(0, text=self.text["tab_main"])
        self.notebook.tab(1, text=self.text["tab_logs"])
        self.notebook.tab(2, text=self.text["tab_stats"])
        
        self.lbl_status.config(text=self.text["status_ready"] if not self.is_running else self.text["status_running"])
        self.update_loop_info(None if self.loop_count == 0 else self.loop_durations[-1] if self.loop_durations else None)
        self.lbl_instruction.config(text=self.text["instruction"])
        self.lbl_version.config(text=self.text["author"])
        
        self.btn_start.itemconfig(self.btn_start.find_withtag("text"), text=self.text["btn_start"])
        self.btn_stop.itemconfig(self.btn_stop.find_withtag("text"), text=self.text["btn_stop"])
        self.btn_help.itemconfig(self.btn_help.find_withtag("text"), text=self.text["btn_settings"])
        
        self.tree.heading("id", text=self.text["col_id"])
        self.tree.heading("time", text=self.text["col_time"])
        self.tree.heading("duration", text=self.text["col_duration"])
        self.tree.heading("avg", text=self.text["col_avg"])

    def toggle_theme(self):
        self.is_dark_mode = self.toggle_switch.is_dark 
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            bg_color, fg_color = "#000000", "#FFFFFF"      
            card_bg = "#1A1A1A"
            card_border = "#FFFFFF" 
            text_bg, text_fg = "#111111", "#E0E0E0"       
            count_fg, time_fg, instr_fg = "#4FC3F7", "#FFB74D", "#81D4FA"
            clock_fg = "#AAAAAA"
            # [新增 4] 深色模式下的連結顏色 (淺藍色)
            link_fg = "#4FC3F7" 
            tab_bg, tab_fg = "#1A1A1A", "#808080"
            tab_sel_bg, tab_sel_fg = "#000000", "#4FC3F7"
            tree_bg, tree_fg = "#111111", "#E0E0E0"
            head_bg, head_fg = "#1A1A1A", "#FFFFFF"
            btn_start_bg, btn_start_hover = "#388E3C", "#2E7D32"
            btn_stop_bg, btn_stop_hover = "#D32F2F", "#C62828"
            btn_help_bg, btn_help_hover, btn_help_fg = "#444444", "#555555", "#FFFFFF"
            btn_help_border = "#FFFFFF"
            btn_lang_bg, btn_lang_fg = "#333333", "#FFFFFF"
        else:
            bg_color, fg_color = "#F0F0F0", "#000000"
            card_bg = "#FFFFFF"
            card_border = "#CCCCCC" 
            text_bg, text_fg = "#FFFFFF", "#000000"
            count_fg, time_fg, instr_fg = "#007ACC", "#E65100", "blue"
            clock_fg = "#555555"
            # [新增 4] 淺色模式下的連結顏色 (標準藍色)
            link_fg = "#0000EE"
            tab_bg, tab_fg = "#E0E0E0", "#000000"
            tab_sel_bg, tab_sel_fg = "#F0F0F0", "#007ACC"
            tree_bg, tree_fg = "#FFFFFF", "#000000"
            head_bg, head_fg = "#E0E0E0", "#000000"
            btn_start_bg, btn_start_hover = "#4CAF50", "#45a049"
            btn_stop_bg, btn_stop_hover = "#F44336", "#d32f2f"
            btn_help_bg, btn_help_hover, btn_help_fg = "#E0E0E0", "#D0D0D0", "#000000"
            btn_help_border = "#AAAAAA"
            btn_lang_bg, btn_lang_fg = "#E0E0E0", "#000000"

        self.toggle_switch.update_bg(bg_color)
        self.btn_start.update_colors(btn_start_bg, btn_start_hover, card_bg)
        self.btn_stop.update_colors(btn_stop_bg, btn_stop_hover, card_bg)
        self.btn_help.update_colors(btn_help_bg, btn_help_hover, bg_color, border_color=btn_help_border, fg_color=btn_help_fg)

        self.style.configure("TNotebook", background=bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=tab_bg, foreground=tab_fg, padding=[12, 8], font=("微軟正黑體", 10), borderwidth=0)
        self.style.map("TNotebook.Tab", background=[("selected", tab_sel_bg)], foreground=[("selected", tab_sel_fg)])

        self.style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg, font=("Consolas", 10), rowheight=25, borderwidth=0)
        self.style.configure("Treeview.Heading", background=head_bg, foreground=head_fg, font=("微軟正黑體", 10, "bold"), borderwidth=0)
        self.style.map("Treeview", background=[('selected', count_fg)], foreground=[('selected', 'white')])

        self.root.config(bg=bg_color)
        self.tab_main.config(bg=bg_color)
        self.tab_logs.config(bg=bg_color)
        self.tab_stats.config(bg=bg_color)
        
        self.card_info.update_colors(card_bg, card_border, bg_color)
        self.card_ctrl.update_colors(card_bg, card_border, bg_color)

        for widget in [self.lbl_clock, self.lbl_status, self.lbl_count, self.lbl_last_time]:
            widget.config(bg=card_bg)

        self.lbl_status.config(fg=fg_color if self.is_dark_mode else "#333333")
        self.lbl_count.config(fg=count_fg)
        self.lbl_last_time.config(fg=time_fg)
        self.lbl_clock.config(fg=clock_fg)
        # [新增 4] 套用連結顏色和底線字型
        self.lbl_version.config(bg=bg_color, fg=link_fg, font=("微軟正黑體", 9, "underline"))
        self.lbl_instruction.config(bg=bg_color, fg=instr_fg)
        self.log_area.config(bg=text_bg, fg=text_fg, insertbackground=fg_color)
        self.btn_help.config(bg=btn_help_bg)
        self.btn_lang.config(bg=btn_lang_bg, fg=btn_lang_fg, activebackground=btn_help_hover)

    # === [新增 3] 開啟 GitHub 網頁的函式 ===
    def open_github(self, event):
        webbrowser.open("https://github.com/xReiNio")

    def switch_to_game(self):
        target_name = "INAZUMA ELEVEN"
        self.log_msg(f"Searching window: {target_name}...")
        try:
            windows = gw.getWindowsWithTitle(target_name)
            if windows:
                win = windows[0]
                if win.isMinimized: win.restore()
                win.activate()
                self.log_msg("Window locked.")
                return True
            else:
                self.log_msg(f"Warning: '{target_name}' not found.")
                return False
        except Exception as e:
            self.log_msg(f"Switch failed: {e}")
            return False

    def log_msg(self, message):
        self.log_area.config(state='normal') 
        current_time = time.strftime("[%H:%M:%S] ", time.localtime())
        self.log_area.insert(tk.END, current_time + message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled') 

    def log_image_msg(self, text, image_path):
        self.log_area.config(state='normal')
        current_time = time.strftime("[%H:%M:%S] ", time.localtime())
        self.log_area.insert(tk.END, current_time + text)
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                base_height = 20
                h_percent = (base_height / float(img.size[1]))
                w_size = int((float(img.size[0]) * float(h_percent)))
                img_resized = img.resize((w_size, base_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_resized)
                self.image_refs.append(photo) 
                self.log_area.image_create(tk.END, image=photo)
                self.log_area.insert(tk.END, f" ({os.path.basename(image_path)})")
            else:
                self.log_area.insert(tk.END, f" [File Missing]")
        except Exception as e:
            self.log_area.insert(tk.END, f"[Error]")
            print(e)
        self.log_area.insert(tk.END, "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def update_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    def update_loop_info(self, last_duration=None):
        self.lbl_count.config(text=self.text["loops_fmt"].format(self.loop_count))
        if last_duration is not None:
            self.lbl_last_time.config(text=self.text["time_fmt"].format(f"{last_duration:.1f}"))
            self.update_stats_table(last_duration)
        else:
            self.lbl_last_time.config(text=self.text["time_fmt"].format("--"))

    def update_stats_table(self, duration):
        self.loop_durations.append(duration)
        avg_duration = sum(self.loop_durations) / len(self.loop_durations)
        current_time_str = time.strftime("%H:%M:%S")
        self.tree.insert("", 0, values=(self.loop_count, current_time_str, f"{duration:.2f}", f"{avg_duration:.2f}"))

    def start_bot(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.loop_count = 0
            self.loop_durations = []
            
            for item in self.tree.get_children(): self.tree.delete(item)
            self.update_loop_info()
            self.image_refs.clear()
            self.log_area.config(state='normal')
            self.log_area.delete(1.0, tk.END)
            self.log_area.config(state='disabled')

            self.btn_start.set_state("disabled")
            self.btn_stop.set_state("normal")
            self.update_status(self.text["status_running"], "green")
            self.log_msg("=== Bot Started ===")

            self.notebook.select(self.tab_logs)
            self.switch_to_game()

            self.bot_thread = threading.Thread(target=self.run_bot_logic)
            self.bot_thread.daemon = True 
            self.bot_thread.start()

    def stop_bot(self):
        self.is_running = False
        self.btn_start.set_state("normal")
        self.btn_stop.set_state("disabled")
        self.update_status(self.text["status_ready"], "red")
        self.log_msg("=== Bot Stopped ===")

    def run_bot_logic(self):
        steps = [
            {"type": "click", "target": "Picture1.png", "timeout": 10,  "on_fail": 12},
            {"type": "click", "target": "Picture2.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture3.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture4.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture5.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture6.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture7.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture7.png", "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture8.png", "timeout": 10,  "on_fail": -1},
            {"type": "key",   "target": "u",            "timeout": 30,  "on_fail": -1},
            {"type": "click", "target": "Picture6.png", "timeout": 300, "on_fail": 8},
            {
                "type": "click", "target": "Picture7.png", "timeout": 300, "on_fail": -1, 
                "wait_after_move": 2, "repeat": 5, "repeat_interval": 2   
            }
        ]
        
        while self.is_running:
            self.log_msg("\n=== New Loop Start ===")
            self.switch_to_game()
            self.loop_start_timestamp = time.time()
            step_index = 0
            step_start_time = time.time()
            if self.smart_sleep(0): continue 
            while step_index < len(steps):
                if not self.is_running: break 
                if self.smart_sleep(0): break 
                step = steps[step_index]
                action_type = step["type"]
                target = step.get("target", "") 
                timeout = step.get("timeout", 10)
                on_fail = step.get("on_fail", -1)
                wait_after_move = step.get("wait_after_move", 1)
                repeat = step.get("repeat", 1)
                repeat_interval = step.get("repeat_interval", 0.1)
                
                if time.time() - step_start_time > timeout and timeout > 0:
                    old_index = step_index
                    if on_fail == -1:
                        step_index = max(step_index - 1, 0)
                        self.log_msg(f"Step {old_index+1} Timeout -> Go back to {step_index+1}")
                    else:
                        step_index = on_fail
                        self.log_msg(f"Step {old_index+1} Timeout -> Jump to {on_fail+1}")
                    step_start_time = time.time()
                    continue

                try:
                    if action_type == "click":
                        img_path = os.path.join(self.steps_folder, target)
                        if not os.path.exists(img_path):
                            self.log_msg(f"Error: Missing {target}")
                            time.sleep(1)
                            continue
                        location = pyautogui.locateOnScreen(img_path, confidence=0.85)
                        if location:
                            center_x, center_y = pyautogui.center(location)
                            pyautogui.moveTo(center_x, center_y, duration=1.0)
                            if self.smart_sleep(wait_after_move): break
                            restart_triggered = False
                            for i in range(repeat):
                                if not self.is_running: break
                                pyautogui.click()
                                log_text = f"Clicked ({i+1}/{repeat}): "
                                self.log_image_msg(log_text, img_path)
                                if i < repeat - 1:
                                    if self.smart_sleep(repeat_interval): 
                                        restart_triggered = True
                                        break
                            if restart_triggered: break
                            step_index += 1
                            step_start_time = time.time()
                    elif action_type == "click_now":
                        restart_triggered = False
                        for i in range(repeat):
                            if not self.is_running: break
                            pyautogui.click()
                            self.log_msg(f"Blind Click ({i+1}/{repeat})")
                            if i < repeat - 1:
                                if self.smart_sleep(repeat_interval):
                                    restart_triggered = True
                                    break
                        if restart_triggered: break
                        step_index += 1
                        step_start_time = time.time()
                    elif action_type == "key":
                        self.log_msg(f"Step {step_index+1}: Press {target.upper()}")
                        pyautogui.keyDown(target)
                        time.sleep(0.15) 
                        pyautogui.keyUp(target)
                        step_index += 1
                        step_start_time = time.time()
                    elif action_type == "wait":
                        sec = step.get("seconds", 1)
                        self.log_msg(f"Step {step_index+1}: Wait {sec}s")
                        if self.smart_sleep(sec): break 
                        step_index += 1
                        step_start_time = time.time()
                except pyautogui.ImageNotFoundException:
                    pass
                except Exception as e:
                    self.log_msg(f"Error: {e}")
                if self.smart_sleep(0.5): break
            
            end_time = time.time()
            duration = end_time - self.loop_start_timestamp
            self.loop_count += 1
            self.update_loop_info(duration)
            self.log_msg(f"=== Loop Done | Duration: {duration:.2f}s ===")
            time.sleep(1)
        self.stop_bot()

    def smart_sleep(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration or duration == 0:
            if not self.is_running: return True 
            if keyboard.is_pressed('F9'):
                self.log_msg("Hotkey: F9 (New Loop)")
                while keyboard.is_pressed('F9'): time.sleep(0.1)
                return True 
            if keyboard.is_pressed('F10'):
                self.is_paused = not self.is_paused
                status_text = self.text["status_paused"] if self.is_paused else self.text["status_running"]
                color = "orange" if self.is_paused else "green"
                self.update_status(status_text, color)
                self.log_msg(f"Hotkey: F10 ({status_text})")
                while keyboard.is_pressed('F10'): time.sleep(0.1)
                while self.is_paused and self.is_running:
                    if keyboard.is_pressed('F10'):
                        self.is_paused = False
                        self.update_status(self.text["status_running"], "green")
                        self.log_msg("Resumed!")
                        while keyboard.is_pressed('F10'): time.sleep(0.1)
                    time.sleep(0.1)
            if keyboard.is_pressed('esc'):
                self.log_msg("Hotkey: ESC (Stop)")
                self.is_running = False
                return True
            if duration == 0: break
            time.sleep(0.1)
        return False

# ==========================================
#  [修正] Taskbar ID 設置
# ==========================================
if __name__ == "__main__":
    myappid = 'kartol.inazuma.bot.v1' 
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    root = TkinterDnD.Tk()
    app = AutomationBotGUI(root)
    root.mainloop()
