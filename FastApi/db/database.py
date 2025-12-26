import os
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # folder of this file
DB_FILE = os.path.join(BASE_DIR, "sqlite123.db")
DB_PATH = f"sqlite:///{DB_FILE}"

engine = create_engine(DB_PATH, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()