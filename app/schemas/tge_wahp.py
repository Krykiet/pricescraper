from pydantic import BaseModel

from datetime import datetime

class TgeWahpDataSchema(BaseModel):
    id: int
    date_scraped: datetime
    hour: datetime
    price: float
    volume: float