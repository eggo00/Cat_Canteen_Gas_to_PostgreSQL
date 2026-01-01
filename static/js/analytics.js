// Analytics Dashboard JavaScript
// 全域變數儲存圖表實例
let charts = {};

// 顏色配置
const COLORS = {
  primary: '#667eea',
  secondary: '#764ba2',
  success: '#48bb78',
  warning: '#ed8936',
  danger: '#f56565',
  info: '#4299e1',
  purple: '#9f7aea',
  pink: '#ed64a6',
  teal: '#38b2ac',
  orange: '#ed8936'
};

const CHART_COLORS = [
  COLORS.primary,
  COLORS.secondary,
  COLORS.success,
  COLORS.warning,
  COLORS.danger,
  COLORS.info,
  COLORS.purple,
  COLORS.pink,
  COLORS.teal,
  COLORS.orange
];

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  setDefaultDates();
  updateCharts();
});

// 設定預設日期（當天）
function setDefaultDates() {
  const today = new Date();

  document.getElementById('startDate').value = formatDate(today);
  document.getElementById('endDate').value = formatDate(today);
}

// 設定最近 30 天
function setLast30Days() {
  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 30);

  document.getElementById('startDate').value = formatDate(startDate);
  document.getElementById('endDate').value = formatDate(endDate);

  updateCharts();
}

// 格式化日期為 YYYY-MM-DD
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 取得日期參數
function getDateParams() {
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  return `start_date=${startDate}&end_date=${endDate}`;
}

// 顯示載入中
function showLoading() {
  document.getElementById('loading').style.display = 'block';
}

// 隱藏載入中
function hideLoading() {
  document.getElementById('loading').style.display = 'none';
}

// 更新所有圖表
async function updateCharts() {
  showLoading();

  try {
    await Promise.all([
      updateSummaryCards(),
      updateRevenueChart(),
      updatePopularDishesChart(),
      updatePopularDrinksChart(),
      updatePickupMethodChart(),
      updatePeakHoursChart(),
      updateIceLevelChart(),
      updateSweetnessChart()
    ]);
  } catch (error) {
    console.error('更新圖表時發生錯誤:', error);
    alert('載入資料時發生錯誤，請稍後再試');
  } finally {
    hideLoading();
  }
}

// 更新摘要卡片
async function updateSummaryCards() {
  const dateParams = getDateParams();

  // 取得平均客單價
  const avgResponse = await fetch(`/api/analytics/revenue/average-order-value?${dateParams}`);
  const avgData = await avgResponse.json();

  // 取得尖峰時段
  const peakResponse = await fetch(`/api/analytics/customer-behavior/peak-hours?${dateParams}`);
  const peakData = await peakResponse.json();

  document.getElementById('totalRevenue').textContent = `NT$ ${avgData.total_revenue.toLocaleString()}`;
  document.getElementById('totalOrders').textContent = avgData.total_orders.toLocaleString();
  document.getElementById('avgOrderValue').textContent = `NT$ ${Math.round(avgData.average_order_value).toLocaleString()}`;
  document.getElementById('peakHour').textContent = `${peakData.peak_hour}:00`;
}

// 更新營收趨勢圖表
async function updateRevenueChart() {
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  const dateParams = getDateParams();

  const ctx = document.getElementById('revenueChart');

  // 銷毀舊圖表
  if (charts.revenue) {
    charts.revenue.destroy();
  }

  // 檢查是否為單日查詢
  const isSingleDay = startDate === endDate;

  let chartData, chartLabel;

  if (isSingleDay) {
    // 單日：顯示每小時營收
    const response = await fetch(`/api/analytics/customer-behavior/peak-hours?${dateParams}`);
    const data = await response.json();

    chartData = {
      labels: data.hourly_data.map(h => `${h.hour}:00`),
      datasets: [{
        label: '每小時營收 (NT$)',
        data: data.hourly_data.map(h => h.revenue),
        borderColor: COLORS.primary,
        backgroundColor: COLORS.primary + '20',
        fill: true,
        tension: 0.4
      }]
    };
  } else {
    // 多日：顯示每日營收
    const response = await fetch(`/api/analytics/revenue/daily?${dateParams}`);
    const data = await response.json();

    chartData = {
      labels: data.data.map(d => d.date),
      datasets: [{
        label: '每日營收 (NT$)',
        data: data.data.map(d => d.revenue),
        borderColor: COLORS.primary,
        backgroundColor: COLORS.primary + '20',
        fill: true,
        tension: 0.4
      }]
    };
  }

  charts.revenue = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `營收: NT$ ${context.parsed.y.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return 'NT$ ' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

// 更新熱門餐點圖表
async function updatePopularDishesChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/popular-items/dishes?${dateParams}&limit=10`);
  const data = await response.json();

  const ctx = document.getElementById('dishesChart');

  if (charts.dishes) {
    charts.dishes.destroy();
  }

  charts.dishes = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.items.map(item => item.item_name),
      datasets: [{
        label: '銷售數量',
        data: data.items.map(item => item.total_quantity),
        backgroundColor: CHART_COLORS
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const item = data.items[context.dataIndex];
              return [
                `數量: ${item.total_quantity}`,
                `營收: NT$ ${item.total_revenue.toLocaleString()}`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true
        }
      }
    }
  });
}

// 更新熱門飲料圖表
async function updatePopularDrinksChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/popular-items/drinks?${dateParams}&limit=10`);
  const data = await response.json();

  const ctx = document.getElementById('drinksChart');

  if (charts.drinks) {
    charts.drinks.destroy();
  }

  charts.drinks = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.items.map(item => item.item_name),
      datasets: [{
        label: '銷售數量',
        data: data.items.map(item => item.total_quantity),
        backgroundColor: CHART_COLORS
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const item = data.items[context.dataIndex];
              return [
                `數量: ${item.total_quantity}`,
                `營收: NT$ ${item.total_revenue.toLocaleString()}`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true
        }
      }
    }
  });
}

// 更新內用外帶比例圖表
async function updatePickupMethodChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/customer-behavior/pickup-method-ratio?${dateParams}`);
  const data = await response.json();

  const ctx = document.getElementById('pickupChart');

  if (charts.pickup) {
    charts.pickup.destroy();
  }

  charts.pickup = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.stats.map(s => s.pickup_method),
      datasets: [{
        data: data.stats.map(s => s.count),
        backgroundColor: [COLORS.primary, COLORS.secondary]
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const stat = data.stats[context.dataIndex];
              return [
                `${stat.pickup_method}: ${stat.count} 筆`,
                `比例: ${stat.percentage}%`,
                `營收: NT$ ${stat.revenue.toLocaleString()}`
              ];
            }
          }
        },
        datalabels: {
          color: '#fff',
          font: {
            size: 16,
            weight: 'bold'
          },
          formatter: function(value, context) {
            const stat = data.stats[context.dataIndex];
            return `${stat.count}\n${stat.percentage.toFixed(1)}%`;
          }
        }
      }
    }
  });
}

// 更新尖峰時段圖表
async function updatePeakHoursChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/customer-behavior/peak-hours?${dateParams}`);
  const data = await response.json();

  const ctx = document.getElementById('peakHoursChart');

  if (charts.peakHours) {
    charts.peakHours.destroy();
  }

  charts.peakHours = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.hourly_data.map(h => `${h.hour}:00`),
      datasets: [{
        label: '訂單數量',
        data: data.hourly_data.map(h => h.order_count),
        backgroundColor: COLORS.success
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const hour = data.hourly_data[context.dataIndex];
              return [
                `訂單: ${hour.order_count} 筆`,
                `營收: NT$ ${hour.revenue.toLocaleString()}`
              ];
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  });
}

// 更新冰度偏好圖表
async function updateIceLevelChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/beverage-preferences/ice-level?${dateParams}`);
  const data = await response.json();

  const ctx = document.getElementById('iceLevelChart');

  if (charts.iceLevel) {
    charts.iceLevel.destroy();
  }

  if (data.preferences.length === 0) {
    // 沒有資料時顯示提示
    ctx.parentElement.innerHTML = '<p style="text-align:center; padding:50px; color:#999;">暫無資料</p><canvas id="iceLevelChart"></canvas>';
    return;
  }

  charts.iceLevel = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.preferences.map(p => p.option),
      datasets: [{
        data: data.preferences.map(p => p.count),
        backgroundColor: CHART_COLORS
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const pref = data.preferences[context.dataIndex];
              return [
                `${pref.option}: ${pref.count} 杯`,
                `比例: ${pref.percentage}%`
              ];
            }
          }
        },
        datalabels: {
          color: '#fff',
          font: {
            size: 14,
            weight: 'bold'
          },
          formatter: function(value, context) {
            const pref = data.preferences[context.dataIndex];
            return `${pref.count}\n${pref.percentage.toFixed(1)}%`;
          }
        }
      }
    }
  });
}

// 更新甜度偏好圖表
async function updateSweetnessChart() {
  const dateParams = getDateParams();
  const response = await fetch(`/api/analytics/beverage-preferences/sweetness?${dateParams}`);
  const data = await response.json();

  const ctx = document.getElementById('sweetnessChart');

  if (charts.sweetness) {
    charts.sweetness.destroy();
  }

  if (data.preferences.length === 0) {
    // 沒有資料時顯示提示
    ctx.parentElement.innerHTML = '<p style="text-align:center; padding:50px; color:#999;">暫無資料</p><canvas id="sweetnessChart"></canvas>';
    return;
  }

  charts.sweetness = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.preferences.map(p => p.option),
      datasets: [{
        data: data.preferences.map(p => p.count),
        backgroundColor: CHART_COLORS
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const pref = data.preferences[context.dataIndex];
              return [
                `${pref.option}: ${pref.count} 杯`,
                `比例: ${pref.percentage}%`
              ];
            }
          }
        },
        datalabels: {
          color: '#fff',
          font: {
            size: 14,
            weight: 'bold'
          },
          formatter: function(value, context) {
            const pref = data.preferences[context.dataIndex];
            return `${pref.count}\n${pref.percentage.toFixed(1)}%`;
          }
        }
      }
    }
  });
}

// ========== Orders Modal Functions ==========

// 顯示訂單明細 Modal
async function showOrdersModal() {
  const modal = document.getElementById('ordersModal');
  modal.style.display = 'block';

  // 載入訂單資料
  await loadOrders();
}

// 關閉訂單明細 Modal
function closeOrdersModal() {
  const modal = document.getElementById('ordersModal');
  modal.style.display = 'none';
}

// 載入訂單列表
async function loadOrders() {
  const container = document.getElementById('ordersTableContainer');

  try {
    const dateParams = getDateParams();
    const response = await fetch(`/api/orders/?limit=1000`);
    const orders = await response.json();

    if (orders.length === 0) {
      container.innerHTML = '<p style="text-align: center; padding: 50px; color: #999;">暫無訂單資料</p>';
      return;
    }

    // 根據日期範圍篩選訂單
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    endDate.setHours(23, 59, 59, 999); // 包含整天

    const filteredOrders = orders.filter(order => {
      const orderDate = new Date(order.created_at);
      return orderDate >= startDate && orderDate <= endDate;
    });

    if (filteredOrders.length === 0) {
      container.innerHTML = '<p style="text-align: center; padding: 50px; color: #999;">所選日期範圍內無訂單</p>';
      return;
    }

    // 按建立時間倒序排列
    filteredOrders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    // 建立表格
    let tableHTML = `
      <table class="orders-table">
        <thead>
          <tr>
            <th>訂單編號</th>
            <th>顧客姓名</th>
            <th>取餐方式</th>
            <th>訂單內容</th>
            <th>總金額</th>
            <th>訂購時間</th>
          </tr>
        </thead>
        <tbody>
    `;

    filteredOrders.forEach(order => {
      // 格式化訂單內容
      let itemsText = '';
      if (order.items && order.items.length > 0) {
        itemsText += order.items.map(item =>
          `${item.name} x${item.quantity}`
        ).join(', ');
      }
      if (order.drinks && order.drinks.length > 0) {
        if (itemsText) itemsText += '<br>';
        itemsText += order.drinks.map(drink => {
          let drinkText = `${drink.name} x${drink.quantity}`;
          // 只有當溫度和甜度都存在時才顯示
          if (drink.temperature && drink.sweetness) {
            drinkText += ` (${drink.temperature}/${drink.sweetness})`;
          }
          return drinkText;
        }).join(', ');
      }

      // 格式化時間
      const orderDate = new Date(order.created_at);
      const formattedDate = orderDate.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });

      tableHTML += `
        <tr>
          <td><strong>${order.order_number}</strong></td>
          <td>${order.customer_name}</td>
          <td>${order.pickup_method}</td>
          <td><div class="order-items">${itemsText}</div></td>
          <td><strong>NT$ ${order.total_amount.toLocaleString()}</strong></td>
          <td>${formattedDate}</td>
        </tr>
      `;
    });

    tableHTML += `
        </tbody>
      </table>
      <p style="margin-top: 20px; text-align: center; color: #666;">
        共 ${filteredOrders.length} 筆訂單
      </p>
    `;

    container.innerHTML = tableHTML;

  } catch (error) {
    console.error('載入訂單時發生錯誤:', error);
    container.innerHTML = '<p style="text-align: center; padding: 50px; color: #f56565;">載入訂單時發生錯誤</p>';
  }
}

// 點擊 Modal 外部關閉
window.onclick = function(event) {
  const modal = document.getElementById('ordersModal');
  if (event.target === modal) {
    closeOrdersModal();
  }
}
