# 🐾 貓咪食堂 - 一步一步部署指南

## 📌 請在你的終端機（Terminal）中依序執行以下命令

---

## 步驟 1️⃣：安裝 CLASP

**複製並執行以下命令：**

```bash
sudo npm install -g @google/clasp
```

- 會要求輸入你的 Mac 密碼（輸入時不會顯示，正常現象）
- 輸入密碼後按 Enter
- 等待安裝完成（約 10-30 秒）

**✅ 看到類似以下訊息就成功了：**
```
+ @google/clasp@2.x.x
added XX packages in XXs
```

---

## 步驟 2️⃣：確認 CLASP 安裝成功

**執行：**

```bash
clasp --version
```

**✅ 應該會顯示版本號，例如：**
```
2.4.2
```

---

## 步驟 3️⃣：登入 Google 帳號

**執行：**

```bash
clasp login
```

**會發生什麼：**
- 會自動開啟瀏覽器
- 顯示 Google 登入畫面
- 選擇你的 Google 帳號
- 點選「允許」授權 CLASP

**✅ 終端機會顯示：**
```
Authorization successful.
Logged in as: your-email@gmail.com
```

---

## 步驟 4️⃣：啟用 Google Apps Script API

**在瀏覽器中打開：**

```
https://script.google.com/home/usersettings
```

**操作：**
- 找到「Google Apps Script API」
- 確認切換開關是「開啟」狀態（藍色）

**✅ 看到「已啟用」就完成了**

---

## 步驟 5️⃣：切換到專案目錄

**執行：**

```bash
cd /Users/fanny/Desktop/Vibe_coding_camp/Gas_Cat_Canteen
```

**確認位置：**

```bash
pwd
```

**✅ 應該顯示：**
```
/Users/fanny/Desktop/Vibe_coding_camp/Gas_Cat_Canteen
```

---

## 步驟 6️⃣：建立 Google Apps Script 專案

**執行：**

```bash
clasp create --type webapp --title "貓咪食堂訂餐系統"
```

**會詢問是否建立新試算表，輸入：**
```
standalone
```

**✅ 成功會顯示：**
```
Created new Google Apps Script project.
https://script.google.com/d/YOUR_SCRIPT_ID/edit
```

---

## 步驟 7️⃣：上傳程式碼到 Google Apps Script

**執行：**

```bash
clasp push
```

**如果詢問是否覆蓋 manifest，輸入：**
```
y
```

**✅ 成功會顯示：**
```
└─ appsscript.json
└─ Code.gs
└─ OrderService.gs
└─ index.html
└─ css.html
└─ js.html
Pushed 6 files.
```

---

## 步驟 8️⃣：開啟 Apps Script 編輯器

**執行：**

```bash
clasp open
```

**會自動在瀏覽器開啟 Google Apps Script 編輯器**

---

## 步驟 9️⃣：部署為 Web App

**在開啟的 Apps Script 編輯器中：**

1. 點選右上角「**部署**」按鈕
2. 選擇「**新增部署作業**」
3. 點選左側齒輪圖示「**選取類型**」
4. 選擇「**網頁應用程式**」
5. 填寫設定：
   - **說明**：`貓咪食堂 v1.0`
   - **執行身分**：選擇「**我**」
   - **具有存取權的使用者**：選擇「**任何人**」
6. 點選「**部署**」
7. 可能會要求授權，點選「**授權存取權**」
8. 選擇你的 Google 帳號
9. 點選「**進階**」→「**前往『貓咪食堂訂餐系統』（不安全）**」
10. 點選「**允許**」

**✅ 成功後會顯示部署視窗，包含：**
- 部署 ID
- **網頁應用程式 URL** ← 這個就是你的網站網址！

---

## 步驟 🔟：測試網站

**複製上一步的「網頁應用程式 URL」，在瀏覽器中開啟**

**測試功能：**
1. 選擇幾個餐點，點選「🐾 加入訂單」
2. 填寫姓名（例如：測試使用者）
3. 選擇「內用」或「外帶」
4. 點選「🐾 送出訂單」

**✅ 應該會看到：**
```
😺 喵～訂單已送出！
您的訂單編號：CAT251227xxxxxx
```

---

## 步驟 1️⃣1️⃣：檢查訂單記錄

**在 Apps Script 編輯器中：**

1. 點選左側選單「**執行作業**」
2. 查看「**執行紀錄**」
3. 找到記錄中提到的 Google Sheets 網址
4. 開啟試算表

**✅ 應該會看到「貓咪食堂訂單」工作表，裡面有你剛才的測試訂單**

---

## 🎉 完成！

恭喜你成功部署了貓咪食堂訂餐系統！

### 📋 接下來可以做什麼？

1. **分享網站**：將 Web App URL 分享給使用者
2. **查看訂單**：隨時在 Google Sheets 查看所有訂單
3. **修改程式碼**：
   - 編輯本地的 `.gs` 或 `.html` 檔案
   - 執行 `clasp push` 上傳更新
   - 重新整理網頁即可看到變更

---

## ⚠️ 如果遇到問題

### ❌ CLASP 安裝失敗
**解決方式：**
```bash
# 清除 npm cache
npm cache clean --force

# 重新安裝
sudo npm install -g @google/clasp
```

### ❌ `User has not enabled the Apps Script API`
**解決方式：**
- 前往 https://script.google.com/home/usersettings
- 確認「Google Apps Script API」已開啟

### ❌ 網頁顯示錯誤
**解決方式：**
1. 確認所有檔案都已上傳：`clasp push`
2. 查看執行紀錄是否有錯誤訊息
3. 重新部署：在 Apps Script 中「管理部署作業」→「編輯」→「部署」

### ❌ 訂單沒有寫入 Google Sheets
**解決方式：**
1. 確認部署時選擇了「執行身分：我」
2. 檢查是否已授權存取 Google Sheets
3. 查看 Apps Script 執行紀錄的錯誤訊息

---

## 📞 需要更多幫助？

- 查看詳細文件：`DEPLOYMENT.md`
- 專案說明：`README.md`
- Apps Script 執行紀錄：在編輯器中查看錯誤訊息

**喵～ 祝你使用順利！🐾**
