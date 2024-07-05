from pydantic import BaseModel
from datetime import datetime
class UserBase(BaseModel):
    """Class with the basic info needed for all user shemas"""
    username : str
    email : str

class User(UserBase):
    """Basic user modell sterilized of secrets"""
    id : int

class LoginUser(BaseModel):
    """User modell for login"""
    username : str
    password : str

class RegisterUser(UserBase):
    """User modell for regitering"""
    password : str
class CreateUser(RegisterUser):
    salt : str
    

class Token(BaseModel):
    """"Token modell"""
    access_token : str
    token_type : str

class TokenReturn(Token):
    """Token modell containing expiry"""
    expiry : datetime