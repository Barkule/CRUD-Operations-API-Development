from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/hushh"

#here is async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

#bsase class for declarative models
Base = declarative_base()