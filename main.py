from fastapi import FastAPI

# Models
import models
from models import Prices, RDN
import test

# Database
from database import engine

# Routers
from routers import scraper_router

app = FastAPI()

# Prices.__table__.drop(engine)
# RDN.__table__.drop(engine)
models.Base.metadata.create_all(bind=engine)

# app.include_router(test.router)
app.include_router(scraper_router.router)