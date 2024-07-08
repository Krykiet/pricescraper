from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Config
from app.config import get_config

config = get_config()
# SQLALCHEMY_DATABASE_URL_LOCAL = 'sqlite:///./todosapp.db'
if config.local:
    DB_URL = os.getenv('DB_URL')
elif config.prod:
    DB_URL = os.getenv('DB_URL')
else:
    DB_URL = os.getenv('DB_URL')

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
