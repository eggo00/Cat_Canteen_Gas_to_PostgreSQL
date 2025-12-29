# 🐾 Cat Claws 貓咪食堂 v2.0

一個可愛的貓咪主題訂餐系統，使用 Python + FastAPI + PostgreSQL 開發，可部署到 Zeabur 雲端平台。

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)

## ✨ 特色功能

- 🎨 **可愛貓咪主題** - 純 CSS 繪製的貓咪動畫
- 📱 **響應式設計** - 完美支援手機和桌面裝置
- 🛡️ **安全防護** - XSS 防護、輸入驗證、價格驗證
- 🚀 **高性能** - FastAPI 異步架構
- 📊 **資料分析** - 內建 pandas/numpy，可擴充分析功能
- 🔄 **自動 API 文檔** - Swagger UI 和 ReDoc
- ☁️ **雲端部署** - 支援 Zeabur 一鍵部署

## 📋 功能列表

### 前端功能
- ✅ 選單瀏覽（主食、湯品、點心、飲料）
- ✅ 購物車管理
- ✅ 飲料客製化（溫度、甜度）
- ✅ 訂單送出
- ✅ 訂單編號顯示

### 後端功能
- ✅ RESTful API
- ✅ PostgreSQL 資料庫
- ✅ 訂單驗證（價格、數量、格式）
- ✅ 安全防護（XSS、SQL Injection）
- ✅ 錯誤記錄
- ✅ 健康檢查端點

### 未來擴充（Python 優勢）
- 📊 資料分析儀表板
- 🤖 AI 推薦系統
- 📈 營收統計報表
- 🔔 LINE Bot 整合

## 🛠️ 技術棧

### 後端
- **框架**: FastAPI 0.104+
- **資料庫**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **驗證**: Pydantic
- **Web 伺服器**: Uvicorn

### 前端
- **HTML5** + **CSS3**
- **Vanilla JavaScript**（無框架）
- **Jinja2** 模板引擎

### 資料分析（可選）
- **pandas** - 資料處理
- **numpy** - 數值計算
- **matplotlib / plotly** - 資料視覺化

## 📦 快速開始

### 1. 環境需求

- Python 3.11+
- PostgreSQL 15+
- pip

### 2. 安裝相依套件

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安裝套件
pip install -r requirements.txt
```

### 3. 設定環境變數

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，設定資料庫連線
nano .env
```

```.env
DATABASE_URL=postgresql://user:password@localhost:5432/cat_canteen
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 4. 初始化資料庫

```bash
# 建立資料表
python scripts/init_db.py
```

### 5. 啟動開發伺服器

```bash
# 方法 1：直接執行
python -m uvicorn app.main:app --reload

# 方法 2：使用 main.py
python app/main.py
```

訪問：
- 主頁：http://localhost:8000
- API 文檔：http://localhost:8000/api/docs
- 健康檢查：http://localhost:8000/health

## 🚀 部署到 Zeabur

### 方法一：GitHub 連接（推薦）

1. **推送程式碼到 GitHub**
   ```bash
   git add .
   git commit -m "Migrate to Python + FastAPI + PostgreSQL"
   git push origin main
   ```

2. **在 Zeabur 建立專案**
   - 訪問 [Zeabur](https://zeabur.com)
   - 建立新專案
   - 連接 GitHub Repository

3. **新增 PostgreSQL 服務**
   - 點擊「Add Service」
   - 選擇「PostgreSQL」
   - Zeabur 會自動建立資料庫

4. **設定環境變數**
   ```env
   DATABASE_URL=${POSTGRES_URL}  # Zeabur 自動提供
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ```

5. **部署**
   - Zeabur 會自動偵測 Python 專案
   - 自動安裝 requirements.txt
   - 自動啟動應用

### 方法二：Zeabur CLI

```bash
# 安裝 Zeabur CLI
npm install -g @zeabur/cli

# 登入
zeabur login

# 部署
zeabur deploy
```

## 📂 專案結構

```
Cat_Canteen_PostgreSQL/
├── app/                        # 應用程式主目錄
│   ├── models/                 # 資料模型（SQLAlchemy）
│   │   └── order.py           # 訂單模型
│   ├── schemas/                # 資料驗證（Pydantic）
│   │   └── order.py           # 訂單 schema
│   ├── routers/                # API 路由
│   │   ├── orders.py          # 訂單 API
│   │   └── menu.py            # 選單 API
│   ├── services/               # 業務邏輯
│   │   ├── order_service.py   # 訂單服務
│   │   └── menu_service.py    # 選單服務
│   ├── utils/                  # 工具函數
│   │   ├── validation.py      # 輸入驗證
│   │   └── order_number.py    # 訂單編號生成
│   ├── config.py              # 配置管理
│   ├── database.py            # 資料庫連線
│   └── main.py                # FastAPI 主程式
│
├── static/                     # 靜態檔案
│   ├── css/
│   │   └── styles.css         # 樣式表
│   └── js/
│       └── script.js          # 前端腳本
│
├── templates/                  # HTML 模板
│   └── index.html             # 主頁面
│
├── scripts/                    # 工具腳本
│   ├── init_db.py             # 資料庫初始化
│   └── migrate_from_sheets.py # Google Sheets 遷移（可選）
│
├── requirements.txt            # Python 依賴
├── .env.example               # 環境變數範本
├── .gitignore                 # Git 忽略規則
└── README.md                  # 專案說明
```

## 🔌 API 端點

### 選單 API
- `GET /api/menu/` - 取得完整選單
- `GET /api/menu/item/{item_id}` - 取得單一餐點

### 訂單 API
- `POST /api/orders/` - 建立訂單
- `GET /api/orders/` - 取得訂單列表
- `GET /api/orders/{order_number}` - 查詢訂單

### 系統
- `GET /` - 主頁面
- `GET /health` - 健康檢查
- `GET /api` - API 資訊
- `GET /api/docs` - Swagger API 文檔
- `GET /api/redoc` - ReDoc API 文檔

## 🎨 選單項目

### 主食 🍛
- 貓爪咖哩飯 - NT$ 120
- 鮭魚親子丼 - NT$ 150
- 喵喵義大利麵 - NT$ 130
- 貓掌漢堡排 - NT$ 140

### 湯品 🍲
- 貓咪味噌湯 - NT$ 30
- 奶油南瓜濃湯 - NT$ 40
- 海鮮巧達湯 - NT$ 50

### 點心 🍰
- 貓掌布丁 - NT$ 60
- 鮮奶雪花冰 - NT$ 70
- 焦糖烤布蕾 - NT$ 65
- 貓咪銅鑼燒 - NT$ 55

### 飲料 🥤
- 貓爪拿鐵 - NT$ 80
- 焦糖瑪奇朵 - NT$ 90
- 抹茶拿鐵 - NT$ 85
- 水果茶 - NT$ 70
- 檸檬冰茶 - NT$ 60

## 🛡️ 安全機制

1. **輸入驗證** - Pydantic schema 自動驗證
2. **XSS 防護** - HTML 特殊字元轉義
3. **價格驗證** - 後端驗證防止前端竄改
4. **SQL Injection 防護** - SQLAlchemy ORM 參數化查詢
5. **錯誤處理** - 完整的錯誤記錄，不暴露敏感資訊

## 📊 資料庫結構

### orders 資料表

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | Integer | 主鍵 |
| order_number | String(20) | 訂單編號（CAT + YYMMDDHHmmss）|
| customer_name | String(100) | 顧客姓名 |
| pickup_method | String(20) | 取餐方式（內用/外帶）|
| items | JSON | 餐點明細 |
| drinks | JSON | 飲料明細 |
| total_amount | Integer | 總金額 |
| notes | Text | 備註 |
| created_at | DateTime | 建立時間 |

## 🔧 開發

### 執行測試

```bash
# 安裝測試套件
pip install pytest pytest-asyncio httpx

# 執行測試
pytest
```

### 資料庫遷移（Alembic）

```bash
# 初始化 Alembic
alembic init alembic

# 建立遷移
alembic revision --autogenerate -m "description"

# 執行遷移
alembic upgrade head
```

### 程式碼格式化

```bash
# 安裝工具
pip install black isort

# 格式化
black app/
isort app/
```

## 🐛 常見問題

### 1. 資料庫連線失敗

檢查 `.env` 的 `DATABASE_URL` 是否正確：
```env
DATABASE_URL=postgresql://user:password@localhost:5432/cat_canteen
```

### 2. 靜態檔案無法載入

確認目錄結構正確：
```
static/
├── css/styles.css
└── js/script.js
```

### 3. 訂單送出失敗

檢查瀏覽器 Console 錯誤訊息，確認 API 端點正確。

## 📝 版本歷史

### v2.0.0 (2025-01-XX)
- 🎉 從 Google Apps Script 遷移到 Python + FastAPI
- 🗄️ 改用 PostgreSQL 資料庫
- 🚀 支援 Zeabur 雲端部署
- 📊 加入資料分析能力（pandas/numpy）
- 📚 自動 API 文檔（Swagger）

### v1.0.0
- ✅ 基於 Google Apps Script 的訂餐系統
- ✅ 使用 Google Sheets 儲存訂單

## 📄 授權

MIT License

## 👨‍💻 開發者

由 Claude Code 協助完成從 GAS 到 Python + FastAPI 的遷移。

## 🙏 致謝

- FastAPI - 現代化的 Python Web 框架
- SQLAlchemy - 強大的 Python ORM
- Zeabur - 優秀的雲端部署平台

---

🐾 **Cat Claws 貓咪食堂** - 喵～歡迎光臨！
