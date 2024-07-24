from contextlib import asynccontextmanager

import uvicorn

from typing import Union
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(
    api_router,
)


@app.get("/ping")
async def ping() -> dict:
    return {"Success": True}


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "Portfolio World"}


@app.get("/item/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
