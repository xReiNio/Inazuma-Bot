# ⚡ Inazuma Chronicle Bot (閃十一編年史機器人)

這是一個為《閃電十一人編年史》設計的自動化掛機機器人，具備現代化的深色介面、智慧設定精靈與防呆機制。

![Version](https://img.shields.io/badge/version-v0.1.2-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)

## ✨ 功能特色

### 🤖 全自動掛機
* **自動循環**：自動點擊關卡、戰鬥、結算畫面，支援無限循環掛機。
* **背景鎖定**：循環開始前自動偵測並鎖定遊戲視窗，避免誤觸其他視窗。
* **斷點恢復**：具備圖片偵測超時機制，卡住時會嘗試恢復或重試。

### 🎨 現代化 UI (v0.1.2+)
* **極致黑介面 (Deep Dark UI)**：全新圓角設計與無邊框介面，視覺舒適。
* **日夜模式切換**：內建擬真開關，可自由切換 深色 / 淺色 模式。
* **儀表板**：即時顯示時鐘、循環次數、單次耗時與平均耗時。

### 🚀 智慧設定精靈 (v0.1.4 New!)
* **支援剪貼簿貼上**：直接使用系統截圖 (`Win+Shift+S`) 後，按下 **`Ctrl+V`** 或點擊按鈕即可匯入圖片，設定只需 2 秒！
* **拖放支援**：也支援將圖片檔案直接拖入視窗。
* **單檔執行**：範例圖片已內建於程式中，無需額外下載資源包。

---

## 📥 下載與安裝

### 方法一：直接執行 (推薦)
1. 前往 [Releases 頁面](../../releases) 下載最新的 `.zip` 檔 (或 `.exe`)。
2. 解壓縮後，右鍵點擊 `InazumaBot.exe` 選擇 **「以系統管理員身分執行」**。
   * *注意：初次執行會自動在旁邊建立 `steps` 資料夾用於儲存您的設定。*

### 方法二：原始碼執行 (開發者用)
如果你想自行修改代碼：

1. 克隆此專案：
    ```bash
   git clone [https://github.com/xReiNio/Inazuma-Bot.git](https://github.com/xReiNio/Inazuma-Bot.git)

2. 安裝依賴套件：
  ```bash
  pip install -r requirements.txt

```


3. 執行程式：
  ```bash
  python bot.py

```



---

## 🎮 使用說明

### 1. 初次設定

第一次開啟時，程式會偵測缺少圖片並跳出「設定精靈」：

1. 在左側列表點選要設定的項目（如：`Picture1.png`）。
2. 在遊戲中截圖對應的按鈕（參考右側範例圖）。
3. 回到程式，直接按下 **`Ctrl+V`** 貼上，或是將圖片檔拖入下方框框。
4. 全部設定完成後，點擊「設定完成」。

### 2. 熱鍵操作

* **`F9`**：啟動機器人 / 開始新循環 (全域熱鍵)
* **`F10`**：暫停 / 繼續
* **`ESC`**：強制停止程式

---

## 📦 自行打包 (Build from Source)

若要自行將 `.py` 打包成單一 `.exe` 檔，請使用以下指令（需安裝 PyInstaller）：

```bash
pyinstaller --noconsole --onefile --icon=app.ico --name="InazumaBot" --collect-all tkinterdnd2 --add-data "app.ico;." --add-data "templates;templates" bot.py

```

---

## 👤 作者

**Kartol**


