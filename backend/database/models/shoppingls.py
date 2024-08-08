from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime)
    menu_id = Column(Integer)
    items = relationship("Item", back_populates="shopping_list")
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="shopping_lists")
