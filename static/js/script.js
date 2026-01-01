// ===== 全域變數 =====
let cart = []; // 購物車
let menuData = {}; // 選單資料

// ===== 頁面載入時執行 =====
window.addEventListener('DOMContentLoaded', function() {
  // 隱藏載入畫面
  setTimeout(function() {
    document.getElementById('loading').classList.add('hidden');
  }, 800);

  // 載入選單資料
  loadMenu();
});

// ===== 載入選單 =====
async function loadMenu() {
  try {
    // 從後端 API 取得選單資料（改為 fetch，不再使用 google.script.run）
    const response = await fetch('/api/menu/');
    if (!response.ok) {
      throw new Error('載入選單失敗');
    }
    const data = await response.json();
    menuData = data;
    renderMenu(data);
  } catch (error) {
    console.error('載入選單失敗:', error);
    alert('載入選單時發生錯誤，請重新整理頁面');
  }
}

// ===== 渲染選單 =====
function renderMenu(data) {
  renderCategory('mains-menu', data.mains, false);
  renderCategory('soups-menu', data.soups, false);
  renderCategory('desserts-menu', data.desserts, false);
  renderCategory('drinks-menu', data.drinks, true);
}

// ===== 渲染分類選單 =====
function renderCategory(containerId, items, isDrink) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  items.forEach(function(item) {
    const itemDiv = createMenuItem(item, isDrink);
    container.appendChild(itemDiv);
  });
}

// ===== 建立選單項目 =====
function createMenuItem(item, isDrink) {
  const div = document.createElement('div');
  div.className = 'menu-item';
  div.id = 'item-' + item.id;

  let html = `
    <div class="menu-item-header">
      <div class="menu-item-name">${item.name}</div>
      <div class="menu-item-price">NT$ ${item.price}</div>
    </div>
  `;

  // 飲料選項（冰熱、甜度）
  if (isDrink) {
    html += `
      <div class="drink-options">
        <div class="option-group">
          <label>溫度：</label>
          <select id="temp-${item.id}">
            <option value="正常冰">正常冰</option>
            <option value="少冰">少冰</option>
            <option value="微冰">微冰</option>
            <option value="去冰">去冰</option>
            <option value="溫">溫</option>
            <option value="熱">熱</option>
          </select>
        </div>
        <div class="option-group">
          <label>甜度：</label>
          <select id="sweet-${item.id}">
            <option value="正常糖">正常糖</option>
            <option value="少糖">少糖</option>
            <option value="半糖">半糖</option>
            <option value="微糖">微糖</option>
            <option value="無糖">無糖</option>
          </select>
        </div>
      </div>
    `;
  }

  html += `
    <div class="quantity-control">
      <button class="quantity-btn" onclick="decreaseQuantity('${item.id}')">−</button>
      <span class="quantity-display" id="qty-${item.id}">1</span>
      <button class="quantity-btn" onclick="increaseQuantity('${item.id}')">+</button>
    </div>
    <button class="add-btn" onclick="addToCart('${item.id}', ${isDrink})">
      🐾 加入訂單
    </button>
  `;

  div.innerHTML = html;
  return div;
}

// ===== 數量控制 =====
function increaseQuantity(itemId) {
  const qtyElement = document.getElementById('qty-' + itemId);
  let qty = parseInt(qtyElement.textContent);
  if (qty < 99) {
    qtyElement.textContent = qty + 1;
  }
}

function decreaseQuantity(itemId) {
  const qtyElement = document.getElementById('qty-' + itemId);
  let qty = parseInt(qtyElement.textContent);
  if (qty > 1) {
    qtyElement.textContent = qty - 1;
  }
}

// ===== 加入購物車 =====
function addToCart(itemId, isDrink) {
  // 找到餐點資料
  let item = findItemById(itemId);
  if (!item) return;

  // 取得數量
  const quantity = parseInt(document.getElementById('qty-' + itemId).textContent);

  // 建立購物車項目
  let cartItem = {
    id: itemId,
    name: item.name,
    price: item.price,
    quantity: quantity
  };

  // 如果是飲料，加入溫度和甜度
  if (isDrink) {
    const tempSelect = document.getElementById('temp-' + itemId);
    const sweetSelect = document.getElementById('sweet-' + itemId);
    cartItem.temperature = tempSelect.value;
    cartItem.sweetness = sweetSelect.value;
    console.log('飲料選項 - ID:', itemId, '溫度:', cartItem.temperature, '甜度:', cartItem.sweetness);
  }

  // 檢查購物車中是否已有相同項目
  let existingItem = cart.find(function(existing) {
    // 比較 ID
    if (existing.id !== itemId) return false;

    // 如果是飲料，還需要比較溫度和甜度
    if (isDrink) {
      return existing.temperature === cartItem.temperature &&
             existing.sweetness === cartItem.sweetness;
    }

    // 如果不是飲料，只要 ID 相同就算相同項目
    return true;
  });

  if (existingItem) {
    // 已存在，增加數量
    existingItem.quantity += quantity;
  } else {
    // 不存在，加入購物車
    cart.push(cartItem);
  }

  // 重設數量為 1
  document.getElementById('qty-' + itemId).textContent = '1';

  // 更新訂單顯示
  updateOrderSummary();

  // 顯示提示
  showToast('已加入訂單！');
}

// ===== 尋找餐點 =====
function findItemById(itemId) {
  for (let category in menuData) {
    const item = menuData[category].find(function(i) {
      return i.id === itemId;
    });
    if (item) return item;
  }
  return null;
}

// ===== 更新訂單摘要 =====
function updateOrderSummary() {
  const summaryDiv = document.getElementById('order-summary');

  if (cart.length === 0) {
    summaryDiv.innerHTML = '<p class="empty-order">還沒有選擇任何餐點喔～</p>';
    document.getElementById('total-amount').textContent = 'NT$ 0';
    return;
  }

  let html = '';
  let total = 0;

  cart.forEach(function(item, index) {
    const itemTotal = item.price * item.quantity;
    total += itemTotal;

    let details = `數量: ${item.quantity}`;
    if (item.temperature || item.sweetness) {
      details += ` | ${item.temperature || ''} ${item.sweetness || ''}`;
    }

    html += `
      <div class="order-item">
        <div class="order-item-info">
          <div class="order-item-name">${item.name}</div>
          <div class="order-item-details">${details}</div>
        </div>
        <div class="order-item-price">NT$ ${itemTotal}</div>
        <button class="remove-item" onclick="removeFromCart(${index})" title="移除">✕</button>
      </div>
    `;
  });

  summaryDiv.innerHTML = html;
  document.getElementById('total-amount').textContent = 'NT$ ' + total;
}

// ===== 從購物車移除 =====
function removeFromCart(index) {
  cart.splice(index, 1);
  updateOrderSummary();
  showToast('已移除');
}

// ===== 送出訂單 =====
async function submitOrder() {
  // 驗證
  const customerName = document.getElementById('customerName').value.trim();

  if (!customerName) {
    alert('請輸入您的姓名');
    document.getElementById('customerName').focus();
    return;
  }

  if (cart.length === 0) {
    alert('請至少選擇一項餐點');
    return;
  }

  // 取得取餐方式
  const diningOption = document.querySelector('input[name="diningOption"]:checked').value;

  // 取得備註
  const note = document.getElementById('note').value.trim();

  // 計算總金額
  let totalAmount = 0;
  cart.forEach(function(item) {
    totalAmount += item.price * item.quantity;
  });

  // 準備訂單資料
  const orderData = {
    customerName: customerName,
    diningOption: diningOption,
    note: note,
    items: cart,
    totalAmount: totalAmount
  };

  // 除錯：顯示訂單資料
  console.log('準備送出訂單資料:', orderData);
  console.log('訂單資料 JSON:', JSON.stringify(orderData, null, 2));

  // 禁用送出按鈕
  const submitBtn = document.getElementById('submit-btn');
  submitBtn.disabled = true;
  submitBtn.textContent = '送出中...';

  try {
    // 送出到後端 API（改為 fetch，不再使用 google.script.run）
    const response = await fetch('/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData)
    });

    const result = await response.json();

    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span class="btn-icon">🐾</span> 送出訂單';

    if (response.ok && result.success) {
      // 顯示成功訊息
      showSuccessModal(result.orderNumber);

      // 清空購物車和表單
      clearOrder();
    } else {
      alert(result.detail || result.message || '送出失敗，請再試一次');
    }
  } catch (error) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span class="btn-icon">🐾</span> 送出訂單';
    console.error('送出訂單失敗:', error);
    alert('送出訂單時發生錯誤，請再試一次');
  }
}

// ===== 顯示成功 Modal =====
function showSuccessModal(orderNumber) {
  const modal = document.getElementById('success-modal');
  document.getElementById('order-number').textContent = orderNumber;
  modal.classList.add('show');
}

// ===== 關閉 Modal =====
function closeModal() {
  const modal = document.getElementById('success-modal');
  modal.classList.remove('show');
}

// ===== 清空訂單 =====
function clearOrder() {
  // 清空購物車
  cart = [];
  updateOrderSummary();

  // 清空表單
  document.getElementById('customerName').value = '';
  document.getElementById('note').value = '';
  document.querySelector('input[name="diningOption"][value="內用"]').checked = true;
}

// ===== Toast 提示 =====
function showToast(message) {
  // 建立 toast 元素
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #F4A460 0%, #DEB887 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 25px;
    box-shadow: 0 4px 15px rgba(244, 164, 96, 0.4);
    z-index: 10000;
    animation: slideInRight 0.3s ease-out;
    font-weight: bold;
  `;
  toast.textContent = message;

  // 加入頁面
  document.body.appendChild(toast);

  // 3 秒後移除
  setTimeout(function() {
    toast.style.animation = 'slideOutRight 0.3s ease-out';
    setTimeout(function() {
      document.body.removeChild(toast);
    }, 300);
  }, 2000);
}
