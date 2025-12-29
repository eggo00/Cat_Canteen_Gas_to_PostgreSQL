"""
選單服務
對應 Code.gs getMenuData (line 299-326)
"""


class MenuService:
    """選單管理服務"""

    @staticmethod
    def get_menu_data() -> dict:
        """
        取得完整選單資料
        對應 Code.gs getMenuData()
        """
        return {
            "mains": [
                {"id": "m1", "name": "貓爪咖哩飯", "price": 120},
                {"id": "m2", "name": "鮭魚親子丼", "price": 150},
                {"id": "m3", "name": "喵喵義大利麵", "price": 130},
                {"id": "m4", "name": "貓掌漢堡排", "price": 140}
            ],
            "soups": [
                {"id": "s1", "name": "貓咪味噌湯", "price": 30},
                {"id": "s2", "name": "奶油南瓜濃湯", "price": 40},
                {"id": "s3", "name": "海鮮巧達湯", "price": 50}
            ],
            "desserts": [
                {"id": "d1", "name": "貓掌布丁", "price": 60},
                {"id": "d2", "name": "鮮奶雪花冰", "price": 70},
                {"id": "d3", "name": "焦糖烤布蕾", "price": 65},
                {"id": "d4", "name": "貓咪銅鑼燒", "price": 55}
            ],
            "drinks": [
                {"id": "dr1", "name": "貓爪拿鐵", "price": 80},
                {"id": "dr2", "name": "焦糖瑪奇朵", "price": 90},
                {"id": "dr3", "name": "抹茶拿鐵", "price": 85},
                {"id": "dr4", "name": "水果茶", "price": 70},
                {"id": "dr5", "name": "檸檬冰茶", "price": 60}
            ]
        }

    @staticmethod
    def get_item_by_id(item_id: str) -> dict:
        """根據 ID 取得單一餐點資料"""
        menu = MenuService.get_menu_data()
        all_items = []
        all_items.extend(menu['mains'])
        all_items.extend(menu['soups'])
        all_items.extend(menu['desserts'])
        all_items.extend(menu['drinks'])

        for item in all_items:
            if item['id'] == item_id:
                return item

        return None
