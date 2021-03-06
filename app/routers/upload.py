from fastapi import APIRouter, File, UploadFile, Request
from typing import List
import os
import time
from app import schemas, models
from hashlib import md5
from pony import orm
from app.core.config import env_api


router = APIRouter()


@router.post("/image", response_model=schemas.UrlTimeResponse)
async def upload_image(
        request: Request,
        file: UploadFile = File(...)
):
    """
    upload image(jpg/jpeg/png/gif) to server and store locally
    :return: upload result
    """

    save_file_path = os.path.join(os.getcwd().split("app")[0], r"app/static/images")
    # pic_uuid = str(uuid.uuid4())
    file_name = file.filename
    endfix = file_name.rpartition(".")[-1]

    try:
        content = await file.read()

        # 对文件进行MD5校验 重复的无需再写
        md5_vercation = md5(content)
        md5_hash = md5_vercation.hexdigest()
        file_url = f'/{env_api}/api/file/image/{md5_hash}'
        file_path = os.path.join(save_file_path, f"{md5_hash}.{endfix}")

        with request.pony_session:
            file_obj = models.Upload.get(md5_hash=md5_hash)

            if file_obj:
                file_obj.file_path = file_path
                file_obj.file_url = file_url
                if not os.path.exists(file_path):  # 判断如果不存在路径 需要重新写入
                    with open(file_path, "wb") as f:
                        f.write(content)
                orm.commit()
                # 说明已经写入过该文件了
                return {"code": 20000, "msg": "Success, file info updated", "time": time.strftime('%Y-%m-%d %H:%M:%S'), "url": file_url}

            # 文件属性
            file_dict = {
                "file_name": file_name,
                "file_path": file_path,
                "md5_hash": md5_hash,
                "file_url": file_url,
                "note": "image"
            }
            models.Upload(**file_dict)
            orm.commit()

        with open(file_path, "wb") as f:
            print("写入路径", file_path)
            f.write(content)
        return {"code": 20000, "msg": "Success", "time": time.strftime('%Y-%m-%d %H:%M:%S'), "url": file_url}
    except Exception as e:
        return {"code": 50000, "msg": str(e), "time": time.strftime('%Y-%m-%d %H:%M:%S'), "url": ""}


@router.post("/files")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}




