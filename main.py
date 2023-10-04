from fastapi import FastAPI

# Models
import models
import test

# Database
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(test.router)