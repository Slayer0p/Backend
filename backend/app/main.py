from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routes import resume, roadmap, interview, tracker

# -------------------------
# DB init
# -------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Career Companion")

# -------------------------
# CORS CONFIG
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# 🔥 FIX: Validation Error Handler
# -------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    # Prevent FastAPI from trying to JSON-encode raw bytes (PDF)
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid request format. Check file upload or payload."
        },
    )

# -------------------------
# Routers
# -------------------------
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(interview.router)
app.include_router(tracker.router)

# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "AI Career Companion Backend Running 🚀"}
