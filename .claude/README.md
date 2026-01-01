# .claude 目錄說明

## 📂 目錄用途

此目錄包含 Claude AI 協助開發時應遵守的最高指導原則和專案文檔。

## 📋 檔案清單

### `SECURITY_CONSTITUTION.md`
**安全憲章 - 最高指導原則**

這是所有 Claude 開發協作的**最高準則**，任何程式碼操作都必須遵守此憲章。

**主要內容**：
- Git 推送前強制安全檢查
- 部署前安全檢查
- 禁止行為清單
- 標準作業流程
- 新專案檢查清單

## 🚀 如何在新專案中使用

### 方法一：複製整個 .claude 目錄

```bash
# 在新專案根目錄執行
cp -r /path/to/old-project/.claude .
```

### 方法二：作為範本庫

1. 建立一個範本 repository
2. 將此 `.claude` 目錄放入範本
3. 每次建立新專案時從範本 clone

### 方法三：全域配置（進階）

```bash
# 建立全域 Claude 配置目錄
mkdir -p ~/.claude/templates

# 複製憲章
cp .claude/SECURITY_CONSTITUTION.md ~/.claude/templates/

# 在新專案中建立符號連結
ln -s ~/.claude/templates .claude
```

## 📖 使用指南

### 給 Claude 的提示

當開始新對話時，可以告訴 Claude：

> "請遵守 `.claude/SECURITY_CONSTITUTION.md` 中的所有安全準則"

或

> "執行任何 Git 操作前，請先參考專案中的安全憲章"

### 給開發者的建議

1. **定期審查憲章**：至少每季度檢視一次，確保符合最新最佳實踐
2. **團隊共識**：確保所有團隊成員都理解並同意遵守憲章
3. **持續改進**：遇到新的安全議題時，更新憲章內容

## 🔒 為什麼 .claude 被 gitignore？

`.claude/` 目錄**預設被 gitignore**，因為：

1. **對話歷史可能包含敏感資訊**（如討論過的密碼、架構細節）
2. **專案規劃可能包含商業機密**
3. **個人筆記不應該上傳到公開 repository**

但 `SECURITY_CONSTITUTION.md` **應該提交到 Git**，因為它是團隊共享的安全準則。

### 建議做法

修改 `.gitignore`：

```gitignore
# Claude 對話記錄和私人筆記
.claude/
# 但允許安全憲章
!.claude/SECURITY_CONSTITUTION.md
!.claude/README.md
```

或者，如果整個團隊都使用 Claude，可以將整個 `.claude/` 目錄納入版本控制。

## 📝 自訂憲章

您可以根據專案需求自訂憲章內容：

1. 開啟 `SECURITY_CONSTITUTION.md`
2. 新增專案特定的安全要求
3. 調整檢查清單以符合團隊工作流程
4. 更新版本號和日期

## 🤝 團隊協作

如果團隊成員都使用 Claude Code 或類似 AI 工具：

1. **共享此憲章**：確保所有 AI 助手都遵守相同規範
2. **Code Review 時驗證**：檢查是否確實遵守憲章
3. **定期培訓**：確保新成員理解安全準則的重要性

## 🆘 遇到問題？

如果 Claude 未遵守憲章或您發現安全漏洞：

1. 立即停止操作
2. 檢查憲章是否需要更新
3. 回報給團隊負責人
4. 必要時更新憲章並通知所有成員

---

**記住**：安全是每個人的責任，憲章只是工具，最終還是要靠團隊的警覺性和執行力。

🔒 **Stay Secure!**
