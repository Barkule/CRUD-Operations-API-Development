from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="orders")
