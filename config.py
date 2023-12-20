from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event

DATABASE_URL = 'postgresql://postgres:root@localhost:5432/homework'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()
