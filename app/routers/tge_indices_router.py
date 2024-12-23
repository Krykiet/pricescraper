from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from typing import List
from datetime import datetime, date
import json

from app.models.tge_indices import IndicesDataModel
from app.schemas.tge_indices import IndicesDataSchema
from app.services.tge_indices_scraper import ExtendedScrapedData
from app.database import db_dependency
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import logging

router = APIRouter(prefix='/indices', tags=['indices-scraper'])

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NaNToNoneJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(jsonable_encoder(content, custom_encoder={float: lambda x: None if x != x else x}),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')

@router.get("/all", response_model=List[IndicesDataSchema])
async def get_all_indices_data(db: db_dependency):
    try:
        records = db.query(IndicesDataModel).all()
        return NaNToNoneJSONResponse(content=records)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")

@router.get("/last", response_model=List[IndicesDataSchema])
async def get_last_scraped_indices(db: db_dependency):
    try:
        records = db.query(IndicesDataModel).order_by(IndicesDataModel.date_scraped.desc()).limit(24).all()
        if records:
            return NaNToNoneJSONResponse(content=records)
        else:
            raise HTTPException(status_code=404, detail="No records found.")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")

@router.get("/by-date", response_model=List[IndicesDataSchema])
async def get_by_date(date: date, db: db_dependency):
    try:
        records = db.query(IndicesDataModel).filter(func.date(IndicesDataModel.date_scraped) == date).all()
        return NaNToNoneJSONResponse(content=records)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", status_code=status.HTTP_201_CREATED)
async def save_indices_data(db: db_dependency):
    try:
        scraped_data = ExtendedScrapedData().indices
        date_scraped = datetime.now()

        for row in scraped_data:
            indices_data_model = IndicesDataModel(
                date_scraped=date_scraped,
                index_name=row['index_name'],
                price=row['price_pln_mwh'],
                volume=row['volume_mwh']
            )
            db.add(indices_data_model)

        db.commit()
        logger.info("Indices data saved successfully.")
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