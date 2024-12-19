from sqlalchemy import Column, Integer, Float, DateTime, func

from app.database import Base

class TgeWahpDataModel(Base):
    __tablename__ = 'tge_wahp_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    hour = Column(DateTime)
    price = Column(Float)
    volume = Column(Float)
