# Zeabur 部署指南

## 📦 部署步驟

### 1. 推送程式碼到 GitHub

```bash
git add .
git commit -m "feat: 準備部署到 Zeabur"
git push origin main
```

### 2. 登入 Zeabur

前往 [Zeabur](https://zeabur.com) 並使用 GitHub 帳號登入。

### 3. 建立新專案

1. 點擊 **Create New Project**
2. 選擇專案名稱（例如：`cat-canteen`）
3. 選擇部署區域（建議：Taiwan 或 Singapore）

### 4. 新增 PostgreSQL 服務

1. 在專案中點擊 **Add Service**
2. 選擇 **Prebuilt Service**
3. 選擇 **PostgreSQL**
4. Zeabur 會自動建立 PostgreSQL 資料庫

### 5. 部署 FastAPI 應用

1. 在專案中點擊 **Add Service**
2. 選擇 **Git Repository**
3. 選擇您的 GitHub repository: `Cat_Canteen_Gas_to_PostgreSQL`
4. Zeabur 會自動偵測到 Python/FastAPI 專案並開始部署

### 6. 設定環境變數

在 FastAPI 服務的設定頁面中，新增以下環境變數：

#### 必要變數：

```env
DATABASE_URL=${POSTGRES_URL}
```

> **重要**：`${POSTGRES_URL}` 是 Zeabur 自動提供的變數引用，會自動連接到您的 PostgreSQL 服務。

#### 可選變數：

```env
APP_NAME=Cat Claws 貓咪食堂
APP_VERSION=2.0.0
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_ORIGINS=["*"]
```

> **安全提示**：請將 `SECRET_KEY` 改為一個隨機的長字串。

### 7. 設定網域

1. 在服務設定中找到 **Domain** 區域
2. Zeabur 會自動提供一個 `.zeabur.app` 網域
3. 也可以綁定自己的網域

### 8. 等待部署完成

- Zeabur 會自動安裝依賴 (`pip install -r requirements.txt`)
- 自動執行資料庫遷移（透過 `Base.metadata.create_all()`）
- 啟動 FastAPI 應用

部署完成後，您的應用會在提供的網域上運行！

## 🔍 部署後檢查

### 訪問應用

- **首頁**：`https://your-app.zeabur.app/`
- **API 文件**：`https://your-app.zeabur.app/api/docs`
- **分析報表**：`https://your-app.zeabur.app/analytics`

### 查看日誌

在 Zeabur 控制台中：
1. 點擊您的服務
2. 切換到 **Logs** 分頁
3. 可以即時查看應用日誌

## 🔧 常見問題

### Q: 資料庫連線失敗

**A**: 確認環境變數 `DATABASE_URL` 設定為 `${POSTGRES_URL}`（包含大括號）

### Q: 靜態檔案無法載入

**A**: Zeabur 會自動處理靜態檔案，確認 `static/` 資料夾已推送到 Git。

### Q: 如何更新部署？

**A**: 只需要推送新的程式碼到 GitHub：
```bash
git add .
git commit -m "更新功能"
git push
```
Zeabur 會自動重新部署。

## 📊 監控與維護

### 查看服務狀態

在 Zeabur 控制台可以看到：
- CPU 使用率
- 記憶體使用量
- 網路流量
- 回應時間

### 擴展服務

如果流量增加，可以在 Zeabur 控制台調整：
- 增加實例數量（水平擴展）
- 升級方案（垂直擴展）

## 🎉 完成！

您的 Cat Claws 貓咪食堂現在已經在雲端運行了！

---

如有任何問題，請參考：
- [Zeabur 官方文件](https://zeabur.com/docs)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
