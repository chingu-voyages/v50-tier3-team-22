from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from database.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image_name = Column(String, unique=True)
    description = Column(String)
    cuisine = Column(String)
    category = Column(Integer)
    time = Column(Integer)
    level = Column(Integer)
    is_favourite = Column(Boolean, default=False)
    ingredients = Column(JSON, default=[])
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="recipes")
