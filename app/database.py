from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Config
from app.config import get_config

config = get_config()
# SQLALCHEMY_DATABASE_URL_LOCAL = 'sqlite:///./todosapp.db'
# postgresql://postgres:password@host_name/server_name
if config.local:

    SQLALCHEMY_DATABASE_URL = 'postgresql://kd:7NdBbDivarbjDRR3eVBOExpIP8y63uev@dpg-ckekncma3ovc73dd62pg-a.frankfurt' \
                          '-postgres.render.com/prices_kvue'
else:
    SQLALCHEMY_DATABASE_URL = 'postgresql://kd:7NdBbDivarbjDRR3eVBOExpIP8y63uev@dpg-ckekncma3ovc73dd62pg-a/prices_kvue'

# engine = create_engine(SQLALCHEMY_DATABASE_URL_LOCAL, connect_args={'check_same_thread': False})  # this is for
# sqlite only
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
