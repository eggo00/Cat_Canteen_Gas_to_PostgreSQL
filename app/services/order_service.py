"""
訂單服務
對應 OrderService.gs 的功能
"""
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate
from app.utils.order_number import generate_order_number
from app.utils.validation import validate_price
from app.services.menu_service import MenuService
from typing import List, Tuple


class OrderService:
    """訂單處理服務"""

    @staticmethod
    def validate_order_items(items: list) -> Tuple[bool, str]:
        """
        驗證訂單項目的價格是否正確
        對應 Code.gs line 105-113 的價格驗證
        """
        menu_service = MenuService()

        for item in items:
            # 取得正確的餐點資料
            menu_item = menu_service.get_item_by_id(item.id)

            if not menu_item:
                return False, f"無效的餐點項目：{item.id}"

            # 驗證價格
            if item.price != menu_item['price']:
                return False, f"餐點價格不符：{item.name}"

        return True, "驗證通過"

    @staticmethod
    def validate_total_amount(items: list, total_amount: int) -> bool:
        """
        驗證總金額是否正確
        對應 Code.gs line 116-122
        """
        calculated_total = sum(item.price * item.quantity for item in items)
        return calculated_total == total_amount

    @staticmethod
    def format_items(items: list) -> str:
        """
        格式化餐點明細
        對應 OrderService.gs formatItems (line 83-101)
        """
        if not items:
            return "-"

        formatted = []
        for item in items:
            detail = f"{item['name']} x{item['quantity']}"

            # 如果有溫度和甜度選項（飲料）
            options = []
            if item.get('temperature'):
                options.append(item['temperature'])
            if item.get('sweetness'):
                options.append(item['sweetness'])

            if options:
                detail += f" ({', '.join(options)})"

            formatted.append(detail)

        return ", ".join(formatted)

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        """
        建立訂單
        對應 OrderService.gs saveOrder (line 108-159)
        """
        # 產生訂單編號
        order_number = generate_order_number()

        # 分離餐點與飲料
        meals = []
        drinks = []

        for item in order_data.items:
            item_dict = item.model_dump()
            if item.id.startswith('dr'):
                drinks.append(item_dict)
            else:
                meals.append(item_dict)

        # 建立訂單記錄
        db_order = Order(
            order_number=order_number,
            customer_name=order_data.customerName,
            pickup_method=order_data.diningOption,
            items=meals,
            drinks=drinks,
            total_amount=order_data.totalAmount,
            notes=order_data.note or ""
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return db_order

    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """取得訂單列表"""
        return db.query(Order).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_order_by_number(db: Session, order_number: str) -> Order:
        """根據訂單編號查詢訂單"""
        return db.query(Order).filter(Order.order_number == order_number).first()
