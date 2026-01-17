from fastapi import FastAPI
from app.routers import orders

app = FastAPI(title="My Shop API")

app.include_router(orders.router, prefix="/orders", tags=["orders"])