from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Order

#create user
async def create_user(db: AsyncSession, name: str, email: str):
    new_user = User(name=name, email=email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#get user
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

#update user
async def update_user(db: AsyncSession, user_id: int, name: str, email: str):
    user = await get_user(db, user_id)
    if user:
        user.name = name
        user.email = email
        await db.commit()
        await db.refresh(user)
    return user

#celete user
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user



#create Order
async def create_order(db: AsyncSession, user_id: int, product_name: str, quantity: int):
    #check if the user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None  # Return None if the user doesn't exist

    #create a new order
    new_order = Order(user_id=user_id, product_name=product_name, quantity=quantity)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

#get order
async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()

#update order
async def update_order(db: AsyncSession, order_id: int, user_id: int, product_name: str, quantity: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        order.user_id = user_id
        order.product_name = product_name
        order.quantity = quantity
        await db.commit()
        await db.refresh(order)
    return order

#delete order
async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if order:
        await db.delete(order)
        await db.commit()
    return order