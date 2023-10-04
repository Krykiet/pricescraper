# General
from datetime import datetime
from typing import Annotated

# App
from fastapi import APIRouter, Depends

# db
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

# models
from models import Prices
from pydantic import BaseModel, Field

router = APIRouter(prefix='/test', tags=['test'])


# Get instance of db for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]  # Database dependency injection


class TestRequest(BaseModel):
    date_scraped: datetime
    list1_content: str = Field(min_length=1)
    list2_content: str = Field(min_length=1)


@router.get("/")
async def get_anything(db: db_dependency):
    return db.query(Prices).all()


@router.post("/test", status_code=status.HTTP_201_CREATED)
async def post_something(db: db_dependency,
                         test_request: TestRequest):
    test_model = Prices(**test_request.model_dump())
    db.add(test_model)
    db.commit()

