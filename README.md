# ⚡ Inazuma Chronicle Bot (閃十一編年史機器人)

這是一個為《閃電十一人編年史》設計的自動化掛機機器人，具備現代化的深色介面、智慧設定精靈與防呆機制。

![Version](https://img.shields.io/badge/version-v0.1.4-blue)
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
