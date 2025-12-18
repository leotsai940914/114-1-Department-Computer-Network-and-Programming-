# LumenFilm - 電影觀影筆記與影像解析平台 (Film Review Platform)

一個基於 Python Flask 構建的現代化內容管理系統 (CMS)，專注於影評撰寫、知識分享與影像美學解析。本專題展示了完整的全端開發能力，包含後端邏輯與前端互動設計。

![Project Status](https://img.shields.io/badge/status-finished-success)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

## ✨ 專案特色 (Features)

### 核心功能 (Core)
*   **會員系統 (RBAC)**：完整的註冊、登入機制，並區分 `Admin` (管理員)、`Author` (作者)、`User` (讀者) 三種權限角色。
*   **內容管理 (CRUD)**：支援文章的新增、編輯、刪除與暫存（草稿/發布狀態）。
*   **即時搜尋 (Search)**：支援標題與內文的關鍵字搜尋功能。
*   **分類索引**：支援多層級或標籤式的分類瀏覽。

### 前端體驗 (UI/UX)
*   **響應式設計 (RWD)**：完全自適應的手機、平板與桌面排版。
*   **深色模式 (Dark Mode)**：內建手動切換與系統自動偵測的深色主題，支援即時切換不閃爍。
*   **現代化介面**：使用 CSS Variables 構建的 Design Token 系統，擁有圓角卡片 (`10px`)、玻璃擬態導覽列 (Glassmorphism) 與高級陰影效果。
*   **互動細節**：微動畫 (Micro-interactions)、按鈕懸停效果、圖片燈箱 (Lightbox) 放大預覽。

### 進階功能 (Advanced)
*   **RSS 訂閱機制**：為每位作者自動生成 XML RSS Feed，符合標準 RSS 2.0 規範。
*   **分頁系統 (Pagination)**：首頁與作者頁支援伺服器端分頁，提升效能。
*   **安全性 (Security)**：全站 CSRF 防護、密碼雜湊儲存 (Werkzeug Security)、強制的權限驗證裝飾器。

---

## 🛠️ 技術棧 (Tech Stack)

*   **Backend**: Python, Flask, Jinja2
*   **Database**: SQLite (輕量級、免配置)
*   **Frontend**: HTML5, CSS3 (Custom Variables), JavaScript (Vanilla ES6)
*   **Library**:
    *   `Werkzeug`: 密碼加密
    *   `Quill.js`: 富文本編輯器 (Rich Text Editor)

---

## 🚀 快速開始 (Quick Start)

### 1. 安裝依賴
確保已安裝 Python 3.9 或以上版本。

```bash
# 建立虛擬環境 (Optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# 安裝套件
pip install -r requirements.txt
```

### 2. 初始化資料庫
系統會在第一次啟動時自動檢測並建立 `database.db`。

### 3. 啟動伺服器

```bash
python app.py
```

開啟瀏覽器訪問： `http://127.0.0.1:5000`

注意：本專案在 `app.py` 內設定使用 `port=8011`，因此實際網址通常是 `http://127.0.0.1:8011`

---

## 📂 專案結構 (Project Structure)

```text
.
├── app.py                 # 應用程式入口 (Entry Point)
├── config.py              # 設定檔 (Config)
├── models/                # 資料庫模型 (Data Layer)
│   ├── database.py        # DB 連線管理
│   ├── post_model.py      # 文章邏輯
│   ├── user_model.py      # 會員邏輯
│   └── ...
├── routes/                # 路由控制器 (Controllers)
│   ├── post_routes.py     # 文章相關路由
│   ├── auth_routes.py     # 認證相關路由
│   └── ...
├── static/                # 靜態檔案
│   ├── css/style.css      # 全站樣式 (CSS Variables)
│   └── js/main.js         # 前端腳本
└── templates/             # HTML 模板 (Jinja2)
    ├── base.html          # 基礎佈局
    ├── index.html         # 首頁
    └── post_detail.html   # 文章內頁
```

---

## 📝 關於開發者

Department of Computer Network and Programming - 114-1 Final Project.
Designed & Developed by **Tsai Cheng Yu**.
