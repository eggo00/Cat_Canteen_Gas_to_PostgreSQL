"""
訂單編號生成工具
對應 OrderService.gs generateOrderNumber (line 68-78)
"""
from datetime import datetime


def generate_order_number() -> str:
    """
    產生訂單編號
    格式：CAT + YYMMDDHHmmss
    範例：CAT231225143530
    """
    now = datetime.now()

    year = now.strftime('%y')      # 年份後兩碼
    month = now.strftime('%m')     # 月份
    day = now.strftime('%d')       # 日期
    hours = now.strftime('%H')     # 時
    minutes = now.strftime('%M')   # 分
    seconds = now.strftime('%S')   # 秒

    order_number = f"CAT{year}{month}{day}{hours}{minutes}{seconds}"

    return order_number
