from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from database.database import Base

class Day(Base):
    __tablename__  = "days"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(DateTime)
    meal_plan = Column(JSON, default={
        "breakfast" : [],  
        "lunch" : [],
        "dinner" : [],
        "snacks" : []
    })
    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Day", back_populates="days")