from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    salt = Column(String)
    email = Column(String, unique=True)
    recipes = relationship("Recipe", back_populates="owner")
    ingredients = relationship("Ingredient", back_populates="owner")
    menus = relationship("Menu", back_populates="owner")
    shopping_lists = relationship("ShoppingList", back_populates="owner")