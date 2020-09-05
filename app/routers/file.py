from fastapi import APIRouter, Request, Body
from fastapi.responses import FileResponse
from app import models, schemas
from app.core.config import env_api


router = APIRouter()


@router.post("/images", response_model=schemas.PageResponse)
async def get_images_list(
        request: Request,
        page: schemas.PageRequest,
):
    """
    According to params to get images list
    :param request: pony ORM
    :param page: page_num page_size To decide how many images return
    :return: List[image_url]
    """
    with request.pony_session:
        images_list = models.Upload.select(lambda file: file.note == "image")
        images_size = len(images_list)

        page_num = page.page_num
        page_size = page.page_size
        # page_num = 1  # page.page_num
        # page_size = 10  # page.page_size

        start_index = (page_num-1) * page_size
        end_index = page_num * page_size

        if images_size <= start_index:
            return {"code": 40001, "msg": "未查询到相关数据", "total": 0, "data": []}
        if images_size <= end_index:
            images = images_list[start_index:]  # 从start_index到最后
        else:
            images = images_list[start_index: end_index]

        images_data = [i.file_url.replace("dev-api", env_api) for i in images]

        return {"code": 20000, "msg": "查询成功", "total": images_size, "data": images_data}


@router.get("/image/{md5_hash}")
async def get_image_file(
        request: Request,
        md5_hash: str,
):
    with request.pony_session:
        image_file = models.Upload.get(md5_hash=md5_hash)

        if not image_file:
            return schemas.BaseResponse(code=40004, msg="未找到对应文件")

        file_path = image_file.file_path
        return FileResponse(file_path, media_type="image/png")

