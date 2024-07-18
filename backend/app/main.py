from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping() -> dict:
    return {"Success": True}


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "Portfolio World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    return {"item_id": item_id, "q": q}
