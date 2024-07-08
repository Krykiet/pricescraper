from typing import Optional

from sqlalchemy import Column, Integer, Float, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base

from datetime import datetime

from pydantic import BaseModel


class RDN(Base):
    __tablename__ = 'rdn'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    f1_price = Column(ARRAY(Float))
    f1_volume = Column(ARRAY(Float))
    f2_price = Column(ARRAY(Float))
    f2_volume = Column(ARRAY(Float))
    cont_price = Column(ARRAY(Float))
    cont_volume = Column(ARRAY(Float))


class TgeRdnData(Base):
    __tablename__ = 'tge_rdn_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    hour = Column(Integer)
    f1_price = Column(Float)
    f1_volume = Column(Float)
    f2_price = Column(Float)
    f2_volume = Column(Float)
    cont_price = Column(Float, nullable=True)
    cont_volume = Column(Float, nullable=True)


class TgeRdnDataModel(BaseModel):
    id: int
    date_scraped: datetime
    hour: int
    f1_price: float
    f1_volume: float
    f2_price: float
    f2_volume: float
    cont_price: Optional[float] = None  # Make these fields optional to handle nulls
    cont_volume: Optional[float] = None

    class Config:
        orm_mode = True
