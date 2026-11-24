# REST: FastAPI, JSON over HTTP/1.1. Run by run.py with uvicorn, access log off.
from fastapi import FastAPI
from pydantic import BaseModel

from order_data import make_order


class Item(BaseModel):
    name: str
    qty: int
    price_cents: int


class Order(BaseModel):
    id: int
    customer: str
    items: list[Item]
    total_cents: int


app = FastAPI()
_cache: dict[tuple[int, int], Order] = {}  # built once, so calls measure serving, not building


@app.get("/orders/{order_id}")
async def get_order(order_id: int, items: int = 2) -> Order:  # return type: Pydantic writes the JSON
    key = (order_id, items)
    if key not in _cache:
        _cache[key] = Order(**make_order(*key))
    return _cache[key]
