from pydantic import BaseModel

from datetime import datetime

class IndicesDataSchema(BaseModel):
    id: int  # ID of the record
    date_scraped: datetime  # When the data was scraped
    index_name: str  # Name of the index
    price: float  # Price in PLN/MWh
    volume: float  # Volume in MWh

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models