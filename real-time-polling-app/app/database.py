from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://root:Anandshukla12%40@127.0.0.1:3306/Move37"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Ensure the .env file is loaded if it exists
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()
    settings = Settings() # Reload settings after loading .env

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
