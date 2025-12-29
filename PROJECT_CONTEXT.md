# Cat Claws 貓咪食堂 - 專案上下文

> **最後更新**: 2025-12-29
> **專案版本**: v2.0.0
> **狀態**: ✅ 遷移完成，本地測試通過

---

## 📋 專案概述

這是一個**可愛的貓咪主題訂餐系統**，已成功從 **Google Apps Script (GAS) + Google Sheets** 遷移到 **Python + FastAPI + PostgreSQL**。

### 核心特色
- 🎨 純 CSS 繪製的可愛貓咪動畫
- 📱 響應式設計（手機/桌面完美支援）
- 🛡️ 完整的安全防護（XSS、SQL Injection、價格驗證）
- 🚀 FastAPI 高性能異步架構
- 📊 內建資料分析能力（pandas/numpy）
- 📚 自動生成 API 文檔（Swagger UI）

---

## 🛠️ 技術棧

### 後端
- **框架**: FastAPI 0.104.1
- **Python 版本**: 3.9+
- **資料庫**: PostgreSQL 15.15
- **ORM**: SQLAlchemy 2.0.23
- **資料驗證**: Pydantic 2.5.0
- **Web 伺服器**: Uvicorn 0.24.0

### 前端
- **HTML5** + **CSS3** (純 CSS 動畫)
- **Vanilla JavaScript** (無框架)
- **模板引擎**: Jinja2 3.1.2

### 資料分析（已安裝，未來可用）
- pandas 2.1.3
- numpy 1.26.2
- matplotlib 3.8.2
- seaborn 0.13.0
- plotly 5.18.0

### 部署目標
- **雲端平台**: Zeabur
- **資料庫**: Zeabur PostgreSQL

---

## 📂 專案結構

```
Cat_Canteen_Gas_to_PostgreSQL/
├── app/                          # Python 後端應用
│   ├── __init__.py
│   ├── main.py                   # FastAPI 主程式入口
│   ├── config.py                 # 配置管理（讀取 .env）
│   ├── database.py               # 資料庫連線設定
│   │
│   ├── models/                   # SQLAlchemy 資料模型
│   │   ├── __init__.py
│   │   └── order.py              # 訂單模型
│   │
│   ├── schemas/                  # Pydantic 驗證 schemas
│   │   ├── __init__.py
│   │   └── order.py              # 訂單驗證（對應 GAS 的驗證邏輯）
│   │
│   ├── routers/                  # API 路由
│   │   ├── __init__.py
│   │   ├── orders.py             # 訂單 API（對應 GAS submitOrder）
│   │   └── menu.py               # 選單 API（對應 GAS getMenuData）
│   │
│   ├── services/                 # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── order_service.py      # 訂單服務（對應 OrderService.gs）
│   │   └── menu_service.py       # 選單服務
│   │
│   └── utils/                    # 工具函數
│       ├── __init__.py
│       ├── validation.py         # 輸入驗證、XSS 防護
│       └── order_number.py       # 訂單編號生成（CATyyMMddHHmmss）
│
├── static/                       # 靜態檔案
│   ├── css/
│   │   └── styles.css            # 從 css.html 轉換
│   └── js/
│       └── script.js             # 從 js.html 轉換（fetch API）
│
├── templates/                    # Jinja2 HTML 模板
│   └── index.html                # 從原 index.html 轉換
│
├── scripts/                      # 工具腳本
│   ├── init_db.py                # 資料庫初始化
│   └── migrate_from_sheets.py    # Google Sheets 遷移（未完成）
│
├── venv/                         # Python 虛擬環境
├── cat_canteen.db                # SQLite（已棄用，改用 PostgreSQL）
│
├── requirements.txt              # Python 依賴清單
├── .env                          # 環境變數（PostgreSQL 配置）
├── .env.example                  # 環境變數範本
├── .gitignore                    # Git 忽略規則（Python 專案）
├── README.md                     # 專案說明文件
└── PROJECT_CONTEXT.md            # 本檔案
```

---

## 🗄️ 資料庫結構

### `orders` 資料表

| 欄位 | 型別 | 說明 | 備註 |
|------|------|------|------|
| `id` | Integer | 主鍵 | 自動遞增 |
| `order_number` | String(20) | 訂單編號 | 格式：CAT + YYMMDDHHmmss |
| `customer_name` | String(100) | 顧客姓名 | 必填，已 XSS 清理 |
| `pickup_method` | String(20) | 取餐方式 | 內用 或 外帶 |
| `items` | JSON | 餐點明細 | 儲存餐點陣列 |
| `drinks` | JSON | 飲料明細 | 儲存飲料陣列（含溫度/甜度） |
| `total_amount` | Integer | 總金額 | 已後端驗證 |
| `notes` | Text | 備註 | 可選，已 XSS 清理 |
| `created_at` | DateTime | 建立時間 | 自動設定 |

**索引:**
- `id` (Primary Key)
- `order_number` (Unique Index)
- `created_at` (Index)

---

## 🎯 選單資料

### 主食 (mains)
- `m1`: 貓爪咖哩飯 - NT$ 120
- `m2`: 鮭魚親子丼 - NT$ 150
- `m3`: 喵喵義大利麵 - NT$ 130
- `m4`: 貓掌漢堡排 - NT$ 140

### 湯品 (soups)
- `s1`: 貓咪味噌湯 - NT$ 30
- `s2`: 奶油南瓜濃湯 - NT$ 40
- `s3`: 海鮮巧達湯 - NT$ 50

### 點心 (desserts)
- `d1`: 貓掌布丁 - NT$ 60
- `d2`: 鮮奶雪花冰 - NT$ 70
- `d3`: 焦糖烤布蕾 - NT$ 65
- `d4`: 貓咪銅鑼燒 - NT$ 55

### 飲料 (drinks)
- `dr1`: 貓爪拿鐵 - NT$ 80
- `dr2`: 焦糖瑪奇朵 - NT$ 90
- `dr3`: 抹茶拿鐵 - NT$ 85
- `dr4`: 水果茶 - NT$ 70
- `dr5`: 檸檬冰茶 - NT$ 60

**飲料選項:**
- **溫度**: 正常冰、少冰、微冰、去冰、溫、熱
- **甜度**: 正常糖、少糖、半糖、微糖、無糖

---

## 🔌 API 端點

### 系統端點
- `GET /` - 主頁面（返回 index.html）
- `GET /health` - 健康檢查
- `GET /api` - API 資訊
- `GET /api/docs` - Swagger API 文檔
- `GET /api/redoc` - ReDoc API 文檔

### 選單 API
- `GET /api/menu/` - 取得完整選單
- `GET /api/menu/item/{item_id}` - 取得單一餐點資料

### 訂單 API
- `POST /api/orders/` - 建立訂單
- `GET /api/orders/` - 取得訂單列表
- `GET /api/orders/{order_number}` - 根據訂單編號查詢

---

## ⚙️ 環境配置

### `.env` 檔案（目前配置）

```env
# 應用設定
APP_NAME=Cat Claws 貓咪食堂
APP_VERSION=2.0.0
DEBUG=True

# 資料庫連線（本地 PostgreSQL）
DATABASE_URL=postgresql://your_username@localhost:5432/cat_canteen

# 安全設定
SECRET_KEY=dev-secret-key-for-testing

# CORS 設定
ALLOWED_ORIGINS=["*"]
```

### 本地 PostgreSQL 資訊
- **版本**: PostgreSQL 15+
- **資料庫名稱**: `cat_canteen`
- **使用者**: 您的系統使用者名稱
- **主機**: `localhost`
- **埠號**: `5432`
- **認證**: 依本地 PostgreSQL 設定

### Zeabur 部署時的配置
```env
DATABASE_URL=${POSTGRES_URL}  # Zeabur 自動提供
DEBUG=False
SECRET_KEY=your-production-secret-key  # 需更改
```

---

## 🚀 本地開發指令

### 啟動開發伺服器

```bash
# 1. 啟動虛擬環境
source venv/bin/activate

# 2. 啟動應用
python -m uvicorn app.main:app --reload

# 3. 訪問
# 主頁: http://localhost:8000
# API 文檔: http://localhost:8000/api/docs
```

### PostgreSQL 管理

```bash
# 啟動 PostgreSQL 服務
brew services start postgresql@15

# 停止 PostgreSQL 服務
brew services stop postgresql@15

# 連接到資料庫
/opt/homebrew/opt/postgresql@15/bin/psql -d cat_canteen

# 查看所有訂單
/opt/homebrew/opt/postgresql@15/bin/psql -d cat_canteen -c "SELECT * FROM orders;"

# 清空訂單（小心！）
/opt/homebrew/opt/postgresql@15/bin/psql -d cat_canteen -c "DELETE FROM orders;"
```

### 資料庫初始化

```bash
# 重新建立資料表
source venv/bin/activate
python scripts/init_db.py
```

### 測試 API

```bash
# 健康檢查
curl http://localhost:8000/health

# 取得選單
curl http://localhost:8000/api/menu/

# 建立訂單
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d @test_order.json
```

---

## ✅ 已完成的遷移工作

### 階段 1: 專案結構建立 ✅
- [x] 建立 Python 專案目錄結構
- [x] 建立虛擬環境
- [x] 安裝所有依賴套件
- [x] 建立 `.env` 環境配置

### 階段 2: 後端遷移 ✅
- [x] 建立資料庫模型 (`models/order.py`)
- [x] 建立 Pydantic schemas (`schemas/order.py`)
- [x] 建立服務層 (`services/`)
- [x] 建立 API 路由 (`routers/`)
- [x] 建立工具函數 (`utils/`)
- [x] 建立 FastAPI 主程式 (`main.py`)

### 階段 3: 前端遷移 ✅
- [x] 轉換 `css.html` → `static/css/styles.css`
- [x] 轉換 `js.html` → `static/js/script.js`
  - 將 `google.script.run` 改為 `fetch()` API
- [x] 轉換 `index.html` → `templates/index.html`
  - 使用 Jinja2 模板語法

### 階段 4: 資料庫設定 ✅
- [x] 安裝 PostgreSQL 15
- [x] 建立資料庫 `cat_canteen`
- [x] 建立資料表 `orders`
- [x] 支援 SQLite 和 PostgreSQL 切換

### 階段 5: 清理與文檔 ✅
- [x] 刪除所有 GAS 相關檔案
  - `Code.gs`, `OrderService.gs`
  - `appsscript.json`, `.clasp.json`
  - `deploy.sh`, `deploy-npx.sh`
  - 舊的文檔檔案
- [x] 更新 `.gitignore` 為 Python 專案
- [x] 更新 `README.md`
- [x] 建立專案上下文檔案

### 階段 6: 測試 ✅
- [x] 本地測試（SQLite）
- [x] 本地測試（PostgreSQL）
- [x] API 端點測試
- [x] 前端功能測試
- [x] 訂單建立與查詢測試

---

## 🔐 安全機制

### 1. 輸入驗證
- **Pydantic schemas**: 自動驗證所有輸入資料
- **姓名**: 1-50 字元，自動清理
- **取餐方式**: 限定「內用」或「外帶」
- **餐點 ID**: 白名單驗證
- **數量**: 1-99 之間
- **備註**: 最多 200 字元

### 2. XSS 防護
```python
# utils/validation.py - sanitizeInput()
def sanitize_input(input_str: str) -> str:
    sanitized = input_str.strip()
    sanitized = sanitized.replace('<', '&lt;')
    sanitized = sanitized.replace('>', '&gt;')
    sanitized = sanitized.replace('"', '&quot;')
    sanitized = sanitized.replace("'", '&#x27;')
    sanitized = sanitized.replace('/', '&#x2F;')
    return sanitized
```

### 3. 價格驗證
- 前端計算總金額
- **後端重新驗證**：對照選單價格重新計算
- 防止前端竄改價格

### 4. SQL Injection 防護
- 使用 SQLAlchemy ORM
- 參數化查詢
- 無原生 SQL 字串拼接

### 5. 錯誤處理
- 詳細錯誤記錄（LOG）
- **不暴露敏感資訊**給用戶
- 統一錯誤訊息格式

---

## 📝 GAS → FastAPI 對應關係

| GAS 檔案/函數 | FastAPI 對應檔案/函數 | 說明 |
|--------------|---------------------|------|
| `Code.gs` - `doGet()` | `app/main.py` - `@app.get("/")` | 返回主頁面 |
| `Code.gs` - `getMenuData()` | `app/routers/menu.py` | 選單 API |
| `Code.gs` - `submitOrder()` | `app/routers/orders.py` - `create_order()` | 訂單提交 |
| `Code.gs` - `sanitizeInput()` | `app/utils/validation.py` | XSS 防護 |
| `OrderService.gs` - `generateOrderNumber()` | `app/utils/order_number.py` | 訂單編號生成 |
| `OrderService.gs` - `saveOrder()` | `app/services/order_service.py` | 訂單儲存 |
| `OrderService.gs` - `formatItems()` | `app/services/order_service.py` | 餐點格式化 |
| Google Sheets | PostgreSQL | 資料儲存 |
| `google.script.run` | `fetch()` API | 前端 API 呼叫 |

---

## 🎨 前端保持不變

前端介面**完全保留**原有的可愛設計：
- ✅ 純 CSS 繪製的貓咪頭像
- ✅ 貓咪載入動畫
- ✅ 貓爪按鈕設計
- ✅ 成功貓咪動畫
- ✅ 響應式佈局
- ✅ Toast 提示訊息
- ✅ Modal 彈窗

**唯一改變**: API 呼叫方式從 `google.script.run` 改為 `fetch()`

---

## 🐛 已知問題與解決方案

### 1. WatchFiles 警告
**問題**: Uvicorn 監視 venv 目錄導致不斷重載

**解決方案**:
```bash
# 可忽略，不影響功能
# 或在 .gitignore 加入 venv/
```

### 2. Homebrew 路徑警告
**問題**: `/usr/local/bin/brew: No such file or directory`

**解決方案**:
```bash
# 實際 brew 在 /opt/homebrew/bin/brew
# 可忽略此警告，或修復 .zprofile
```

### 3. email-validator 被 yanked
**問題**: 安裝時顯示 email-validator 2.1.0 被 yanked

**影響**: 無影響（專案未使用 email 驗證功能）

---

## 📊 測試資料

### 測試訂單 (`test_order.json`)
```json
{
  "customerName": "測試用戶",
  "diningOption": "內用",
  "note": "不要香菜",
  "items": [
    {"id": "m1", "name": "貓爪咖哩飯", "quantity": 2, "price": 120},
    {"id": "dr1", "name": "貓爪拿鐵", "quantity": 1, "price": 80}
  ],
  "totalAmount": 320
}
```

### 最新測試訂單（PostgreSQL）
- **訂單編號**: CAT251229235157
- **顧客姓名**: 測試用戶
- **取餐方式**: 內用
- **總金額**: NT$ 320
- **建立時間**: 2025-12-29 23:51:57

---

## 🚀 部署到 Zeabur

### 準備工作
1. 確保 Git repository 乾淨
2. 確認 `.env` 已加入 `.gitignore`
3. 測試本地所有功能正常

### 部署步驟

```bash
# 1. 提交變更
git add .
git commit -m "Ready for Zeabur deployment"
git push origin main

# 2. 在 Zeabur 操作
# - 建立新專案
# - 連接 GitHub Repository
# - 新增 PostgreSQL 服務
# - 設定環境變數:
#   DATABASE_URL=${POSTGRES_URL}
#   DEBUG=False
#   SECRET_KEY=your-production-secret-key

# 3. Zeabur 自動部署
# - 自動偵測 Python 專案
# - 安裝 requirements.txt
# - 啟動 uvicorn
```

### 部署後驗證
- [ ] 訪問主頁
- [ ] 檢查 API 文檔
- [ ] 測試建立訂單
- [ ] 查詢訂單
- [ ] 檢查資料庫資料

---

## 🎯 未來擴充建議

### 短期（1-2週）
- [ ] 部署到 Zeabur
- [ ] 設定自訂網域
- [ ] 建立資料庫備份機制
- [ ] 新增訂單管理後台

### 中期（1個月）
- [ ] 實作資料分析儀表板
  - 每日/每週營收統計
  - 熱門餐點排行
  - 尖峰時段分析
- [ ] 新增會員系統
- [ ] 優惠券功能

### 長期（3個月+）
- [ ] AI 推薦系統
- [ ] LINE Bot 整合
- [ ] 訂單狀態追蹤（製作中/已完成）
- [ ] 多語系支援
- [ ] 行動 App (React Native / Flutter)

---

## 📞 重要提醒

### 給未來 Claude 的提示

1. **專案已完成 GAS → Python 遷移**
   - 所有 `.gs` 檔案已刪除
   - 不要再參考 GAS 相關檔案

2. **本地使用 PostgreSQL**
   - 已安裝 PostgreSQL 15.15
   - 資料庫名稱: `cat_canteen`
   - 使用者: 您的系統使用者名稱
   - 連線不需密碼（Trust）

3. **環境已設定完成**
   - 虛擬環境: `venv/`
   - 所有依賴已安裝
   - `.env` 已配置 PostgreSQL

4. **應用目前狀態**
   - 可正常啟動: `python -m uvicorn app.main:app --reload`
   - 本地測試通過
   - 準備部署到 Zeabur

5. **下一步通常是**
   - 部署到 Zeabur
   - 或新增資料分析功能
   - 或優化前端 UX

### 快速啟動指令

```bash
# 啟動 PostgreSQL
brew services start postgresql@15

# 啟動應用
source venv/bin/activate
python -m uvicorn app.main:app --reload

# 訪問
open http://localhost:8000
```

---

## 📚 相關檔案

- `README.md` - 專案說明（面向所有使用者）
- `PROJECT_CONTEXT.md` - 本檔案（面向 AI/開發者）
- `.env.example` - 環境變數範本
- `requirements.txt` - Python 依賴清單
- `.gitignore` - Git 忽略規則

---

**建立日期**: 2025-12-29
**建立者**: Claude Code
**專案狀態**: ✅ 遷移完成，本地測試通過，準備部署

---

🐾 **Cat Claws 貓咪食堂** - 喵～
