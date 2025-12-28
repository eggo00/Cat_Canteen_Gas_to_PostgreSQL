# 🐾 Cat Claws 貓咪食堂

一個可愛的貓咪主題網頁訂餐系統，使用 Google Apps Script 建立。

## ✨ 功能特色

### 🎨 視覺設計
- 溫暖可愛的貓咪卡通風格
- 奶茶色/淺咖啡/米白/淡橘色系
- 貓爪按鈕與圓角卡片設計
- 可愛的 CSS 貓咪動畫

### 🍽 訂餐功能
- **主食**：貓爪咖哩飯、鮭魚親子丼、喵喵義大利麵、貓掌漢堡排
- **湯品**：貓咪味噌湯、奶油南瓜濃湯、海鮮巧達湯
- **點心**：貓掌布丁、鮮奶雪花冰、焦糖烤布蕾、貓咪銅鑼燒
- **飲料**：可選擇冰熱、甜度

### 📝 訂單管理
- 即時購物車功能
- 自動計算總金額
- 訂單資料自動儲存到 Google Sheets
- 成功提示動畫

## 📁 專案結構

```
Gas_Cat_Canteen/
├── appsscript.json      # GAS 專案配置
├── Code.gs              # 主要後端邏輯
├── OrderService.gs      # 訂單處理服務
├── index.html           # 主頁面 HTML
├── css.html             # 樣式表
├── js.html              # JavaScript 邏輯
├── DEPLOYMENT.md        # 部署指南
├── README.md            # 專案說明
└── .gitignore           # Git 忽略檔案
```

## 🚀 快速開始

### 1. 安裝 CLASP

```bash
npm install -g @google/clasp
```

### 2. 登入並啟用 API

```bash
clasp login
```

前往 https://script.google.com/home/usersettings 啟用 Apps Script API

### 3. 建立專案並部署

```bash
cd Gas_Cat_Canteen
clasp create --type webapp --title "貓咪食堂訂餐系統"
clasp push
clasp deploy
```

詳細部署步驟請參考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🎯 使用說明

### 顧客端
1. 開啟 Web App URL
2. 瀏覽選單並選擇喜歡的餐點
3. 調整數量，飲料可選擇冰熱和甜度
4. 點選「加入訂單」
5. 填寫姓名、選擇內用/外帶
6. 送出訂單

### 管理端
訂單會自動儲存到 Google Sheets，包含：
- 時間戳記
- 訂單編號
- 顧客姓名
- 取餐方式
- 餐點明細
- 飲料明細
- 總金額
- 備註

## 🛠 技術棧

- **後端**：Google Apps Script
- **前端**：HTML5 + CSS3 + Vanilla JavaScript
- **資料庫**：Google Sheets
- **開發工具**：CLASP

## 🎨 設計特色

### 貓咪元素
- 純 CSS 繪製的貓咪頭像
- 貓爪按鈕設計
- 載入動畫貓咪
- 成功提示貓咪表情

### 互動效果
- 卡片 hover 動畫
- 按鈕點擊回饋
- Toast 通知訊息
- Modal 彈窗

### 響應式設計
- 支援桌面與行動裝置
- 自適應網格佈局

## 📊 資料格式

### 訂單資料結構

```javascript
{
  customerName: "王小明",
  diningOption: "內用",
  note: "不要加蔥",
  items: [
    {
      id: "m1",
      name: "貓爪咖哩飯",
      price: 120,
      quantity: 2
    },
    {
      id: "dr1",
      name: "貓爪拿鐵",
      price: 80,
      quantity: 1,
      temperature: "熱",
      sweetness: "半糖"
    }
  ],
  totalAmount: 320
}
```

## 🔧 客製化

### 修改選單

編輯 `Code.gs` 中的 `getMenuData()` 函數：

```javascript
function getMenuData() {
  return {
    mains: [
      { id: 'm1', name: '您的餐點名稱', price: 價格 }
    ],
    // ...
  };
}
```

### 修改顏色

編輯 `css.html` 中的顏色變數：

```css
/* 主色調 */
#F4A460  /* 淺咖啡色 */
#FFE4C4  /* 米白色 */
#5D4037  /* 深咖啡色 */
```

### 修改試算表名稱

編輯 `OrderService.gs` 中的：

```javascript
var SHEET_NAME = '貓咪食堂訂單';
```

## 📝 授權

此專案為教學用途，可自由使用與修改。

## 🐱 作者

使用 Claude Code 與 Google Apps Script 打造的可愛訂餐系統

---

**喵～ 歡迎來到貓咪食堂！🐾**
