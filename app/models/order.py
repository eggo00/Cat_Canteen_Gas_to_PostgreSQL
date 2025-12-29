"""
訂單資料模型（SQLAlchemy ORM）
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    """訂單模型"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, comment="訂單 ID")
    order_number = Column(String(20), unique=True, nullable=False, index=True, comment="訂單編號")
    customer_name = Column(String(100), nullable=False, comment="顧客姓名")
    pickup_method = Column(String(20), nullable=False, comment="取餐方式（內用/外帶）")
    items = Column(JSON, nullable=False, comment="餐點明細（JSON 格式）")
    drinks = Column(JSON, comment="飲料明細（JSON 格式）")
    total_amount = Column(Integer, nullable=False, comment="總金額")
    notes = Column(Text, comment="備註")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        comment="建立時間"
    )

    def __repr__(self):
        return f"<Order {self.order_number}: {self.customer_name} - NT${self.total_amount}>"
