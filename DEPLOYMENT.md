# 🐾 Cat Claws 貓咪食堂 - 部署指南

## 📋 前置需求

1. **安裝 Node.js**
   - 下載並安裝 Node.js（建議 v14 以上）
   - 官網：https://nodejs.org/

2. **Google 帳號**
   - 需要有 Google 帳號來使用 Google Apps Script

## 🚀 部署步驟

### 步驟 1：安裝 CLASP

```bash
npm install -g @google/clasp
```

### 步驟 2：登入 Google 帳號

```bash
clasp login
```

這會開啟瀏覽器，請選擇您的 Google 帳號並授權 CLASP。

### 步驟 3：啟用 Apps Script API

1. 前往：https://script.google.com/home/usersettings
2. 將「Google Apps Script API」設定為「開啟」

### 步驟 4：建立新的 GAS 專案

在專案目錄中執行：

```bash
cd Gas_Cat_Canteen
clasp create --type webapp --title "貓咪食堂訂餐系統"
```

這會建立一個新的 Google Apps Script 專案，並產生 `.clasp.json` 檔案。

### 步驟 5：上傳程式碼到 GAS

```bash
clasp push
```

確認是否要覆蓋雲端檔案，輸入 `Y` 或 `yes`。

### 步驟 6：部署為 Web App

#### 方法 1：使用命令列（推薦）

```bash
# 開啟專案
clasp open

# 或使用部署命令
clasp deploy --description "貓咪食堂 v1.0"
```

#### 方法 2：在 Apps Script 介面部署

1. 執行 `clasp open` 開啟 Google Apps Script 編輯器
2. 點選右上角「部署」→「新增部署作業」
3. 選擇類型：「網頁應用程式」
4. 設定：
   - **說明**：貓咪食堂訂餐系統
   - **執行身分**：我
   - **具有存取權的使用者**：任何人
5. 點選「部署」
6. 複製「網頁應用程式 URL」

### 步驟 7：測試網頁

1. 開啟部署後的 URL
2. 測試以下功能：
   - 選擇餐點並加入訂單
   - 填寫姓名和取餐方式
   - 送出訂單
   - 檢查是否成功顯示「喵～訂單已送出！」

### 步驟 8：檢查 Google Sheets

1. 在 Apps Script 編輯器中，查看執行記錄（Logger）
2. 找到自動建立的「貓咪食堂訂單記錄」試算表
3. 確認訂單資料已正確寫入

## 🔄 更新程式碼

當您修改程式碼後，重新部署：

```bash
# 推送更新
clasp push

# 建立新版本部署
clasp deploy --description "v1.1 - 修復問題"
```

## 📝 常用 CLASP 指令

| 指令 | 說明 |
|------|------|
| `clasp login` | 登入 Google 帳號 |
| `clasp logout` | 登出 |
| `clasp create` | 建立新專案 |
| `clasp push` | 上傳本地檔案到雲端 |
| `clasp pull` | 下載雲端檔案到本地 |
| `clasp open` | 在瀏覽器開啟專案 |
| `clasp deploy` | 部署新版本 |
| `clasp deployments` | 查看所有部署版本 |
| `clasp logs` | 查看執行記錄 |

## ⚠️ 常見問題

### 問題 1：`clasp: command not found`
**解決方式**：確認 Node.js 和 npm 已正確安裝，並重新執行 `npm install -g @google/clasp`

### 問題 2：推送時出現權限錯誤
**解決方式**：
1. 確認已執行 `clasp login`
2. 前往 https://script.google.com/home/usersettings
3. 確認「Google Apps Script API」已開啟

### 問題 3：網頁顯示「此應用程式尚未經過 Google 驗證」
**解決方式**：
1. 點選「進階」
2. 點選「前往『專案名稱』（不安全）」
3. 這是因為是個人開發的應用程式，可以安全使用

### 問題 4：訂單沒有寫入 Google Sheets
**解決方式**：
1. 檢查 Apps Script 執行記錄：`clasp logs`
2. 確認部署時選擇「執行身分：我」
3. 授予必要的 Google Sheets 權限

## 📌 重要提醒

1. **第一次執行時**，Google 會要求授權存取 Google Sheets
2. **Web App URL** 會在每次新部署時改變，除非您使用「管理部署作業」來更新現有部署
3. 建議將 `.clasp.json` 加入 `.gitignore`（如果使用 Git）

## 🎉 完成！

您的貓咪食堂訂餐系統已成功部署！

可以分享 Web App URL 給使用者，讓他們開始訂餐了～ 🐾
