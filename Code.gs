/**
 * Cat Claws 貓咪食堂 - 主要後端程式
 * 處理 Web App 的 HTTP 請求
 */

/**
 * doGet() - 處理 GET 請求，回傳 HTML 頁面
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('🐾 Cat Claws 貓咪食堂')
    .setFaviconUrl('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/350/cat-face_1f431.png')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * include() - 引入其他 HTML 檔案（CSS、JS）
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * submitOrder() - 接收前端訂單資料並儲存
 * @param {Object} orderData - 訂單資料物件
 * @returns {Object} 回傳結果
 */
function submitOrder(orderData) {
  try {
    // 除錯：記錄收到的資料
    Logger.log('收到訂單資料: ' + JSON.stringify(orderData));

    // === 輸入驗證 ===

    // 1. 檢查資料是否存在
    if (!orderData || typeof orderData !== 'object') {
      return {
        success: false,
        message: '訂單資料格式錯誤'
      };
    }

    // 2. 驗證姓名（必填，長度限制）
    if (!orderData.customerName || typeof orderData.customerName !== 'string') {
      return {
        success: false,
        message: '請輸入姓名'
      };
    }
    if (orderData.customerName.length > 50) {
      return {
        success: false,
        message: '姓名長度不可超過 50 字元'
      };
    }

    // 3. 驗證取餐方式
    var validDiningOptions = ['內用', '外帶'];
    if (!validDiningOptions.includes(orderData.diningOption)) {
      return {
        success: false,
        message: '取餐方式錯誤'
      };
    }

    // 4. 驗證餐點項目
    if (!Array.isArray(orderData.items) || orderData.items.length === 0) {
      return {
        success: false,
        message: '請至少選擇一項餐點'
      };
    }
    if (orderData.items.length > 50) {
      return {
        success: false,
        message: '單次訂單不可超過 50 項餐點'
      };
    }

    // 5. 驗證每個餐點項目
    var validItemIds = ['m1', 'm2', 'm3', 'm4', 's1', 's2', 's3', 'd1', 'd2', 'd3', 'd4', 'dr1', 'dr2', 'dr3', 'dr4', 'dr5'];
    var calculatedTotal = 0;

    for (var i = 0; i < orderData.items.length; i++) {
      var item = orderData.items[i];

      // 驗證餐點 ID
      if (!validItemIds.includes(item.id)) {
        return {
          success: false,
          message: '包含無效的餐點項目'
        };
      }

      // 驗證數量
      if (!item.quantity || item.quantity < 1 || item.quantity > 99) {
        return {
          success: false,
          message: '餐點數量必須在 1-99 之間'
        };
      }

      // 驗證價格（對照正確價格）
      var menuItem = getMenuItemById(item.id);
      if (!menuItem || item.price !== menuItem.price) {
        return {
          success: false,
          message: '餐點價格不符'
        };
      }

      calculatedTotal += item.price * item.quantity;
    }

    // 6. 驗證總金額
    if (orderData.totalAmount !== calculatedTotal) {
      return {
        success: false,
        message: '訂單金額計算錯誤'
      };
    }

    // 7. 驗證備註長度
    if (orderData.note && orderData.note.length > 200) {
      return {
        success: false,
        message: '備註長度不可超過 200 字元'
      };
    }

    // 8. 清理輸入（防止 XSS）
    orderData.customerName = sanitizeInput(orderData.customerName);
    orderData.note = sanitizeInput(orderData.note || '');

    // === 驗證通過，儲存訂單 ===
    var result = OrderService.saveOrder(orderData);

    return {
      success: true,
      message: '喵～訂單已送出！',
      orderNumber: result.orderNumber
    };

  } catch (error) {
    // 詳細的錯誤日誌（含上下文）
    logError('submitOrder', error, {
      customerName: orderData ? orderData.customerName : 'unknown',
      itemCount: orderData && orderData.items ? orderData.items.length : 0,
      totalAmount: orderData ? orderData.totalAmount : 0
    });

    // 嚴重錯誤通知（可選）
    if (isServerError(error)) {
      notifyAdmin('訂單系統發生嚴重錯誤', error);
    }

    // 不要暴露詳細錯誤給用戶
    return {
      success: false,
      message: '系統錯誤，請稍後再試'
    };
  }
}

/**
 * 記錄錯誤（含完整上下文）
 */
function logError(functionName, error, context) {
  var timestamp = new Date().toISOString();
  var logEntry = {
    timestamp: timestamp,
    function: functionName,
    error: error.toString(),
    stack: error.stack,
    context: context
  };

  Logger.log('=== 錯誤記錄 ===');
  Logger.log(JSON.stringify(logEntry, null, 2));

  // 選擇性：寫入錯誤日誌試算表
  // writeErrorLog(logEntry);
}

/**
 * 判斷是否為伺服器錯誤（需要立即關注）
 */
function isServerError(error) {
  var serverErrorPatterns = [
    'Internal error',
    'Service invoked too many times',
    'Spreadsheet not found',
    'Permission denied'
  ];

  var errorMsg = error.toString();
  return serverErrorPatterns.some(function(pattern) {
    return errorMsg.indexOf(pattern) !== -1;
  });
}

/**
 * 通知管理員（發生嚴重錯誤時）
 */
function notifyAdmin(subject, error) {
  try {
    var adminEmail = Session.getActiveUser().getEmail();
    var timestamp = new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });

    var body = '貓咪食堂系統錯誤通知\n\n' +
               '時間：' + timestamp + '\n' +
               '錯誤：' + error.toString() + '\n\n' +
               '錯誤堆疊：\n' + error.stack + '\n\n' +
               '請盡快檢查系統狀態。';

    // 發送郵件通知（可選，取消註解以啟用）
    // MailApp.sendEmail(adminEmail, subject, body);

    Logger.log('管理員通知已觸發（郵件功能未啟用）');
  } catch (e) {
    Logger.log('無法發送管理員通知: ' + e.toString());
  }
}

/**
 * 寫入錯誤日誌到試算表（選擇性功能）
 */
function writeErrorLog(logEntry) {
  try {
    var scriptProperties = PropertiesService.getScriptProperties();
    var errorLogId = scriptProperties.getProperty('ERROR_LOG_SPREADSHEET_ID');

    if (!errorLogId) {
      // 首次使用時建立錯誤日誌試算表
      var ss = SpreadsheetApp.create('貓咪食堂 - 錯誤日誌');
      var sheet = ss.getActiveSheet();
      sheet.setName('錯誤記錄');

      // 設定標題列
      var headers = ['時間', '函數', '錯誤訊息', '上下文', '堆疊'];
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.getRange(1, 1, 1, headers.length)
        .setBackground('#FF6B6B')
        .setFontColor('#FFFFFF')
        .setFontWeight('bold');

      scriptProperties.setProperty('ERROR_LOG_SPREADSHEET_ID', ss.getId());
      Logger.log('已建立錯誤日誌試算表: ' + ss.getUrl());

      errorLogId = ss.getId();
    }

    // 寫入錯誤記錄
    var sheet = SpreadsheetApp.openById(errorLogId).getSheets()[0];
    sheet.appendRow([
      logEntry.timestamp,
      logEntry.function,
      logEntry.error,
      JSON.stringify(logEntry.context),
      logEntry.stack
    ]);

  } catch (e) {
    Logger.log('無法寫入錯誤日誌: ' + e.toString());
  }
}

/**
 * 根據 ID 取得餐點資料
 */
function getMenuItemById(id) {
  var menu = getMenuData();
  var allItems = [].concat(menu.mains, menu.soups, menu.desserts, menu.drinks);
  return allItems.find(function(item) {
    return item.id === id;
  });
}

/**
 * 清理使用者輸入，防止 XSS
 */
function sanitizeInput(input) {
  if (typeof input !== 'string') return '';
  // 移除 HTML 標籤和特殊字元
  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    .trim();
}

/**
 * getMenuData() - 取得餐點選單資料
 * @returns {Object} 選單資料
 */
function getMenuData() {
  return {
    mains: [
      { id: 'm1', name: '貓爪咖哩飯', price: 120 },
      { id: 'm2', name: '鮭魚親子丼', price: 150 },
      { id: 'm3', name: '喵喵義大利麵', price: 130 },
      { id: 'm4', name: '貓掌漢堡排', price: 140 }
    ],
    soups: [
      { id: 's1', name: '貓咪味噌湯', price: 30 },
      { id: 's2', name: '奶油南瓜濃湯', price: 40 },
      { id: 's3', name: '海鮮巧達湯', price: 50 }
    ],
    desserts: [
      { id: 'd1', name: '貓掌布丁', price: 60 },
      { id: 'd2', name: '鮮奶雪花冰', price: 70 },
      { id: 'd3', name: '焦糖烤布蕾', price: 65 },
      { id: 'd4', name: '貓咪銅鑼燒', price: 55 }
    ],
    drinks: [
      { id: 'dr1', name: '貓爪拿鐵', price: 80 },
      { id: 'dr2', name: '焦糖瑪奇朵', price: 90 },
      { id: 'dr3', name: '抹茶拿鐵', price: 85 },
      { id: 'dr4', name: '水果茶', price: 70 },
      { id: 'dr5', name: '檸檬冰茶', price: 60 }
    ]
  };
}
