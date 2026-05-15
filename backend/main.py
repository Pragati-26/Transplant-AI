from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from .database import Base, engine
from .routers import auth, match, history

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TransplantAI",
    description="AI-powered kidney donor-patient matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "code": "INTERNAL_ERROR"}
    )

# ── All API routes MUST be registered before the static mount ──
app.include_router(auth.router)
app.include_router(match.router)
app.include_router(history.router)

@app.get("/health")
def health():
    return {"status": "ok"}

# ── Static files mount LAST — only if frontend folder exists ──
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")