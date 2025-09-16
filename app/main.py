from fastapi import FastAPI

app = FastAPI(title="Law Assistant")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Law Assistant is running 🚀"
    }
