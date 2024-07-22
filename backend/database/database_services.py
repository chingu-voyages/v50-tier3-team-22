
from database.database import engine, SessionLocal, Base

from database.models.user import User
from database.models.recipe import Recipe
#import order to keep relationship in database

def start_database():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()