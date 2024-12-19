from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TgeRdnDataSchema(BaseModel):
    id: int
    date_scraped: datetime
    hour: datetime
    f1_price: float
    f1_volume: float
    f2_price: float
    f2_volume: float
    cont_price: Optional[float] = None  # Make these fields optional to handle nulls
    cont_volume: Optional[float] = None

    class Config:
        orm_mode = True