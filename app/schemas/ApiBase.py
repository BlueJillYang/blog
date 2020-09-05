from pydantic import BaseModel


# Response 回复类
class BaseResponse(BaseModel):
    code: int
    msg: str


class TimeResponse(BaseResponse):
    time: str


class UrlResponse(BaseResponse):
    url: str


class UrlTimeResponse(TimeResponse):
    url: str


class PageResponse(BaseResponse):
    total: int = 0
    data: list = []


# Request 请求类
class PageRequest(BaseModel):
    page_num: int
    page_size: int





