import asyncio
from sqlalchemy import text
from app.db.session import SessionLocal

async def test_connection():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        print("✅ Database connected! Result =", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
