from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import agent
from app.db.session import engine, Base
from app.db.seed import seed_data
from app.core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute startup logic
    Base.metadata.create_all(bind=engine)
    try:
        seed_data()
    except Exception as e:
        print(f"Error seeding data: {e}")
    yield
    # Shutdown logic if any

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router, prefix="/api/agent", tags=["agent"])

@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
