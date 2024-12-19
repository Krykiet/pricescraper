from fastapi import FastAPI

# Database
from app.database import engine

# Models
from app.database import Base

# Routers
from app.routers import tge_rdn_scraper_router, wahp_scraper_router
from app.scheduler import start_scheduler

import os

API_ROOT_PATH = os.getenv("API_ROOT_PATH", "")

app = FastAPI(root_path=API_ROOT_PATH)

@app.on_event("startup")
async def on_startup():
    start_scheduler()

Base.metadata.create_all(bind=engine)

app.include_router(tge_rdn_scraper_router.router)
app.include_router(wahp_scraper_router.router)
