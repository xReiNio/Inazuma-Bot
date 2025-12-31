# ⚡ Inazuma Chronicle Bot

A modern, automated farming bot for **Inazuma Eleven: Victory Road (Chronicle Mode)**.  
Designed with a sleek dark UI, ease of use, and stability in mind.

![Version](https://img.shields.io/badge/version-v0.1.3-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![License](https://img.shields.io/badge/license-MIT-green)

> 🇹🇼 **中文說明請往下滑 (Scroll down for Chinese instructions)**

---

## ✨ Features

### 🤖 Automation
* **Auto-Loop**: Automatically handles level selection, battle sequences, and result screens.
* **Background Lock**: Detects and locks onto the game window automatically.
* **Smart Recovery**: Includes timeouts and retry mechanisms to prevent getting stuck.

### 🎨 Modern UI
* **Deep Dark Mode**: A comfortable, borderless dark theme with rounded corners.
* **Multi-Language**: Switch between **English** and **Traditional Chinese** instantly.
* **Dashboard**: Real-time stats including loop count, duration, and average time.

### 🚀 Smart Setup Wizard
* **Clipboard Paste**: Simply take a screenshot (`Win+Shift+S`) and press **`Ctrl+V`** in the bot to set up images. No file saving required!
* **Single File**: The bot comes as a standalone `.exe`. No installation or extra folders needed.

---

## 📥 Installation

### Method 1: Pre-built EXE (Recommended)
1.  Go to the [Releases Page](../../releases) and download the latest `InazumaBot_v0.1.3.zip`.
2.  Unzip the file.
3.  Right-click `InazumaBot.exe` and select **"Run as Administrator"**.
    * *Note: This is required for hotkeys and mouse control to work properly.*

### Method 2: Run from Source
1.  Clone the repository:
    ```bash
    git clone [[https://github.com/xReiNio/Inazuma-Chronicle-Bot](https://github.com/xReiNio/Inazuma-Bot).git]([https://github.com/xReiNio/Inazuma-Chronicle-Bot](https://github.com/xReiNio/Inazuma-Bot).git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the bot:
    ```bash
    python bot.py
    ```

---

## 🎮 How to Use

1.  **Initial Setup**:
    * On the first launch, the **Setup Wizard** will appear.
    * Select an image from the list (e.g., `Picture1.png`).
    * Take a screenshot of the corresponding button in your game.
    * Press **`Ctrl+V`** in the bot to paste it.
    * Repeat for all images and click "Done".

2.  **Hotkeys**:
    * `F9`: Start Bot / Start New Loop
    * `F10`: Pause / Resume
    * `ESC`: Stop Bot

---

## 📦 Build Instructions

To build the standalone `.exe` yourself, use **PyInstaller**:

```bash
pyinstaller --noconsole --onefile --icon=app.ico --name="InazumaBot" --collect-all tkinterdnd2 --add-data "app.ico;." --add-data "templates;templates" bot.py

```

---

# 🇹🇼 閃電十一人編年史 自動掛機機器人

專為《閃電十一人：英雄勝利之路》設計的現代化自動掛機工具。具備深色介面、多語言支援與智慧設定功能。

## ✨ 功能特色

* **全自動掛機**：自動點擊關卡、戰鬥、結算畫面，支援無限循環。
* **極致黑介面**：全新圓角設計與擬真日夜開關，視覺舒適。
* **多語言支援**：內建 **繁體中文** 與 **英文**，可一鍵切換。
* **智慧設定精靈**：支援 **剪貼簿貼上**！使用系統截圖 (`Win+Shift+S`) 後，直接按下 **`Ctrl+V`** 即可匯入圖片，設定只需 2 秒。
* **單檔執行**：範例圖片已內建於程式中，無需額外下載資源包。

## 📥 下載與教學

1. 前往 [Release](../../releases) 下載最新的 `.zip` 檔。
2. 解壓縮後，右鍵點擊 `InazumaBot.exe` 選擇 **「以系統管理員身分執行」**。
* *注意：初次執行會自動在旁邊建立 `steps` 資料夾用於儲存您的設定。*


3. **初次設定**：
* 依照提示選擇項目 (如 `Picture1.png`)。
* 在遊戲中截圖對應按鈕。
* 回到程式按 `Ctrl+V` 貼上。


4. **熱鍵**：
* `F9`: 啟動 / 新循環
* `F10`: 暫停
* `ESC`: 停止



---

## 👤 Author

**Kartol** [GitHub Profile](https://github.com/xReiNio)

```

```
