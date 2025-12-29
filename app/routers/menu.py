"""
選單 API 路由
對應 Code.gs getMenuData
"""
from fastapi import APIRouter
from app.services.menu_service import MenuService

router = APIRouter(prefix="/api/menu", tags=["menu"])


@router.get("/")
async def get_menu():
    """
    取得完整選單資料
    對應 Code.gs getMenuData()
    """
    return MenuService.get_menu_data()


@router.get("/item/{item_id}")
async def get_menu_item(item_id: str):
    """根據 ID 取得單一餐點資料"""
    item = MenuService.get_item_by_id(item_id)
    if not item:
        return {"error": "找不到該餐點"}
    return item
