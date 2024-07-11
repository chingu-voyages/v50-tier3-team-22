from sqlalchemy.orm import Session

from database.models.user import User as UserModel
from database.schemas.authentication import CreateUser

def create_user(db : Session, user : CreateUser) -> UserModel:
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db : Session, id:int):
    db.query(UserModel).filter(UserModel.id == id).delete()
    db.commit()

def get_user_by_username(db : Session, username : str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_id(db : Session, user_id : int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db : Session, email : str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).first()