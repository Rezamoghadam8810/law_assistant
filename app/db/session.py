from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ساختن موتور اتصال به دیتابیس
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Session = مثل شلنگ برای دسترسی به آب دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def ping_db() -> bool:
    """یک تست ساده برای اینکه ببینیم دیتابیس روشنه یا نه"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
