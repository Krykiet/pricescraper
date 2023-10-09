from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# postgresql://postgres:password@host_name/server_name
SQLALCHEMY_DATABASE_URL = 'postgresql://kd:7NdBbDivarbjDRR3eVBOExpIP8y63uev@dpg-ckekncma3ovc73dd62pg-a.frankfurt' \
                          '-postgres.render.com/prices_kvue'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})  # this is for sqlite only
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
