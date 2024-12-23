from pydantic import BaseModel
from datetime import datetime

class BlockContractsSchema(BaseModel):
    id: int  # ID of the record
    date_scraped: datetime  # Date when the data was scraped
    contract_name: str  # Name of the contract
    min_price: float | None  # Minimum price (nullable)
    max_price: float | None  # Maximum price (nullable)
    volume: float | None  # Volume (nullable)

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models
