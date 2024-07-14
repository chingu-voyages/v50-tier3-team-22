from sqlalchemy.orm import Session

from database.models.user import User as UserModel
from database.schemas.authentication import CreateUser

def create_user(db : Session, user : CreateUser) -> UserModel:
    db_user = UserModel(
        name = user.name,
        password = user.password,
        salt = user.salt,
        email = user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db : Session, id:int):
    db.query(UserModel).filter(UserModel.id == id).delete()
    db.commit()

def get_user_by_name(db : Session, username : str) -> UserModel:
    return db.query(UserModel).filter(UserModel.name == username).first()

def get_user_by_id(db : Session, user_id : int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db : Session, email : str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()