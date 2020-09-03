from app.core.config import settings
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
import hashlib
import time

from fastapi import Header, HTTPException, Request
from pony.orm import commit
from app import schemas, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    now_secret = settings.SECRET_KEY
    # print("Create Token   now Secret = ", now_secret)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, now_secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "e6eee997821c54c661ab6f237fb3c71b":  # selenium_encode的md5
        raise HTTPException(status_code=400, detail="X-Token header invalid")

#
# async def api_verify_token(
#         request: Request,
#         form_data: ApiParamRequest
# ):
#     """
#     验证api权限
#     app_key: str, app_secret: str, timestamp: str, form_token: str
#     """
#     app_key = form_data.app_key
#     timestamp = form_data.timestamp
#     form_token = form_data.token  # 客户端传入的token
#
#     if not all([app_key, timestamp, form_token]):
#         raise HTTPException(status_code=401, detail="app_key invalid")
#     if not timestamp.isdigit():
#         raise HTTPException(status_code=401, detail="timestamp invalid")
#     if (int(timestamp) - int(time.time())) > 20:
#         raise HTTPException(status_code=401, detail="timestamp invalid")
#
#     with request.pony_session:
#         current_api_user = ApiUser.get(app_key=app_key)
#
#     if not current_api_user:
#         raise HTTPException(status_code=401, detail="no access")
#
#     app_secret = current_api_user.app_secret
#     if not app_secret:
#         raise HTTPException(status_code=401, detail="no access")
#
#     m = hashlib.md5()
#     token = app_key + "+" + str(timestamp) + "+" + app_secret
#     m.update(token.encode('utf-8'))
#     token = m.hexdigest()
#
#     limit_call_count = current_api_user.limit_call_count
#     if token != form_token:
#         raise HTTPException(status_code=401, detail="token invalid")
#     if limit_call_count <= 0:
#         raise HTTPException(status_code=401, detail="No available packet")
#     if current_api_user.status_code != 0:
#         raise HTTPException(status_code=401, detail="App is still under review")
#     if current_api_user.isDelete != 0:
#         raise HTTPException(status_code=401, detail="App Deleted")
#
#     # 判断是否过期
#     # current_api_user.expired_time为<class 'datetime.datetime'> 2021-06-24 12:03:13这种格式
#     # print(type(current_api_user.expired_time), current_api_user.expired_time)
#     if current_api_user.expired_time < datetime.now():
#         raise HTTPException(status_code=401, detail="App has expired")
#     else:
#         # 调用次数加1
#         current_api_user.call_count += 1
#         commit()
#         # return current_api_user


async def account_verify_password(request: Request, form_data: schemas.LoginForm):
    with request.pony_session:
        user_with_name = models.User.get(account_name=form_data.username)
        user_with_email = models.User.get(email=form_data.username)
    user = user_with_email or user_with_name
    if not user:
        raise HTTPException(status_code=409, detail="wrong username or password")

    m = hashlib.md5()
    final_pwd = user.hashed_password + "*/-sz"
    m.update(final_pwd.encode('utf-8'))
    final_pwd = m.hexdigest()

    if final_pwd == form_data.password:
        return form_data
    else:
        raise HTTPException(status_code=401, detail="wrong username or password")






