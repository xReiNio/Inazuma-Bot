# ⚡ Inazuma Chronicle Bot (閃十一編年史機器人)

這是一個為《閃電十一人編年史》設計的自動化掛機機器人，具備現代化的深色介面與防呆機制。

![Version](https://img.shields.io/badge/version-v0.1-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)

## ✨ 功能特色

* **全自動循環**：自動點擊關卡、戰鬥、結算，支援無限循環掛機。
* **現代化 UI**：
    * 支援 **深色/淺色模式** 切換 (含擬真日夜開關)。
    * 圓角按鈕與卡片式設計，視覺舒適。
* **智慧防呆**：
    * **初始設定精靈**：支援拖放截圖，自動轉檔與歸檔。
    * **自動視窗對焦**：循環開始前自動鎖定遊戲視窗，避免點錯。
    * **斷點恢復**：偵測圖片失敗時具備超時重試機制。
* **數據統計**：即時顯示循環次數、單次耗時與平均耗時。

## 🛠️ 安裝與使用

### 方法一：直接執行 (推薦)
前往 [Releases 頁面](這裡貼上你之後發布exe的網址) 下載最新的 `.exe` 檔案，解壓縮後直接執行即可，無需安裝 Python。

### 方法二：原始碼執行
如果你想自行修改代碼：

1.  克隆此專案：
    ```bash
    git clone [https://github.com/你的帳號/Inazuma-Chronicle-Bot.git](https://github.com/你的帳號/Inazuma-Chronicle-Bot.git)
    ```
2.  安裝依賴套件：
    ```bash
    pip install -r requirements.txt
    ```
3.  執行程式：
    ```bash
    python bot.py
    ```

## 🎮 使用說明

1.  **截圖設定**：
    * 初次開啟程式若缺少圖片，會自動跳出「設定精靈」。
    * 依照提示截取遊戲中的按鈕，並拖入視窗中即可。
2.  **熱鍵操作**：
    * `F9`: 啟動機器人 / 開始新循環
    * `F10`: 暫停 / 繼續
    * `ESC`: 強制停止

## 📦 打包方式

若要自行打包成 exe，請使用以下指令：
```bash
pyinstaller --noconsole --onefile --icon=app.ico --name="InazumaBot" --collect-all tkinterdnd2 --add-data "app.ico;." bot.py