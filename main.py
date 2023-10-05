from fastapi import FastAPI

# Models
import models
import test

# Database
from database import engine

# Routers
from routers import scraper_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# app.include_router(test.router)
app.include_router(scraper_router.router)