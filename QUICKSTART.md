# 🚀 快速啟動指南

## 方法一：使用自動化腳本（推薦）

在終端機執行：

```bash
cd /Users/fanny/Desktop/Vibe_coding_camp/Gas_Cat_Canteen
./deploy.sh
```

腳本會自動幫你完成所有步驟！

---

## 方法二：手動執行（逐步操作）

### 1️⃣ 安裝 CLASP

```bash
sudo npm install -g @google/clasp
```

輸入你的 Mac 密碼後等待安裝完成。

### 2️⃣ 登入 Google

```bash
clasp login
```

- 會開啟瀏覽器
- 選擇你的 Google 帳號
- 點選「允許」授權

### 3️⃣ 啟用 API

前往：https://script.google.com/home/usersettings

將「Google Apps Script API」設定為「開啟」

### 4️⃣ 切換到專案目錄

```bash
cd /Users/fanny/Desktop/Vibe_coding_camp/Gas_Cat_Canteen
```

### 5️⃣ 建立 GAS 專案

```bash
clasp create --type webapp --title "貓咪食堂訂餐系統"
```

看到 `Created new Google Sheet...` 就成功了！

### 6️⃣ 推送代碼

```bash
clasp push
```

如果詢問是否覆蓋，輸入 `y` 或 `yes`

### 7️⃣ 部署 Web App

#### 選項 A：使用命令（簡單）

```bash
clasp open
```

然後在開啟的 Apps Script 編輯器中：

1. 點選右上角「部署」→「新增部署作業」
2. 點選「選取類型」→「網頁應用程式」
3. 設定：
   - **執行身分**：我
   - **具有存取權的使用者**：任何人
4. 點選「部署」
5. 複製「網頁應用程式 URL」

#### 選項 B：使用部署命令（進階）

```bash
clasp deploy --description "貓咪食堂 v1.0"
```

然後執行：

```bash
clasp deployments
```

找到最新的部署 ID，然後：

```bash
clasp open --deploymentId <YOUR_DEPLOYMENT_ID>
```

### 8️⃣ 測試網站

1. 開啟複製的 Web App URL
2. 選擇一些餐點加入訂單
3. 填寫姓名、選擇內用或外帶
4. 點選「送出訂單」
5. 看到「喵～訂單已送出！」就成功了！

### 9️⃣ 檢查訂單記錄

在 Apps Script 編輯器中：

1. 點選「執行作業」→「執行紀錄」
2. 找到自動建立的「貓咪食堂訂單記錄」試算表連結
3. 打開試算表，確認訂單已儲存

---

## ⚠️ 常見問題

### Q: `clasp: command not found`

A: CLASP 尚未安裝或安裝失敗，請重新執行：
```bash
sudo npm install -g @google/clasp
```

### Q: `User has not enabled the Apps Script API`

A: 請前往 https://script.google.com/home/usersettings 啟用 API

### Q: `Permission denied`

A: 腳本沒有執行權限，執行：
```bash
chmod +x deploy.sh
```

### Q: 部署後網頁顯示錯誤

A:
1. 確認所有檔案都已正確上傳（`clasp push`）
2. 檢查 Apps Script 執行紀錄是否有錯誤
3. 確認部署時選擇了「執行身分：我」

### Q: 訂單沒有寫入 Google Sheets

A:
1. 第一次執行需要授權存取 Google Sheets
2. 查看 Apps Script 執行紀錄的錯誤訊息
3. 重新部署並確認權限

---

## 📞 需要幫助？

如果遇到問題：

1. 查看 `DEPLOYMENT.md` 的詳細說明
2. 檢查 Apps Script 的執行紀錄
3. 確認所有步驟都按順序完成

---

## 🎉 完成！

部署成功後，你可以：

- 分享 Web App URL 給使用者
- 在 Google Sheets 查看所有訂單
- 修改程式碼後執行 `clasp push` 更新

**喵～ 開始使用貓咪食堂吧！🐾**
