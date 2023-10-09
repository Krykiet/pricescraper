# General
from datetime import datetime
from typing import Annotated, List

# App
from fastapi import APIRouter, Depends, Path, HTTPException
from numpy import isnan
from sqlalchemy import text

# db
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

# models
from models import Prices, RDN
from pydantic import BaseModel, Field

# scraper
from scraper import scraper

router = APIRouter(prefix='/scraper', tags=['scraper'])

scraped_data = scraper.ScrapedData()


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


class RDNRequest(BaseModel):
    date_scraped: datetime
    f1_price: list
    f1_volume: list
    f2_price: list
    f2_volume: list
    cont_price: list
    cont_volume: list


@router.get("/price")
async def get_anything(db: db_dependency):
    return db.query(Prices).all()


@router.post("/price", status_code=status.HTTP_201_CREATED)
async def post_something(db: db_dependency,
                         test_request: PricesDataRequest):
    prices_data_model = Prices(**test_request.model_dump())

    # Scrape data
    list1, list2 = scraper.get_prices()
    # Date
    prices_data_model.date_scraped = datetime.now()
    print(prices_data_model.date_scraped)

    prices_data_model.list1_content = str(list1)

    prices_data_model.list2_content = str(list2)

    db.add(prices_data_model)
    db.commit()


# Convert ARRAY(Float) to string
def convert_properties_to_str(obj: RDN):
    return {'f1_price': str(obj.f1_price),
            'f1_volume': str(obj.f1_volume),
            'f2_price': str(obj.f2_price),
            'f2_volume': str(obj.f2_volume),
            'cont_price': str(obj.cont_price),
            'cont_volume': str(obj.cont_volume)}


# RDN
@router.get("/rdn", status_code=status.HTTP_200_OK)
async def get_all_rdn(db: db_dependency):
    rdn_data = db.query(RDN).all()
    return [convert_properties_to_str(obj) for obj in rdn_data]


@router.post("/rdn", status_code=status.HTTP_201_CREATED)
async def create_rdn(db: db_dependency,
                     rdn_request: RDNRequest):
    rdn_data_model = RDN(**rdn_request.model_dump())

    # Pass data
    rdn_data_model.date_scraped = datetime.now()
    rdn_data_model.f1_price = scraped_data.f1_price
    rdn_data_model.f1_volume = scraped_data.f1_volume
    rdn_data_model.f2_price = scraped_data.f2_price
    rdn_data_model.f2_volume = scraped_data.f2_volume
    rdn_data_model.cont_price = scraped_data.cont_price
    rdn_data_model.cont_volume = scraped_data.cont_volume

    db.add(rdn_data_model)
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
