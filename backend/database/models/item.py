from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(Integer)
    unit = Column(Integer)
    amount = Column(Integer)
    is_checked = Column(Boolean, default=False)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"))

    shopping_list = relationship("ShoppingList", back_populates="items")