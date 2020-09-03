from typing import Generator

from fastapi import Depends, HTTPException, status, Request, Query, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.core.config import settings


def get_current_user_with_query_param(
        request: Request,
        token: str = Query(...)
) -> models.User:
    now_secret = settings.SECRET_KEY
    # print("get_current_user_with_query_param   now Secret = ", now_secret)
    try:
        payload = jwt.decode(
            token, now_secret, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    with request.pony_session:
        user = models.User.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.to_dict()
    roles = user_dict.get("roles", "")
    user_dict["roles"] = [roles]
    return user_dict


def get_current_user(
        request: Request,
        X_Token: str = Header(...)
) -> models.User:
    token = X_Token
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    with request.pony_session:
        user = models.User.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # print(f"model.users={user.to_dict()}")
    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.is_active == 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.is_superuser != 1:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


