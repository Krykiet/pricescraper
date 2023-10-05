# General
from datetime import datetime
from typing import Annotated

# App
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import text

import models
# db
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

# models
from models import Prices
from pydantic import BaseModel, Field

# scraper
from scraper import scraper

router = APIRouter(prefix='/scraper', tags=['scraper'])


# Get instance of db for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]  # Database dependency injection


class PricesDataRequest(BaseModel):
    date_scraped: datetime
    list1_content: str = Field(min_length=1)
    list2_content: str = Field(min_length=1)


@router.get("/price")
async def get_anything(db: db_dependency):
    return db.query(Prices).all()


@router.get("/scrape", status_code=status.HTTP_200_OK)
async def scrape():
    return scraper.get_prices()


@router.post("/price", status_code=status.HTTP_201_CREATED)
async def post_something(db: db_dependency,
                         test_request: PricesDataRequest):
    prices_data_model = Prices(**test_request.model_dump())

    # Scrape data
    list1, list2 = scraper.get_prices()
    # Date
    prices_data_model.date_scraped = datetime.now()

    prices_data_model.list1_content = str(list1)

    prices_data_model.list2_content = str(list2)

    db.add(prices_data_model)
    db.commit()


@router.delete("/price/clear_base", status_code=status.HTTP_204_NO_CONTENT)
async def clear_base(db: db_dependency):
    db.query(Prices).delete()

    # Reset indexes
    sequence_name = "prices_id_seq"
    db.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))
    db.commit()


@router.delete("/price/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(db: db_dependency,
                       price_id: int = Path(gt=0)):
    print(scraper.SCRAPER_MESSAGE)

    price_model = db.query(Prices).filter(Prices.id == price_id).first()

    if price_model is None:
        raise HTTPException(status_code=401, detail='No such record to delete')

    db.query(Prices).filter(Prices.id == price_id).delete()
    db.commit()
