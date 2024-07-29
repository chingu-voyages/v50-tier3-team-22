from sqlalchemy.orm import Session

from database.models.day import Day as DayModell

from database.schemas.day import CreateDay

def create_day(db : Session, day : CreateDay) -> DayModell:
    db_day = DayModell(**day.dict())
    db.add(db_day)
    db.commit()
    db.refresh(db_day)

    return db_day

def update_day(db : Session,id = int,  data_to_update = dict):
    db.query(DayModell).filter(DayModell.id == id).update(data_to_update)
    db.commit()
    
def delete_day(db : Session, id : int):
    db.query(DayModell).filter(DayModell.id == id).delete()
    db.commit()

def delete_days(db : Session, owner_id : int):
    db.query(DayModell).filter(DayModell.owner_id == owner_id).delete()

def get_day_by_id(db : Session, id : int) -> DayModell | None:
    return db.query(DayModell).filter(DayModell.id == id).first()