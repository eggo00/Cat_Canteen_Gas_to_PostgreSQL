"""
補足訂單中飲料的溫度和甜度資料
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.order import Order
import random

# 溫度選項
TEMPERATURES = ["正常冰", "少冰", "微冰", "去冰", "溫", "熱"]

# 甜度選項
SWEETNESS = ["正常糖", "少糖", "半糖", "微糖", "無糖"]

def fix_drink_preferences():
    """補足所有訂單中缺少溫度和甜度的飲料"""
    db = SessionLocal()

    try:
        # 取得所有訂單
        orders = db.query(Order).all()

        updated_count = 0
        drink_count = 0

        print(f"檢查 {len(orders)} 筆訂單...")

        for order in orders:
            # 檢查是否有飲料
            if not order.drinks or len(order.drinks) == 0:
                continue

            # 檢查每杯飲料是否缺少溫度或甜度
            order_updated = False

            for drink in order.drinks:
                # 如果缺少溫度，隨機補上
                if not drink.get('temperature'):
                    drink['temperature'] = random.choice(TEMPERATURES)
                    order_updated = True
                    drink_count += 1

                # 如果缺少甜度，隨機補上
                if not drink.get('sweetness'):
                    drink['sweetness'] = random.choice(SWEETNESS)
                    order_updated = True

            # 如果有更新，標記為修改
            if order_updated:
                # 使用 flag_modified 告訴 SQLAlchemy JSON 欄位已修改
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(order, 'drinks')
                updated_count += 1
                print(f"  ✓ 訂單 {order.order_number}: 已補足 {len(order.drinks)} 杯飲料的資料")

        # 提交變更
        db.commit()

        print(f"\n完成！")
        print(f"  更新訂單數: {updated_count} 筆")
        print(f"  補足飲料數: {drink_count} 杯")

    except Exception as e:
        db.rollback()
        print(f"錯誤: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_drink_preferences()
