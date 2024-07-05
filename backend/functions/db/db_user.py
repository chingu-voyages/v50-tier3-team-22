from sqlalchemy.orm import Session

from database.models.user import User as UserModel
from database.schemas.authentication import CreateUser

def create_user(db : Session, user : CreateUser) -> UserModel:
    db_user = UserModel(
        username = user.username,
        password = user.password,
        salt = user.salt,
        email = user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db : Session, id:int):
    db.query(UserModel)

def get_user_by_username(db : Session, username : str) -> UserModel:
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_id(db : Session, user_id : int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db : Session, email : str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()