from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    msg: str


class TimeResponse(BaseResponse):
    time: str
