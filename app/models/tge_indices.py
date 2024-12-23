from sqlalchemy import Column, Integer, Float, DateTime, String, func
from app.database import Base

class IndicesDataModel(Base):
    __tablename__ = 'tge_indices_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    index_name = Column(String)
    price = Column(Float)  # Stores the price in PLN/MWh
    volume = Column(Float)  # Stores the volume in MWh
