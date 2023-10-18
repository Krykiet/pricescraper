# General
from datetime import datetime
from typing import Annotated, Type, List

# App
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

# db
from app.database import SessionLocal
# models
from app.models.models import RDN
# services
from app.services import scraper

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


class RDNRequest(BaseModel):
    date_scraped: datetime
    f1_price: list
    f1_volume: list
    f2_price: list
    f2_volume: list
    cont_price: list
    cont_volume: list


# Convert ARRAY(Float) to string
def convert_properties_to_str(obj: Type[RDN]):
    return {'id': obj.id,
            'date': str(obj.date_scraped),
            'f1_price': str(obj.f1_price),
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


@router.get("/wakeup", status_code=status.HTTP_200_OK)
async def get_all_rdn(db: db_dependency):
    return 'wakeup'


@router.post("/rdn", status_code=status.HTTP_201_CREATED)
async def create_rdn(db: db_dependency):
    rdn_data_model = RDN()
    print('Post request')

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


@router.delete("/rdn", status_code=200)
async def clear_rdns(db: db_dependency):
    ids = [1, 8, 37, 58, 89]
    try:
        # your logic here
        rows_deleted = db.query(RDN).filter(~RDN.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return {"detail": f"{rows_deleted} rows deleted."}
    except Exception as e:
        # db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.delete("/rdn/{rdn_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rdn(db: db_dependency,
                     rdn_id: int):
    rdn_model = db.query(RDN).filter(RDN.id == rdn_id).first()
    if rdn_model is None:
        raise HTTPException(status_code=404, detail='No RDN of this id')
    db.query(RDN).filter(RDN.id == rdn_id).delete()
    db.commit()


@router.delete("/rdn/tobedeleted/")
async def show_rdns_to_be_deleted(db: db_dependency, ids: List[int]):
    rdns_to_be_deleted = db.query(RDN).filter(~RDN.id.in_(ids))
    return [convert_properties_to_str(obj) for obj in rdns_to_be_deleted]



