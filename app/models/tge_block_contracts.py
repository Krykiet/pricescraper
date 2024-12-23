from sqlalchemy import Column, Integer, Float, String, DateTime, func
from app.database import Base

class BlockContractsModel(Base):
    __tablename__ = 'block_contracts_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime, default=func.now())
    contract_name = Column(String, index=True)  # Name of the contract
    min_price = Column(Float)  # Minimum price
    max_price = Column(Float)  # Maximum price
    volume = Column(Float)  # Volume