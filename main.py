from contextlib import asynccontextmanager

from fastapi import FastAPI

import redis_utils
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_utils.redis_init()
    yield
    await redis_utils.redis_close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
