# General
from datetime import datetime
from typing import Annotated, Type, List

# App
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from starlette import status

# db
from app.database import SessionLocal
# models
from app.models.models import RDN, TgeRdnData, TgeRdnDataModel
# services
from app.services import scraper

router = APIRouter(prefix='/tge-rdn', tags=['tge-rdn-scraper'])

# JSON
from fastapi.responses import JSONResponse
import json
from fastapi.encoders import jsonable_encoder


class NaNToNoneJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(jsonable_encoder(content, custom_encoder={float: lambda x: None if x != x else x}),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')


# Get instance of db for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]  # Database dependency injection


@router.get("/tge-rdn", response_model=List[TgeRdnDataModel])
async def get_all_tge_rdn(db: db_dependency):
    try:
        records = db.query(TgeRdnData).all()
        return NaNToNoneJSONResponse(content=records)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")


@router.get("/tge-rdn/last", response_model=TgeRdnDataModel)
async def get_last_24_scraped_tge_rdn(db: db_dependency):
    try:
        # Order by date_scraped descending to get the most recent records first
        # and limit the results to the last 24 records
        records = db.query(TgeRdnData).order_by(TgeRdnData.date_scraped.desc()).limit(24).all()

        # Reverse the records to have them in ascending order by date_scraped
        records = list(reversed(records))

        if records:
            return NaNToNoneJSONResponse(content=records)
        else:
            raise HTTPException(status_code=404, detail="No records found.")
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")


@router.post("/tge-rdn", status_code=status.HTTP_201_CREATED)
async def create_tge_rdn(db: db_dependency):
    try:
        scraped_data = scraper.ScrapedData()

        for hour in range(24):
            rdn_data_model = TgeRdnData()
            print(f'Processing hour: {hour}')

            rdn_data_model.date_scraped = datetime.now()
            rdn_data_model.hour = hour
            rdn_data_model.f1_price = scraped_data.f1_price[hour] if hour < len(scraped_data.f1_price) else None
            rdn_data_model.f1_volume = scraped_data.f1_volume[hour] if hour < len(scraped_data.f1_volume) else None
            rdn_data_model.f2_price = scraped_data.f2_price[hour] if hour < len(scraped_data.f2_price) else None
            rdn_data_model.f2_volume = scraped_data.f2_volume[hour] if hour < len(scraped_data.f2_volume) else None
            rdn_data_model.cont_price = scraped_data.cont_price[hour] if hour < len(scraped_data.cont_price) else None
            rdn_data_model.cont_volume = scraped_data.cont_volume[hour] if hour < len(
                scraped_data.cont_volume) else None

            db.add(rdn_data_model)

        db.commit()
        print('Data for all hours committed successfully')
    except SQLAlchemyError as e:
        # Rollback in case of error
        db.rollback()
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to save data to database.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unexpected error occurred.")

    return {"message": "Data successfully saved"}
