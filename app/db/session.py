from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
# from app.db.base import Base

engine= create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# وابستگی برای گرفتن Session
def get_db():
    db = SessionLocal()
    try:
        yield db   # 👈 حتماً yield (نه return)
    finally:
        db.close()




def ping_db() -> bool:

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

