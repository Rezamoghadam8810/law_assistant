from fastapi import FastAPI
from app.core.config import settings
from app.db.session import ping_db
from app.routers import user, auth
from app.routers import clients


app = FastAPI(title=settings.app_name)

# include routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(clients.router)



@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.environment,
        "app": settings.app_name
    }

@app.get("/db-check")
def db_check():
    ok = ping_db()
    return {"db_ok": ok}
