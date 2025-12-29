"""
輸入驗證工具
對應 Code.gs 的 sanitizeInput 和驗證邏輯
"""


def sanitize_input(input_str: str) -> str:
    """
    清理使用者輸入，防止 XSS
    對應 Code.gs line 283-293
    """
    if not input_str:
        return ""

    # 移除 HTML 標籤和特殊字元
    sanitized = input_str.strip()
    sanitized = sanitized.replace('<', '&lt;')
    sanitized = sanitized.replace('>', '&gt;')
    sanitized = sanitized.replace('"', '&quot;')
    sanitized = sanitized.replace("'", '&#x27;')
    sanitized = sanitized.replace('/', '&#x2F;')

    return sanitized


def validate_price(items: list, total_amount: int) -> bool:
    """
    驗證訂單總金額是否正確
    對應 Code.gs line 83-122 的價格驗證邏輯
    """
    calculated_total = 0

    for item in items:
        item_total = item.get('price', 0) * item.get('quantity', 0)
        calculated_total += item_total

    return calculated_total == total_amount


def get_menu_item_by_id(item_id: str) -> dict:
    """
    根據 ID 取得餐點資料
    對應 Code.gs getMenuItemById (line 272-278)
    """
    from app.services.menu_service import MenuService
    menu = MenuService.get_menu_data()

    # 搜尋所有分類
    all_items = []
    all_items.extend(menu['mains'])
    all_items.extend(menu['soups'])
    all_items.extend(menu['desserts'])
    all_items.extend(menu['drinks'])

    for item in all_items:
        if item['id'] == item_id:
            return item

    return None
