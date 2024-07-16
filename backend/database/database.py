from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_URL}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    def dict(self):
        """"Generates a dictionary that is not tied to the modell therefore can be freely changed"""
        dictionary = {}
        for key, value in self.__dict__.items():
            dictionary[key] = value

        return dictionary
