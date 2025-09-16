from fastapi import FastAPI
from app.core.config import settings
from app.db.session import ping_db

app = FastAPI(title=settings.app_name)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.environment,
        "app": settings.app_name
    }

@app.get("/db-check")
def db_check():
    ok=ping_db()
    return {"db_ok": ok}