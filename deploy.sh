#!/bin/bash

# ====================================
# 🐾 貓咪食堂部署腳本
# ====================================

echo "🐱 歡迎使用貓咪食堂部署腳本！"
echo ""

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 步驟 1: 檢查 Node.js
echo -e "${YELLOW}📌 步驟 1: 檢查 Node.js 安裝...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未安裝 Node.js${NC}"
    echo "請先安裝 Node.js: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✅ Node.js 版本: $(node -v)${NC}"
echo ""

# 步驟 2: 檢查 npm
echo -e "${YELLOW}📌 步驟 2: 檢查 npm 安裝...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ 未安裝 npm${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm 版本: $(npm -v)${NC}"
echo ""

# 步驟 3: 安裝 CLASP
echo -e "${YELLOW}📌 步驟 3: 安裝 CLASP...${NC}"
if ! command -v clasp &> /dev/null; then
    echo "正在安裝 CLASP..."
    sudo npm install -g @google/clasp
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ CLASP 安裝成功${NC}"
    else
        echo -e "${RED}❌ CLASP 安裝失敗${NC}"
        echo "請手動執行: sudo npm install -g @google/clasp"
        exit 1
    fi
else
    echo -e "${GREEN}✅ CLASP 已安裝${NC}"
fi
echo ""

# 步驟 4: 登入 Google
echo -e "${YELLOW}📌 步驟 4: 登入 Google 帳號...${NC}"
echo "這會開啟瀏覽器，請授權 CLASP 存取您的 Google 帳號"
read -p "按 Enter 繼續..."
clasp login
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 登入成功${NC}"
else
    echo -e "${RED}❌ 登入失敗${NC}"
    exit 1
fi
echo ""

# 步驟 5: 提醒啟用 API
echo -e "${YELLOW}📌 步驟 5: 啟用 Google Apps Script API${NC}"
echo "請前往以下網址，確認「Google Apps Script API」已開啟："
echo "https://script.google.com/home/usersettings"
read -p "確認已啟用後，按 Enter 繼續..."
echo ""

# 步驟 6: 建立專案
echo -e "${YELLOW}📌 步驟 6: 建立 Google Apps Script 專案...${NC}"
if [ -f ".clasp.json" ]; then
    echo -e "${YELLOW}⚠️  .clasp.json 已存在，跳過建立專案${NC}"
else
    clasp create --type webapp --title "貓咪食堂訂餐系統"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 專案建立成功${NC}"
    else
        echo -e "${RED}❌ 專案建立失敗${NC}"
        exit 1
    fi
fi
echo ""

# 步驟 7: 推送代碼
echo -e "${YELLOW}📌 步驟 7: 推送代碼到 Google Apps Script...${NC}"
clasp push
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 代碼推送成功${NC}"
else
    echo -e "${RED}❌ 代碼推送失敗${NC}"
    exit 1
fi
echo ""

# 步驟 8: 部署
echo -e "${YELLOW}📌 步驟 8: 部署為 Web App...${NC}"
echo "即將開啟 Apps Script 編輯器"
echo "請在編輯器中："
echo "1. 點選「部署」→「新增部署作業」"
echo "2. 選擇類型：「網頁應用程式」"
echo "3. 設定執行身分：「我」"
echo "4. 具有存取權的使用者：「任何人」"
echo "5. 點選「部署」"
echo "6. 複製「網頁應用程式 URL」"
read -p "按 Enter 開啟編輯器..."
clasp open
echo ""

# 完成
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}🎉 部署流程完成！${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo "📝 下一步："
echo "1. 在開啟的瀏覽器中完成部署"
echo "2. 複製 Web App URL"
echo "3. 開啟 URL 測試網站功能"
echo "4. 檢查訂單是否正確儲存到 Google Sheets"
echo ""
echo -e "${GREEN}喵～ 祝您使用愉快！🐾${NC}"
