# 大樂透動力學預測儀 (Taiwan Lotto 6/49 Dynamics Engine)

本專案是一個基於**台灣彩券大樂透歷史真實開獎大數據**與**非線性時間衰減轉移矩陣**的數理實驗網頁。

專案遵循 **Google Modern Web Guidance** 規範，針對安全性（CSP、零危險 DOM 匯入）、無障礙（WCAG 2.1 AA、ARIA Live Regions、鍵盤導航）、效能（Compositor-accelerated CSS 動畫、Reduced Motion 支援）進行了全面強化。

---

## 專案目錄結構

```text
taiwan-lotto-project/
├── .github/
│   └── workflows/
│       └── auto_sync.yml       # GitHub Actions 每週二、五定時自動抓取最新開獎
├── data/
│   └── lotto649.json           # 800+ 期完整歷史大樂透中央資料庫
├── scripts/
│   └── sync_lotto.py           # 自動化增量爬蟲同步腳本 (Python)
├── public/
│   ├── index.html              # 高效能、安全合規的前端單頁應用 (SPA)
│   └── data/
│       └── lotto649.json       # 供前端靜態請求的高速 JSON 鏡像
└── README.md
```

---

## 採用「方案 A：GitHub Actions 自動化」的運作機制

1. **零成本、零維護：**
   * 透過 `.github/workflows/auto_sync.yml`，GitHub 的雲端伺服器會在**每週二、每週五晚上 21:00（UTC 13:00）**自動喚醒。
   * 執行 `scripts/sync_lotto.py` 自動向台彩檢查有無最新一期開獎。
   * 若有新開獎，自動 commit 並 push 回你的 repository，整個過程你完全不用手動操作。

2. **一人更新，萬人秒讀：**
   * 所有訪客打開網頁時，都是直接讀取 GitHub Pages 部署的高速靜態 `data/lotto649.json`。
   * 訪客的瀏覽器完全不需要爬蟲，0 延遲、0 跨域問題（CORS），即使使用者隔了半年沒上線，一進來也是瞬間載入最新資料！

---

## 如何在 GitHub 上部署上線？（5 分鐘三步驟）

1. **建立 GitHub 儲存庫：**
   在你的 GitHub 帳號下建立一個新的 Repository（例如命名為 `taiwan-lotto-649`）。
2. **上傳本專案所有檔案：**
   將本專案目錄下的所有檔案（含 `.github` 資料夾）推送到該倉庫的 `main` 分支。
3. **啟用 GitHub Pages：**
   * 到 GitHub 儲存庫的 **Settings > Pages**。
   * 在 **Build and deployment** 下的 **Branch** 選擇 `main`，資料夾選擇 `/public`（或 `/root`，若選 root 請將 public 內檔案移到根目錄），點擊 **Save**。
   * 稍等 1 分鐘，GitHub 就會為你產生一個專屬網址（例如 `https://yourname.github.io/taiwan-lotto-649/`）！

---

## 遵循 Google Modern Web Guidance 之規範說明

* **安全性（Web Security）：**
  * 配置嚴格的 `Content-Security-Policy`（CSP）以及 `referrer: no-referrer-when-downgrade`。
  * 杜絕危險 DOM Sinks（完全廢除 `innerHTML` 拼接，全數採用原生 `textContent`、`createElement` 與 `replaceChildren`）。
* **無障礙體驗（Accessibility / WCAG AA）：**
  * 具備完整語意結構（`<header>`、`<main>`、`<article>`、`<footer>`，每個區塊具有獨立清晰的 `aria-labelledby` 與 Accessible Names）。
  * 支援鍵盤使用者友善的 `Skip Link`（跳至主要內容）與可視焦點外框（Focus Ring）。
  * 支援螢幕閱讀器實時廣播（`aria-live="polite"`），拉霸開出號碼時視障朋友也能立即聽見語音廣播。
* **效能與動畫（Motion & CWV）：**
  * 拉霸轉軸採用 GPU 複合層硬體加速（`will-change: transform`，僅位移 `translateY`，避開重排 Reflow）。
  * 完整適配系統使用者「減少動畫偏好」（`prefers-reduced-motion`），開啟省電或易暈眩設定的使用者可直出結果，避免過度動畫。
