"""
生成測試訂單資料
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.order import Order
from datetime import datetime, timedelta
import random

# 三個字的中文姓名
NAMES = [
    "王小明", "李美玲", "張志豪", "陳雅婷", "林志偉",
    "黃淑芬", "吳建宏", "蔡佳玲", "鄭文華", "劉俊傑",
    "許雅雯", "謝承翰", "楊佳慧", "賴文心", "施俊宇",
    "呂佳穎", "洪志強", "宋雅芳", "江承恩", "何佳玲",
    "羅文傑", "葉淑惠", "朱志豪", "曾雅婷", "游建華",
    "詹美玲", "高志偉", "梁雅芬", "孫建宏", "石雅婷"
]

# 菜單項目
DISHES = [
    {"id": "m1", "name": "貓爪咖哩飯", "price": 120},
    {"id": "m2", "name": "喵喵義大利麵", "price": 150},
    {"id": "m3", "name": "貓咪漢堡套餐", "price": 180},
    {"id": "m4", "name": "虎斑三明治", "price": 100},
    {"id": "m5", "name": "波斯貓沙拉", "price": 130}
]

DRINKS = [
    {"id": "dr1", "name": "貓爪拿鐵", "price": 80},
    {"id": "dr2", "name": "喵喵奶茶", "price": 70},
    {"id": "dr3", "name": "橘貓果汁", "price": 60},
    {"id": "dr4", "name": "黑貓可可", "price": 75},
    {"id": "dr5", "name": "白貓優格飲", "price": 65}
]

# 飲料選項
ICE_LEVELS = ["正常冰", "少冰", "微冰", "去冰", "溫", "熱"]
SWEETNESS = ["正常糖", "少糖", "半糖", "微糖", "無糖"]

# 取餐方式
PICKUP_METHODS = ["內用", "外帶"]

def generate_order_number(index):
    """生成訂單編號"""
    timestamp = datetime.now().strftime("%y%m%d")
    return f"ORD{timestamp}{index:04d}"

def generate_random_datetime(days_ago=30):
    """生成隨機日期時間（最近N天內）"""
    now = datetime.now()
    days_offset = random.randint(0, days_ago)
    hours_offset = random.randint(10, 21)  # 營業時間 10:00 - 21:00
    minutes_offset = random.randint(0, 59)

    random_date = now - timedelta(days=days_offset)
    random_date = random_date.replace(hour=hours_offset, minute=minutes_offset, second=0, microsecond=0)
    return random_date

def create_test_orders(count=30):
    """建立測試訂單"""
    db = SessionLocal()

    try:
        print(f"開始生成 {count} 筆測試訂單...")

        for i in range(count):
            # 隨機選擇客戶
            customer_name = random.choice(NAMES)
            pickup_method = random.choice(PICKUP_METHODS)

            # 隨機選擇餐點（1-3 種）
            num_dishes = random.randint(1, 3)
            selected_dishes = random.sample(DISHES, num_dishes)
            items = []
            total_amount = 0

            for dish in selected_dishes:
                quantity = random.randint(1, 2)
                items.append({
                    "id": dish["id"],
                    "name": dish["name"],
                    "price": dish["price"],
                    "quantity": quantity
                })
                total_amount += dish["price"] * quantity

            # 隨機選擇飲料（0-2 種）
            drinks = []
            if random.random() > 0.2:  # 80% 機率點飲料
                num_drinks = random.randint(1, 2)
                selected_drinks = random.sample(DRINKS, num_drinks)

                for drink in selected_drinks:
                    quantity = random.randint(1, 2)
                    drinks.append({
                        "id": drink["id"],
                        "name": drink["name"],
                        "price": drink["price"],
                        "quantity": quantity,
                        "temperature": random.choice(ICE_LEVELS),
                        "sweetness": random.choice(SWEETNESS)
                    })
                    total_amount += drink["price"] * quantity

            # 建立訂單
            order = Order(
                order_number=generate_order_number(i + 1),
                customer_name=customer_name,
                pickup_method=pickup_method,
                items=items,
                drinks=drinks if drinks else None,
                total_amount=total_amount,
                created_at=generate_random_datetime(30)
            )

            db.add(order)
            print(f"[{i+1}/{count}] {customer_name} - {pickup_method} - NT$ {total_amount}")

        db.commit()
        print(f"\n✓ 成功建立 {count} 筆測試訂單！")

    except Exception as e:
        db.rollback()
        print(f"錯誤: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_orders(30)
