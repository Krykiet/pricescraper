from database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime


class Prices(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_scraped = Column(DateTime)
    list1_content = Column(String)
    list2_content = Column(String)
