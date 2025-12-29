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
from PIL import Image, ImageTk 
import pygetwindow as gw 
from tkinterdnd2 import DND_FILES, TkinterDnD

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
#  [視覺元件] 圓角框架 (已修復消失問題)
# ==========================================
class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, radius=20, bg_color="#252526", border_color="#FFFFFF", border_width=2):
        # 設定 Canvas 背景色與父層一致，避免圓角外出現白邊
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0)
        self.radius = radius
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.width = width
        self.height = height
        
        # 初始化繪製背景
        self.draw_background()

    def draw_background(self):
        # 這裡不使用 delete("all")，而是只繪製背景並給予標籤 "bg_shape"
        self.delete("bg_shape") 
        offset = self.border_width / 2
        self.create_rounded_rect(
            offset, offset, self.width - offset, self.height - offset,
            self.radius, fill=self.bg_color, outline=self.border_color, width=self.border_width,
            tags="bg_shape" # 加上標籤
        )
        # 確保背景在最底層
        self.tag_lower("bg_shape")

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def add_widget(self, widget, x, y, anchor="center"):
        return self.create_window(x, y, window=widget, anchor=anchor)

    def update_colors(self, bg_color, border_color, parent_bg):
        self.bg_color = bg_color
        self.border_color = border_color
        self.config(bg=parent_bg) # 更新 Canvas 本身的背景色以融入父層
        
        # 只更新背景圖形的顏色，不刪除其他元件
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
    def __init__(self, parent, steps_folder, examples_folder, missing_files, is_dark=False):
        super().__init__(parent)
        self.title("初次設定指引")
        self.geometry("800x600") 
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
        
        self.descriptions = {
            "Picture1.png": "要挑戰的關卡",
            "Picture2.png": "要挑戰的難度",
            "Picture3.png": "比賽開始",
            "Picture4.png": "是",
            "Picture5.png": "按(左鍵)",
            "Picture6.png": "結束編組",
            "Picture7.png": "NEXT",
            "Picture8.png": "開球",
        }

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
        tk.Label(top_frame, text="👋 歡迎使用閃十一編年史機器人", font=("微軟正黑體", 16, "bold"), fg=self.accent_color, bg=self.bg_color).pack()
        tk.Label(top_frame, text="請依照右方「範例圖片」，將您的截圖拖曳至下方框框", font=("微軟正黑體", 11), fg=self.fg_color, bg=self.bg_color).pack()

        main_content = tk.Frame(self, bg=self.bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        left_panel = tk.Frame(main_content, bg=self.bg_color)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_panel, text="1. 點選要設定的圖片：", font=("微軟正黑體", 10, "bold"), anchor="w", bg=self.bg_color, fg=self.fg_color).pack(fill=tk.X)
        
        list_frame = tk.Frame(left_panel, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, font=("微軟正黑體", 10), height=8, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, 
                                  bg=self.list_bg, fg=self.list_fg, highlightthickness=0, bd=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.drop_frame = tk.LabelFrame(left_panel, text="2. 拖曳圖片到這裡", font=("微軟正黑體", 12, "bold"), 
                                        fg=self.fg_color, bg=self.bg_color, height=150)
        self.drop_frame.pack(fill=tk.X, pady=(10, 0))
        self.drop_frame.pack_propagate(False)
        
        self.drop_label = tk.Label(self.drop_frame, text="請先從上方選擇項目", font=("微軟正黑體", 12), 
                                   fg=self.drop_fg, bg=self.drop_bg)
        self.drop_label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)

        right_panel = tk.LabelFrame(main_content, text="範例參考 (Reference)", font=("微軟正黑體", 10, "bold"), 
                                    padx=10, pady=10, bg=self.bg_color, fg=self.fg_color)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.preview_label = tk.Label(right_panel, text="請點選左側列表\n查看範例圖片", font=("微軟正黑體", 10), 
                                      fg=self.drop_fg, bg=self.bg_color)
        self.preview_label.pack(expand=True, fill=tk.BOTH)

        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="📂 打開 steps 資料夾", bg="#FFC107", fg="black", font=("微軟正黑體", 11), 
                  command=self.open_folder, bd=0).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="✅ 設定完成", bg="#4CAF50", fg="white", font=("微軟正黑體", 11, "bold"), 
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
            
            self.drop_frame.config(text=f"設定: {self.selected_file}", fg=self.accent_color)
            target_bg = "#2D2D30" if self.is_dark else "#E3F2FD"
            target_fg = "#FFFFFF" if self.is_dark else "black"
            self.drop_label.config(text=f"請將【{self.selected_file}】的截圖拖曳至此\n(自動轉檔命名)", fg=target_fg, bg=target_bg)
            
            example_path = os.path.join(self.examples_folder, self.selected_file)
            if os.path.exists(example_path):
                try:
                    img = Image.open(example_path)
                    img.thumbnail((300, 300))
                    self.img_cache = ImageTk.PhotoImage(img)
                    self.preview_label.config(image=self.img_cache, text="")
                except Exception:
                    self.preview_label.config(image="", text="[範例圖片損毀]")
            else:
                self.preview_label.config(image="", text="[無範例圖片]\n開發者未提供此步驟的範例")

    def on_drop(self, event):
        if not self.selected_file:
            messagebox.showwarning("提示", "請先在左側列表點選你要設定哪一張圖片！")
            return
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'): file_path = file_path[1:-1]
        try:
            img = Image.open(file_path)
            target_path = os.path.join(self.steps_folder, self.selected_file)
            img.save(target_path, "PNG")
            
            success_bg = "#1B5E20" if self.is_dark else "#C8E6C9"
            self.drop_label.config(text=f"✅ {self.selected_file} 設定成功！", bg=success_bg)
            self.refresh_list()
            self.after(1500, lambda: self.reset_drop_zone())
        except Exception as e:
            messagebox.showerror("錯誤", f"圖片處理失敗：\n{e}")

    def reset_drop_zone(self):
        if self.selected_file:
             target_bg = "#2D2D30" if self.is_dark else "#E3F2FD"
             target_fg = "#FFFFFF" if self.is_dark else "black"
             self.drop_label.config(text=f"請將【{self.selected_file}】的截圖拖曳至此", bg=target_bg, fg=target_fg)
        else:
             self.drop_label.config(text="請先從上方選擇項目", bg=self.drop_bg, fg=self.drop_fg)

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
        self.root.title("閃十一編年史機器人 By Kartol")
        self.root.geometry("650x650") 
        
        # === 設定 ICON ===
        icon_path = resource_path("app.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path) 
            except Exception as e:
                print(f"圖示載入失敗: {e}")

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
        except Exception as e:
            print(f"熱鍵註冊失敗: {e}")

        # 開關
        self.toggle_switch = ModernToggle(root, command=self.toggle_theme, width=80, height=35)
        self.toggle_switch.place(relx=0.95, rely=0.02, anchor="ne")

        # 分頁
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=(50, 10))

        self.tab_main = tk.Frame(self.notebook)
        self.tab_logs = tk.Frame(self.notebook)
        self.tab_stats = tk.Frame(self.notebook)

        self.notebook.add(self.tab_main, text="主控制台")
        self.notebook.add(self.tab_logs, text="詳細日誌")
        self.notebook.add(self.tab_stats, text="循環紀錄")

        # === Tab 1: 主控制台 ===
        self.tab_main.config(bd=0, highlightthickness=0)
        
        # [修改] 使用 RoundedFrame (修復後)
        self.card_info = RoundedFrame(self.tab_main, width=580, height=200, radius=15)
        self.card_info.pack(pady=(20, 10))

        # === 時鐘 (放在卡片最上方) ===
        self.lbl_clock = tk.Label(self.tab_main, text="", font=("Consolas", 11), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_clock, 290, 30)
        self.update_clock() 

        self.lbl_status = tk.Label(self.tab_main, text="狀態: 就緒", font=("微軟正黑體", 18, "bold"), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_status, 290, 80)
        
        self.lbl_count = tk.Label(self.tab_main, text="已完成循環: 0 次", font=("微軟正黑體", 15, "bold"), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_count, 290, 120)
        
        self.lbl_last_time = tk.Label(self.tab_main, text="上回耗時: -- 秒", font=("微軟正黑體", 13), bg=self.card_info.bg_color)
        self.card_info.add_widget(self.lbl_last_time, 290, 160)

        # 控制卡片
        self.card_ctrl = RoundedFrame(self.tab_main, width=580, height=150, radius=15)
        self.card_ctrl.pack(pady=10)

        self.btn_start = RoundedButton(self.tab_main, text="開始執行", width=180, height=50, radius=25, 
                                     bg_color="#4CAF50", hover_color="#45a049", command=self.start_bot)
        self.card_ctrl.add_widget(self.btn_start, 290, 40)
        
        self.btn_stop = RoundedButton(self.tab_main, text="停止執行", width=180, height=50, radius=25, 
                                    bg_color="#F44336", hover_color="#d32f2f", command=self.stop_bot, state="disabled")
        self.card_ctrl.add_widget(self.btn_stop, 290, 100)

        # 說明區
        self.lbl_instruction = tk.Label(self.tab_main, text="[F9] 啟動機器人 / 新循環\n[F10] 暫停  |  [ESC] 停止", font=("微軟正黑體", 11), justify=tk.CENTER)
        self.lbl_instruction.pack(side=tk.BOTTOM, pady=40)
        
        # 設定按鈕 (改成圓角按鈕)
        self.btn_help = RoundedButton(self.tab_main, text="⚙️ 圖片設定", width=100, height=30, radius=15,
                                      bg_color="#444444", hover_color="#555555", fg_color="white",
                                      command=lambda: self.check_missing_files(force_show=True))
        self.btn_help.place(relx=0.03, rely=0.97, anchor="sw")

        # === 版本與作者資訊 (右下角) ===
        self.lbl_version = tk.Label(self.tab_main, text="v0.1 | 作者: Kartol", font=("微軟正黑體", 9))
        self.lbl_version.place(relx=0.97, rely=0.97, anchor="se")

        # === Tab 2 & 3 ===
        self.log_area = scrolledtext.ScrolledText(self.tab_logs, width=70, height=25, font=("Consolas", 10), bd=0, highlightthickness=0)
        self.log_area.pack(expand=True, fill='both', padx=2, pady=2) 
        self.log_area.config(state='disabled') 

        columns = ("id", "time", "duration", "avg")
        self.tree = ttk.Treeview(self.tab_stats, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="#"); self.tree.column("id", width=50, anchor="center")
        self.tree.heading("time", text="完成時間"); self.tree.column("time", width=150, anchor="center")
        self.tree.heading("duration", text="耗時 (秒)"); self.tree.column("duration", width=100, anchor="center")
        self.tree.heading("avg", text="平均耗時 (秒)"); self.tree.column("avg", width=120, anchor="center")
        
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
            SetupWizard(self.root, self.steps_folder, self.templates_folder, missing, is_dark=self.is_dark_mode)

    def toggle_theme(self):
        self.is_dark_mode = self.toggle_switch.is_dark 
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            # 深色配色
            bg_color, fg_color = "#000000", "#FFFFFF"      
            card_bg = "#1A1A1A"
            card_border = "#FFFFFF" 
            text_bg, text_fg = "#111111", "#E0E0E0"       
            count_fg, time_fg, instr_fg = "#4FC3F7", "#FFB74D", "#81D4FA"
            clock_fg = "#AAAAAA"
            version_fg = "#666666"
            
            tab_bg, tab_fg = "#1A1A1A", "#808080"
            tab_sel_bg, tab_sel_fg = "#000000", "#4FC3F7"
            tree_bg, tree_fg = "#111111", "#E0E0E0"
            head_bg, head_fg = "#1A1A1A", "#FFFFFF"
            btn_start_bg, btn_start_hover = "#388E3C", "#2E7D32"
            btn_stop_bg, btn_stop_hover = "#D32F2F", "#C62828"
            
            btn_help_bg, btn_help_hover, btn_help_fg = "#444444", "#555555", "#FFFFFF"
            btn_help_border = "#FFFFFF"
        else:
            # 淺色配色
            bg_color, fg_color = "#F0F0F0", "#000000"
            card_bg = "#FFFFFF"
            card_border = "#CCCCCC" 
            text_bg, text_fg = "#FFFFFF", "#000000"
            count_fg, time_fg, instr_fg = "#007ACC", "#E65100", "blue"
            clock_fg = "#555555"
            version_fg = "#888888"

            tab_bg, tab_fg = "#E0E0E0", "#000000"
            tab_sel_bg, tab_sel_fg = "#F0F0F0", "#007ACC"
            tree_bg, tree_fg = "#FFFFFF", "#000000"
            head_bg, head_fg = "#E0E0E0", "#000000"
            btn_start_bg, btn_start_hover = "#4CAF50", "#45a049"
            btn_stop_bg, btn_stop_hover = "#F44336", "#d32f2f"
            
            btn_help_bg, btn_help_hover, btn_help_fg = "#E0E0E0", "#D0D0D0", "#000000"
            btn_help_border = "#AAAAAA"

        self.toggle_switch.update_bg(bg_color)
        self.btn_start.update_colors(btn_start_bg, btn_start_hover, card_bg)
        self.btn_stop.update_colors(btn_stop_bg, btn_stop_hover, card_bg)
        
        # 更新設定按鈕顏色和邊框
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
        
        # [關鍵修正] 使用新的 update_colors 方法，傳入 parent_bg
        self.card_info.update_colors(card_bg, card_border, bg_color)
        self.card_ctrl.update_colors(card_bg, card_border, bg_color)

        for widget in [self.lbl_clock, self.lbl_status, self.lbl_count, self.lbl_last_time]:
            widget.config(bg=card_bg)

        self.lbl_status.config(fg=fg_color if self.is_dark_mode else "#333333")
        self.lbl_count.config(fg=count_fg)
        self.lbl_last_time.config(fg=time_fg)
        
        self.lbl_clock.config(fg=clock_fg)
        self.lbl_version.config(bg=bg_color, fg=version_fg)

        self.lbl_instruction.config(bg=bg_color, fg=instr_fg)
        self.log_area.config(bg=text_bg, fg=text_fg, insertbackground=fg_color)
        self.btn_help.config(bg=btn_help_bg) # 注意 Canvas 背景

    def switch_to_game(self):
        target_name = "INAZUMA ELEVEN"
        self.log_msg(f"正在搜尋視窗: {target_name}...")
        try:
            windows = gw.getWindowsWithTitle(target_name)
            if windows:
                win = windows[0]
                if win.isMinimized: win.restore()
                win.activate()
                self.log_msg(f"已鎖定並切換至遊戲視窗")
                return True
            else:
                self.log_msg(f"警告: 找不到 '{target_name}' 視窗，請確認遊戲已開啟")
                return False
        except Exception as e:
            self.log_msg(f"視窗切換失敗 (請嘗試以管理員身分執行): {e}")
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
                self.log_area.insert(tk.END, f" [圖檔遺失]")
        except Exception as e:
            self.log_area.insert(tk.END, f"[圖片錯誤]")
            print(e)
        self.log_area.insert(tk.END, "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def update_status(self, text, color):
        self.lbl_status.config(text=f"狀態: {text}", fg=color)

    def update_loop_info(self, last_duration=None):
        self.lbl_count.config(text=f"已完成循環: {self.loop_count} 次")
        if last_duration is not None:
            m, s = divmod(last_duration, 60)
            time_str = f"{int(m)}分 {int(s)}秒" if m > 0 else f"{int(s)}秒"
            self.lbl_last_time.config(text=f"上回耗時: {time_str}")
            self.update_stats_table(last_duration)

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
            self.lbl_last_time.config(text="上回耗時: -- 秒")
            self.image_refs.clear()
            self.log_area.config(state='normal')
            self.log_area.delete(1.0, tk.END)
            self.log_area.config(state='disabled')

            self.btn_start.set_state("disabled")
            self.btn_stop.set_state("normal")
            self.update_status("執行中...", "green")
            self.log_msg("=== 機器人已啟動 ===")

            self.notebook.select(self.tab_logs)
            self.switch_to_game()

            self.bot_thread = threading.Thread(target=self.run_bot_logic)
            self.bot_thread.daemon = True 
            self.bot_thread.start()

    def stop_bot(self):
        self.is_running = False
        self.btn_start.set_state("normal")
        self.btn_stop.set_state("disabled")
        self.update_status("已停止", "red")
        self.log_msg("=== 使用者已停止機器人 ===")

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
            self.log_msg("\n=== 開始新的循環 ===")
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
                        self.log_msg(f"步驟 {old_index+1} 超時 → 返回步驟 {step_index+1}")
                    else:
                        step_index = on_fail
                        self.log_msg(f"步驟 {old_index+1} 超時 → 跳轉至步驟 {on_fail+1}")
                    step_start_time = time.time()
                    continue

                try:
                    if action_type == "click":
                        img_path = os.path.join(self.steps_folder, target)
                        if not os.path.exists(img_path):
                            self.log_msg(f"錯誤: 找不到 {target}")
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
                                log_text = f"已點擊 ({i+1}/{repeat}): "
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
                            self.log_msg(f"原地盲點擊 ({i+1}/{repeat})")
                            if i < repeat - 1:
                                if self.smart_sleep(repeat_interval):
                                    restart_triggered = True
                                    break
                        if restart_triggered: break
                        step_index += 1
                        step_start_time = time.time()
                    elif action_type == "key":
                        self.log_msg(f"步驟 {step_index+1}: 按住 {target.upper()} 鍵")
                        pyautogui.keyDown(target)
                        time.sleep(0.15) 
                        pyautogui.keyUp(target)
                        step_index += 1
                        step_start_time = time.time()
                    elif action_type == "wait":
                        sec = step.get("seconds", 1)
                        self.log_msg(f"步驟 {step_index+1}: 等待 {sec} 秒")
                        if self.smart_sleep(sec): break 
                        step_index += 1
                        step_start_time = time.time()
                except pyautogui.ImageNotFoundException:
                    pass
                except Exception as e:
                    self.log_msg(f"錯誤: {e}")
                if self.smart_sleep(0.5): break
            
            end_time = time.time()
            duration = end_time - self.loop_start_timestamp
            self.loop_count += 1
            self.update_loop_info(duration)
            self.log_msg(f"=== 循環結束 | 耗時: {duration:.2f} 秒 ===")
            time.sleep(1)
        self.stop_bot()

    def smart_sleep(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration or duration == 0:
            if not self.is_running: return True 
            if keyboard.is_pressed('F9'):
                self.log_msg("熱鍵: F9 (開始新循環)")
                while keyboard.is_pressed('F9'): time.sleep(0.1)
                return True 
            if keyboard.is_pressed('F10'):
                self.is_paused = not self.is_paused
                status_text = "暫停中" if self.is_paused else "執行中..."
                color = "orange" if self.is_paused else "green"
                self.update_status(status_text, color)
                self.log_msg(f"熱鍵: F10 ({status_text})")
                while keyboard.is_pressed('F10'): time.sleep(0.1)
                while self.is_paused and self.is_running:
                    if keyboard.is_pressed('F10'):
                        self.is_paused = False
                        self.update_status("執行中...", "green")
                        self.log_msg("已恢復執行!")
                        while keyboard.is_pressed('F10'): time.sleep(0.1)
                    time.sleep(0.1)
            if keyboard.is_pressed('esc'):
                self.log_msg("熱鍵: ESC (停止程式)")
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
