"""
Cat Claws 貓咪食堂 - FastAPI 主程式
對應 Code.gs 的 Web App 功能
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import orders, menu, analytics
from app.config import get_settings
from app.database import engine, Base
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 取得設定
settings = get_settings()

# 建立資料表
Base.metadata.create_all(bind=engine)

# 建立 FastAPI 應用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="可愛的貓咪主題訂餐系統 🐾",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板引擎
templates = Jinja2Templates(directory="templates")

# 註冊路由
app.include_router(orders.router)
app.include_router(menu.router)
app.include_router(analytics.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    首頁
    對應 Code.gs doGet (line 9-15)
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "🐾 Cat Claws 貓咪食堂"}
    )


@app.get("/analytics", response_class=HTMLResponse)
async def analytics_dashboard(request: Request):
    """分析報表後台頁面"""
    return templates.TemplateResponse(
        "analytics.html",
        {"request": request}
    )


@app.get("/favicon.ico")
async def favicon():
    """Favicon 圖示（避免 404 錯誤）"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/350/cat-face_1f431.png"
    )


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.get("/api")
async def api_info():
    """API 資訊"""
    return {
        "message": "歡迎使用 Cat Claws 貓咪食堂 API",
        "version": settings.app_version,
        "docs": "/api/docs",
        "dashboard": "/analytics",
        "endpoints": {
            "menu": "/api/menu",
            "orders": "/api/orders",
            "analytics": "/api/analytics"
        }
    }


# 啟動事件
@app.on_event("startup")
async def startup_event():
    logger.info(f"🐱 {settings.app_name} v{settings.app_version} 啟動中...")
    logger.info("資料庫連線已建立")


# 關閉事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("應用程式關閉中...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
