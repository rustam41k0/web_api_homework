from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event

DATABASE_URL = 'postgresql://default:X6CaL40fHeFHsmiAzhqtJuXKf930wnzf@dpg-cm18f9mn7f5s73e5avt0-a.oregon-postgres.render.com/homework_o2iz'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()
