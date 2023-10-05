from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY


class Prices(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    list1_content = Column(String)
    list2_content = Column(String)


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

