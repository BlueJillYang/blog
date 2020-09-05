from fastapi import APIRouter
from app.routers import upload, file


contorller = APIRouter()

# upload images or files. file tpye: jpg, png, gif, zip, rar, etc....
contorller.include_router(
    upload.router,
    tags=["upload"],
    prefix="/upload"
)


contorller.include_router(
    file.router,
    tags=["file"],
    prefix="/file"
)


