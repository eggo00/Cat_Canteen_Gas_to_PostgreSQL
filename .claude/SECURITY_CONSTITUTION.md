# 🔒 Claude 安全憲章 - 最高指導原則

> **版本**: 1.0.0
> **生效日期**: 2026-01-01
> **適用範圍**: 所有軟體開發專案

---

## 📜 憲章宣言

本憲章為所有 Claude 協助開發工作的**最高指導原則**，任何程式碼操作、Git 提交、部署行為都**必須**遵守本憲章規範。

**違反本憲章的任何操作都應立即中止並警告使用者。**

---

## 🚨 第一條：Git 推送前強制安全檢查

### 原則聲明

在執行任何 `git push`、`git commit` 或程式碼上傳操作前，**必須**完成以下安全檢查。未通過檢查者，**禁止**執行推送。

### 強制檢查清單

#### ✅ 檢查項目 1：.gitignore 完整性

**必須確認**以下敏感檔案類型已被 `.gitignore` 排除：

```gitignore
# 環境變數和機密資料
.env
.env.*
!.env.example
config.json
secrets.json
credentials.json
*.pem
*.key
*.crt

# 資料庫檔案
*.db
*.sqlite
*.sqlite3

# 虛擬環境
venv/
env/
ENV/
.venv

# 日誌
*.log
logs/

# IDE 和編輯器
.vscode/
.idea/
*.swp

# Claude 對話記錄
.claude/
```

**執行指令驗證**：
```bash
git check-ignore .env
git check-ignore venv/
git check-ignore *.db
```

---

#### ✅ 檢查項目 2：敏感檔案掃描

**禁止提交**的檔案模式：

```bash
# 掃描即將提交的檔案
git ls-files | grep -E "\.env$|\.db$|secret|password|credential|\.key$|\.pem$"
```

**如果有任何匹配，立即中止並警告使用者。**

---

#### ✅ 檢查項目 3：配置檔案安全檢查

檢查所有配置檔案（如 `config.py`, `settings.js` 等）：

**❌ 禁止硬編碼**：
- 資料庫密碼
- API 金鑰
- Secret Key
- 第三方服務憑證
- 使用者真實姓名、電話、地址

**✅ 必須使用**：
- 環境變數（`os.getenv()`, `process.env`）
- 明顯的佔位值（`your-secret-key-here`, `user:password@localhost`）

**檢查範例**：
```python
# ❌ 錯誤 - 硬編碼真實密碼
DATABASE_URL = "postgresql://admin:MyRealP@ssw0rd@db.example.com/prod"

# ✅ 正確 - 使用環境變數
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db")

# ✅ 正確 - 明顯的佔位值
SECRET_KEY = "your-secret-key-change-in-production"
```

---

#### ✅ 檢查項目 4：即將提交的檔案審查

**執行指令**：
```bash
# 查看即將提交的所有檔案
git status
git diff --name-only
git diff --cached --name-only

# 查看未追蹤的檔案
git ls-files --others --exclude-standard
```

**人工審查**：
- 每個檔案的用途
- 是否包含測試資料（如果有真實使用者資料，必須移除或匿名化）
- 是否包含臨時偵錯代碼

---

#### ✅ 檢查項目 5：.env.example 檢查

如果專案使用 `.env` 檔案：

**必須提供** `.env.example` 範本檔案，包含：
- 所有必要的環境變數名稱
- 佔位值或範例值（非真實值）
- 清楚的註解說明

**範例**：
```env
# .env.example - 可以提交到 Git

# 資料庫連線（本地開發範例）
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API 金鑰（請向管理員索取）
API_KEY=your-api-key-here

# 安全金鑰（請產生隨機字串）
SECRET_KEY=generate-a-random-secret-key
```

---

## 🛡️ 第二條：部署前安全檢查

### 原則聲明

在部署到任何環境（開發、測試、正式）前，必須完成以下檢查。

### 強制檢查清單

#### ✅ 環境變數設定確認

- [ ] 所有敏感資料都已設定為環境變數
- [ ] 環境變數已在部署平台（Zeabur, Vercel, AWS 等）正確設定
- [ ] DEBUG 模式在正式環境設為 `False` 或 `false`
- [ ] CORS 設定已限制允許的來源（不使用 `["*"]`）

#### ✅ 資料庫安全

- [ ] 資料庫密碼強度足夠（至少 16 字元）
- [ ] 資料庫不允許公開存取
- [ ] 使用 SSL/TLS 加密連線

#### ✅ API 金鑰和憑證

- [ ] 所有 API 金鑰已輪替（不使用開發環境的金鑰）
- [ ] 金鑰權限最小化
- [ ] 啟用金鑰使用監控

---

## 🚫 第三條：禁止行為

以下行為**絕對禁止**，違反者必須立即警告使用者：

### 禁止清單

1. **❌ 提交 .env 檔案到 Git**
   - 即使是 private repository 也禁止

2. **❌ 在程式碼中硬編碼密碼、API 金鑰**
   - 包括註解中的真實憑證

3. **❌ 提交包含真實使用者資料的測試檔案**
   - 必須使用假資料或匿名化

4. **❌ 提交資料庫備份檔案**
   - 如 `.sql`, `.dump`, `.backup`

5. **❌ 提交私鑰檔案**
   - 如 `.pem`, `.key`, SSH keys

6. **❌ 在公開 repository 中存放內部文件**
   - 如包含真實 IP、內部架構圖等

7. **❌ 跳過安全檢查直接 push**
   - 即使「只是測試」或「稍後會改」

---

## ✅ 第四條：推送前標準流程

### 標準作業程序 (SOP)

每次執行 Git 推送時，**必須**按照以下順序執行：

```bash
# 步驟 1: 安全檢查
echo "🔍 執行安全檢查..."

# 1.1 檢查 .gitignore
git check-ignore .env
git check-ignore venv/

# 1.2 掃描敏感檔案
git ls-files | grep -E "\.env$|secret|password|\.key$"

# 1.3 檢查即將提交的檔案
git status
git diff --name-only

# 步驟 2: 確認無誤後才執行
git add .
git commit -m "描述性的提交訊息"

# 步驟 3: 最後檢查
echo "⚠️  即將推送到遠端，請再次確認無敏感資料"

# 步驟 4: 推送
git push origin main
```

### Claude 的責任

在協助使用者 Git 操作時，Claude **必須**：

1. **主動執行**上述安全檢查（不需使用者要求）
2. **明確告知**檢查結果
3. **發現問題時立即中止**，不繼續執行
4. **提供修正建議**
5. **記錄檢查過程**在回應中

---

## 📋 第五條：新專案檢查清單

開始新專案時，**第一件事**就是建立安全基礎設施：

### 專案初始化安全清單

- [ ] 建立 `.gitignore` 檔案（複製本專案的版本）
- [ ] 建立 `.env.example` 範本
- [ ] 建立 `.env` 並加入真實憑證（確認已被 .gitignore）
- [ ] 建立 `SECURITY.md` 說明安全政策
- [ ] 複製 `.claude/` 目錄到新專案
- [ ] 設定 pre-commit hook（可選，自動檢查敏感資料）

### 建議的 pre-commit hook

在專案根目錄建立 `.git/hooks/pre-commit`：

```bash
#!/bin/bash

echo "🔍 執行安全檢查..."

# 檢查是否有敏感檔案
if git diff --cached --name-only | grep -E "\.env$|secret|password|\.key$"; then
    echo "❌ 錯誤：偵測到敏感檔案！"
    echo "請從暫存區移除這些檔案"
    exit 1
fi

# 檢查是否有硬編碼密碼
if git diff --cached | grep -iE "password.*=.*['\"].*['\"]|api_key.*=.*['\"].*['\"]"; then
    echo "⚠️  警告：可能包含硬編碼的密碼或 API 金鑰"
    echo "請確認這些是佔位值而非真實憑證"
    read -p "確定要繼續嗎？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ 安全檢查通過"
exit 0
```

---

## 🎯 第六條：持續監控

### 定期安全審查

每週/每月應執行：

```bash
# 檢查 Git 歷史中是否有敏感資料
git log --all --full-history --source --oneline | grep -i "password\|secret\|key"

# 掃描所有已追蹤的檔案
git ls-tree -r HEAD --name-only | grep -E "\.env$|secret|password"

# 檢查大型檔案（可能是誤提交的備份）
git rev-list --all --objects | \
  git cat-file --batch-check='%(objectsize:disk) %(objectname) %(rest)' | \
  sort -nr | head -20
```

### 緊急處理程序

如果**已經提交**敏感資料到 Git：

1. **立即**輪替所有暴露的憑證
2. 使用 `git filter-branch` 或 `BFG Repo-Cleaner` 清除歷史
3. Force push 覆蓋遠端歷史
4. 通知所有協作者重新 clone repository
5. 記錄事件並檢討預防措施

---

## 📖 第七條：團隊協作規範

### Code Review 要求

所有 Pull Request **必須**包含：

- [ ] 安全檢查確認聲明
- [ ] `.env.example` 已更新（如有新增環境變數）
- [ ] 無硬編碼憑證
- [ ] 測試資料已匿名化

### 文檔要求

每個專案必須包含：

- `README.md` - 專案說明和設定指引
- `SECURITY.md` - 安全政策和漏洞回報方式
- `.env.example` - 環境變數範本
- `CONTRIBUTING.md` - 貢獻指南（包含安全規範）

---

## 🔄 憲章更新

本憲章應隨著最佳實踐演進而更新。建議更新時機：

- 發現新的安全風險
- 採用新的開發工具或平台
- 發生安全事件後的檢討
- 至少每季度審查一次

---

## ✍️ 憲章簽署

**專案**: Cat Canteen - 貓咪食堂點餐系統
**建立日期**: 2026-01-01
**最後更新**: 2026-01-01
**版本**: 1.0.0

---

**本憲章為最高指導原則，所有開發工作必須遵守。**

**記住：安全不是選項，而是必須。**

🔒 **Security First, Always.**
