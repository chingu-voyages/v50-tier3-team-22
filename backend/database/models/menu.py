from sqlalchemy import Column, Integer, JSON, Date, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    days = relationship("Day", back_populates="menu")
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="menus")
