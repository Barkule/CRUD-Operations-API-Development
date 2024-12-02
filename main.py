from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, engine
from models import Base
import crud

app = FastAPI()

#create the database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session

#user endpoints
@app.post("/users/")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, name, email)

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return user

@app.put("/users/{user_id}")
async def update_user(user_id: int , name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = await crud.update_user(db, user_id, name, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return {"detail": "User  deleted"}

#create order
@app.post("/orders/")
async def create_order(user_id: int, product_name: str, quantity: int, db: AsyncSession = Depends(get_db)):
    order = await crud.create_order(db, user_id, product_name, quantity)
    if not order:
        raise HTTPException(status_code=404, detail="User not found")
    return order

#read order
@app.get("/orders/{order_id}")
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#update order
@app.put("/orders/{order_id}")
async def update_order(order_id: int, user_id: int, product_name: str, quantity: int, db: AsyncSession = Depends(get_db)):
    order = await crud.update_order(db, order_id, user_id, product_name, quantity)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#delete order
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}
