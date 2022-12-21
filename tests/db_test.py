from fastapi.testclient import TestClient
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from twitter_app.app import app
from twitter_app.database import Base, get_session

test_db_url = "postgresql+asyncpg:///./test.db"
engine = create_async_engine(test_db_url, echo=True)
TestingSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# session = async_session()

async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all(bind=engine))


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

client = TestClient(app)
