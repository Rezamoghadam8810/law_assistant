from fastapi import FastAPI
from app.core.config import settings
from app.db.session import ping_db
from app.routers import user


app =FastAPI(title=settings.app_name)
app.include_router(user.router)

@app.get("/health")
def health():
    return {
        "status":"ok",
        "env":settings.environment,
        "app":settings.app_name
    }

@app.get("/db-check")
def db_check():
    ok=ping_db()
    return {"db_ok": ok}








# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# def root():
#     return {"msg": "Hello, Law Assistant is running!"}
