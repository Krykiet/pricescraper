from fastapi import FastAPI

# Database
from app.database import engine
# Models
from app.models import models
from app.models.models import TgeRdnData
# Routers
from app.routers import scraper_router, tge_rdn_scraper_router

app = FastAPI()

# Prices.__table__.drop(engine)
# TgeRdnData.__table__.drop(engine)
models.Base.metadata.create_all(bind=engine)

# app.include_router(test.router)
app.include_router(scraper_router.router)
app.include_router(tge_rdn_scraper_router.router)
