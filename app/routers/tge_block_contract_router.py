from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from typing import List
from datetime import datetime, date
import json

from app.models.tge_block_contracts import BlockContractsModel
from app.schemas.tge_block_contracts import BlockContractsSchema
from app.services.block_contracts_scraper import BlockContractsScraper
from app.database import db_dependency
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import logging

router = APIRouter(prefix='/block-contracts', tags=['block-contracts-scraper'])

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NaNToNoneJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(jsonable_encoder(content, custom_encoder={float: lambda x: None if x != x else x}),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')

@router.get("/all", response_model=List[BlockContractsSchema])
async def get_all_block_contracts_data(db: db_dependency):
    try:
        records = db.query(BlockContractsModel).all()
        return NaNToNoneJSONResponse(content=records)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")

@router.get("/last", response_model=List[BlockContractsSchema])
async def get_last_scraped_block_contracts(db: db_dependency):
    try:
        records = db.query(BlockContractsModel).order_by(BlockContractsModel.date_scraped.desc()).limit(24).all()
        if records:
            return NaNToNoneJSONResponse(content=records)
        else:
            raise HTTPException(status_code=404, detail="No records found.")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to retrieve data.")

@router.get("/by-date", response_model=List[BlockContractsSchema])
async def get_block_contracts_by_date(date: date, db: db_dependency):
    try:
        records = db.query(BlockContractsModel).filter(func.date(BlockContractsModel.date_scraped) == date).all()
        return NaNToNoneJSONResponse(content=records)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", status_code=201)
async def save_block_contracts_data(db: db_dependency):
    try:
        scraper = BlockContractsScraper()
        scraped_data = scraper.block_contracts
        date_scraped = datetime.now()

        for row in scraped_data:
            block_contract = BlockContractsModel(
                date_scraped=date_scraped,
                contract_name=row['contract_name'],
                min_price=row['min_price'],
                max_price=row['max_price'],
                volume=row['volume']
            )
            db.add(block_contract)

        db.commit()
        logger.info("Block contracts data saved successfully.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to save data to database.")
    except Exception as e:
        logger.error(f"Unknown error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unexpected error occurred.")

    return {"message": "Block contracts data successfully saved"}

@router.get("/check")
async def debug():
    logger.info("Check works")
    return {"works": "ok"}
