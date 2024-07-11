from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique= True)
    password = Column(String)
    salt = Column(String)
    email = Column(String, unique=True)
    recipes = relationship("Recipe", back_populates="owner")