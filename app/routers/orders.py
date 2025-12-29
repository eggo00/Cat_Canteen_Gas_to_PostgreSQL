"""
訂單 API 路由
對應 Code.gs submitOrder
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderSuccessResponse, OrderErrorResponse
from app.services.order_service import OrderService
import logging

router = APIRouter(prefix="/api/orders", tags=["orders"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=OrderSuccessResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    提交訂單
    對應 Code.gs submitOrder (line 29-163)
    """
    try:
        # 1. 驗證餐點項目和價格（對應 Code.gs line 105-113）
        is_valid, error_msg = OrderService.validate_order_items(order.items)
        if not is_valid:
            logger.warning(f"訂單驗證失敗：{error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # 2. 驗證總金額（對應 Code.gs line 116-122）
        if not OrderService.validate_total_amount(order.items, order.totalAmount):
            logger.warning("訂單金額計算錯誤")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="訂單金額計算錯誤"
            )

        # 3. 建立訂單（對應 OrderService.gs saveOrder）
        db_order = OrderService.create_order(db, order)

        logger.info(f"訂單建立成功：{db_order.order_number}")

        # 4. 回傳成功訊息（對應 Code.gs line 139-143）
        return OrderSuccessResponse(
            success=True,
            message="喵～訂單已送出！",
            orderNumber=db_order.order_number
        )

    except HTTPException:
        raise
    except Exception as e:
        # 詳細的錯誤日誌（對應 Code.gs logError line 169-184）
        logger.error(f"建立訂單時發生錯誤：{str(e)}", exc_info=True)

        # 不要暴露詳細錯誤給用戶（對應 Code.gs line 159-162）
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統錯誤，請稍後再試"
        )


@router.get("/")
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """取得訂單列表"""
    orders = OrderService.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_number}")
async def get_order(
    order_number: str,
    db: Session = Depends(get_db)
):
    """根據訂單編號查詢訂單"""
    order = OrderService.get_order_by_number(db, order_number)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該訂單"
        )
    return order
