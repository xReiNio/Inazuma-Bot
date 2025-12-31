# ⚡ Inazuma Bot

A modern, automated farming bot for **Inazuma Eleven: Victory Road**.  
Designed with a sleek dark UI, ease of use, and stability in mind.

![Version](https://img.shields.io/badge/version-v0.1.3-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![License](https://img.shields.io/badge/license-MIT-green)

> **[繁體中文說明 (Chinese Version)](./README_zh.md)**

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
1.  Go to the [Releases Page](../../releases) and download the latest `InazumaBot.exe`.
2.  Right-click `InazumaBot.exe` and select **"Run as Administrator"**.
    * *Note: This is required for hotkeys and mouse control to work properly.*

### Method 2: Run from Source
1.  Clone the repository:
    ```bash
    git clone [https://github.com/xReiNio/Inazuma-Bot.git](https://github.com/xReiNio/Inazuma-Bot.git)
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
👤 Author
Kartol (@xReiNio)


