from sqlalchemy import Column, Integer, Float, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


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

