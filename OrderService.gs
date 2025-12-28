/**
 * OrderService - 訂單處理服務
 * 負責將訂單資料寫入 Google Sheets
 */

var OrderService = (function() {

  // Google Sheet 設定
  var SHEET_NAME = '貓咪食堂訂單';

  /**
   * 取得或建立訂單試算表
   */
  function getOrCreateSheet() {
    var scriptProperties = PropertiesService.getScriptProperties();
    var spreadsheetId = scriptProperties.getProperty('SPREADSHEET_ID');
    var ss;

    // 如果已經有儲存的試算表 ID，嘗試開啟
    if (spreadsheetId) {
      try {
        ss = SpreadsheetApp.openById(spreadsheetId);
      } catch (e) {
        Logger.log('無法開啟現有試算表，將建立新的: ' + e);
        ss = null;
      }
    }

    // 如果沒有試算表，建立新的
    if (!ss) {
      ss = SpreadsheetApp.create('貓咪食堂訂單記錄');
      scriptProperties.setProperty('SPREADSHEET_ID', ss.getId());
      Logger.log('已建立新試算表: ' + ss.getUrl());
    }

    var sheet = ss.getSheetByName(SHEET_NAME);

    // 如果沂有此工作表，建立並設定標題列
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);

      // 設定標題列
      var headers = ['時間戳記', '訂單編號', '姓名', '取餐方式', '餐點明細', '飲料明細', '總金額', '備註'];
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

      // 美化標題列
      sheet.getRange(1, 1, 1, headers.length)
        .setBackground('#F4A460')
        .setFontColor('#FFFFFF')
        .setFontWeight('bold')
        .setHorizontalAlignment('center');

      // 凍結標題列
      sheet.setFrozenRows(1);

      // 自動調整欄寬
      for (var i = 1; i <= headers.length; i++) {
        sheet.autoResizeColumn(i);
      }
    }

    return sheet;
  }

  /**
   * 產生訂單編號
   */
  function generateOrderNumber() {
    var now = new Date();
    var year = now.getFullYear().toString().substr(-2);
    var month = ('0' + (now.getMonth() + 1)).slice(-2);
    var day = ('0' + now.getDate()).slice(-2);
    var hours = ('0' + now.getHours()).slice(-2);
    var minutes = ('0' + now.getMinutes()).slice(-2);
    var seconds = ('0' + now.getSeconds()).slice(-2);

    return 'CAT' + year + month + day + hours + minutes + seconds;
  }

  /**
   * 格式化餐點明細
   */
  function formatItems(items) {
    if (!items || items.length === 0) {
      return '-';
    }

    return items.map(function(item) {
      var detail = item.name + ' x' + item.quantity;

      // 如果有溫度和甜度選項（飲料）
      if (item.temperature || item.sweetness) {
        var options = [];
        if (item.temperature) options.push(item.temperature);
        if (item.sweetness) options.push(item.sweetness);
        detail += ' (' + options.join(', ') + ')';
      }

      return detail;
    }).join(', ');
  }

  /**
   * 儲存訂單到 Google Sheets
   * @param {Object} orderData - 訂單資料
   * @returns {Object} 處理結果
   */
  function saveOrder(orderData) {
    try {
      var sheet = getOrCreateSheet();
      var orderNumber = generateOrderNumber();
      var timestamp = new Date();

      // 分離餐點與飲料
      var meals = [];
      var drinks = [];

      if (orderData.items && orderData.items.length > 0) {
        orderData.items.forEach(function(item) {
          if (item.id.startsWith('dr')) {
            drinks.push(item);
          } else {
            meals.push(item);
          }
        });
      }

      // 格式化資料
      var mealsText = formatItems(meals);
      var drinksText = formatItems(drinks);

      // 準備要寫入的資料列
      var rowData = [
        timestamp,                        // 時間戳記
        orderNumber,                      // 訂單編號
        orderData.customerName || '',     // 姓名
        orderData.diningOption || '',     // 取餐方式
        mealsText,                        // 餐點明細
        drinksText,                       // 飲料明細
        orderData.totalAmount || 0,       // 總金額
        orderData.note || ''              // 備註
      ];

      // 寫入新列
      sheet.appendRow(rowData);

      Logger.log('訂單已儲存: ' + orderNumber);

      return {
        success: true,
        orderNumber: orderNumber,
        sheetUrl: sheet.getParent().getUrl()
      };

    } catch (error) {
      Logger.log('儲存訂單時發生錯誤: ' + error.toString());
      throw error;
    }
  }

  // 公開的方法
  return {
    saveOrder: saveOrder
  };

})();
