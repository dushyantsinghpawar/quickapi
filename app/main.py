from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, items, ml

app = FastAPI(title="Quick API (Prod-Ready Starter)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(ml.router)
