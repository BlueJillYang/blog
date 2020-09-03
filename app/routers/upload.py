from fastapi import APIRouter, File, UploadFile, Request
from typing import List
import os
import time
from app import schemas, models
from hashlib import md5
from pony import orm


router = APIRouter()


@router.post("/image", response_model=schemas.TimeResponse)
async def upload_image(
        request: Request,
        file: UploadFile = File(...)
):
    """
    upload image(jpg/jpeg/png/gif) to server and store locally
    :return: upload result
    """

    save_file_path = os.path.join(os.getcwd(), r"app/static/images")
    # pic_uuid = str(uuid.uuid4())
    # endfix = file.filename.rpartition(".")[-1]
    file_name = file.filename
    file_path = os.path.join(save_file_path, file_name)

    try:
        content = await file.read()

        # 对文件进行MD5校验 重复的无需再写
        md5_vercation = md5(content)
        md5_hash = md5_vercation.hexdigest()

        with request.pony_session:
            file_obj = models.Upload.get(md5_hash=md5_hash)

            if file_obj:
                # 说明已经写入过该文件了
                return {"code": 201, "msg": "Success, File already exists", "time": time.strftime('%Y-%m-%d %H:%M:%S')}

            # 文件属性
            file_dict = {
                "file_name": file_name,
                "file_path": file_path,
                "md5_hash": md5_hash,
                "note": ""
            }
            models.Upload(**file_dict)
            orm.commit()

        with open(file_path, "wb") as f:
            f.write(content)
        return {"code": 200, "msg": "Success", "time": time.strftime('%Y-%m-%d %H:%M:%S')}
    except Exception as e:
        return {"code": 500, "msg": str(e), "time": time.strftime('%Y-%m-%d %H:%M:%S')}


@router.post("/files")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}




