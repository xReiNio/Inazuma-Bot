# ⚡ 閃電十一人編年史 自動掛機機器人

專為《閃電十一人：英雄勝利之路》設計的現代化自動掛機工具。  
具備深色介面、多語言支援與智慧設定功能。

![Version](https://img.shields.io/badge/version-v0.1.3-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![License](https://img.shields.io/badge/license-MIT-green)

> **[English Version (英文版)](./README.md)**

---

## ✨ 功能特色

### 🤖 全自動掛機
* **自動循環**：自動點擊關卡、戰鬥、結算畫面，支援無限循環。
* **背景鎖定**：循環開始前自動偵測並鎖定遊戲視窗，避免誤觸。
* **斷點恢復**：具備圖片偵測超時機制，卡住時會嘗試恢復或重試。

### 🎨 現代化 UI
* **極致黑介面**：全新圓角設計與擬真日夜開關，視覺舒適。
* **多語言支援**：內建 **繁體中文** 與 **英文**，可一鍵切換。
* **儀表板**：即時顯示時鐘、循環次數、單次耗時與平均耗時。

### 🚀 智慧設定精靈
* **支援剪貼簿貼上**：使用系統截圖 (`Win+Shift+S`) 後，直接在程式內按下 **`Ctrl+V`** 即可匯入圖片，設定只需 2 秒！
* **單檔執行**：範例圖片已內建於程式中，無需額外下載資源包。

---

## ⚠️ 重要注意事項

在執行機器人之前，請務必確認以下事項：

* **🖥️ 遊戲解析度**：
    建議將遊戲解析度設定為 **1600x900**。
    *否則機器人可能會無法識別圖片，導致腳本無法執行。*

* **📂 資料夾路徑**：
    存放此程式的資料夾路徑 **不能包含中文字元**。
    *請將機器人放在純英文的路徑下（例如：`C:\Games\InazumaBot`），否則可能會無法運作。*

---

## 📥 下載與教學

### 方法一：直接下載執行 (推薦)
1.  前往 [Releases 頁面](../../releases) 下載最新的 `InazumaBot.exe`。
2.  右鍵點擊 `InazumaBot.exe` 選擇 **「以系統管理員身分執行」**。
    * *注意：初次執行會自動在旁邊建立 `steps` 資料夾用於儲存您的設定。*

### 方法二：從原始碼執行
1.  複製專案：
    ```bash
    git clone [https://github.com/xReiNio/Inazuma-Bot.git](https://github.com/xReiNio/Inazuma-Bot.git)
    ```
2.  安裝套件：
    ```bash
    pip install -r requirements.txt
    ```
3.  執行程式：
    ```bash
    python bot.py
    ```

---

## 🎮 使用說明

1.  **初次設定**：
    * 第一次開啟時會跳出設定精靈。
    * 點選左側列表項目 (如 `Picture1.png`)。
    * 在遊戲中截圖對應按鈕。
    * 回到程式按 **`Ctrl+V`** 貼上。
    * 全部設定完成後點擊「設定完成」。

2.  **熱鍵操作**：
    * `F9`: 啟動機器人 / 開始新循環
    * `F10`: 暫停 / 繼續
    * `ESC`: 強制停止

---

## 📦 自行打包

若要自行編譯成 `.exe`，請使用以下指令：

```bash
pyinstaller --noconsole --onefile --icon=app.ico --name="InazumaBot" --collect-all tkinterdnd2 --add-data "app.ico;." --add-data "templates;templates" bot.py
```
👤 作者
Kartol (@xReiNio)
