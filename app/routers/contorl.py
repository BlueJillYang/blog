from fastapi import APIRouter
from app.routers import upload


contorller = APIRouter()

# upload images or files. file tpye: jpg, png, gif, zip, rar, etc....
contorller.include_router(
    upload.router,
    tags=["upload"],
    prefix="/upload"
)


