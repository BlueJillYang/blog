from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routers import contorller
from pony.orm import db_session

app = FastAPI()

# add static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def _enter_session():
    # print('加载DB_session && redis缓存')
    print('加载DB_session')
    # 缓存
    # rc = RedisCacheBackend('redis://redis')
    # caches.set(CACHE_KEY, rc)

    # 数据库db session
    session = db_session()
    Request.pony_session = session
    session.__enter__()


@app.on_event("shutdown")
async def _exit_session(exception):
    # print('释放DB_session && redis缓存释放')
    print('释放DB_session')
    # await close_caches()

    session = getattr(Request, 'pony_session', None)
    if session is not None:
        session.__exit__(exc=exception)


@app.get("/")
async def index():
    return {"msg": "Hello World"}


app.include_router(
    router=contorller,
    prefix="/api",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, port=8001, host="0.0.0.0")

