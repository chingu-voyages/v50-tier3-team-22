from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    guide = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("user", back_populates="recipes")
