from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import auth, workflows, ai

app = FastAPI(
    title="m8m API",
    description="Open source automation and workflow platform powered by Vercel AI SDK",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "m8m-backend", "features": ["workflows", "ai"]}
