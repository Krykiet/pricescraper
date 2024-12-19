"""
TGeBase i średnioważone ceny godzinowe
URL:
https://www.tge.pl/energia-elektryczna-rdn-tge-base?date_start=2024-12-04&iframe=1
"""

from datetime import datetime, timedelta, date
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.models.tge_wahp import TgeWahpDataModel
from app.schemas.tge_wahp import TgeWahpDataSchema
from app.services.wahp_scraper import scrape_wahp

from fastapi.responses import JSONResponse
import json
from fastapi.encoders import jsonable_encoder

import logging

from app.database import db_dependency

router = APIRouter(prefix='/tge-wahp', tags=['tge-wahp-scraper'])

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NaNToNoneJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(jsonable_encoder(content, custom_encoder={float: lambda x: None if x != x else x}),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')

@router.get("/all", response_model=List[TgeWahpDataSchema])
async def get_all_tge_wahp(db: db_dependency):
    try:
        records = db.query(TgeWahpDataModel).all()
        return NaNToNoneJSONResponse(content=records)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")


@router.get("/last", response_model=List[TgeWahpDataSchema])
async def get_last_24_scraped_tge_wahp(db: db_dependency):
    try:
        records = db.query(TgeWahpDataModel).order_by(TgeWahpDataModel.date_scraped.desc()).limit(24).all()
        if records:
            return NaNToNoneJSONResponse(content=records)
        else:
            raise HTTPException(status_code=404, detail="No records found.")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")


@router.get("/by-date", response_model=List[TgeWahpDataSchema])
async def get_by_date(date: date, db: db_dependency):
    try:
        records = db.query(TgeWahpDataModel).filter(func.date(TgeWahpDataModel.date_scraped) == date).all()
        return NaNToNoneJSONResponse(content=records)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save", status_code=status.HTTP_201_CREATED)
async def create_tge_wahp(db: db_dependency):
    try:
        scraped_data = scrape_wahp()
        date_scraped = datetime.now()

        for row in scraped_data:
            wahp_data_model = TgeWahpDataModel(
                date_scraped=date_scraped,
                hour=row['datetime'],
                price=row['price_pln_mwh'],
                volume=row['volume_mwh']
            )
            db.add(wahp_data_model)

        db.commit()
        logger.info("TGE Wahp data saved successfully.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to save data to database.")
    except Exception as e:
        logger.error(f"Unknown error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unexpected error occurred.")

    return {"message": "Data successfully saved"}


@router.get("/check")
async def debug():
    logger.info("Check works")
    return {"works": "ok"}
