from pydantic import BaseModel
from datetime import datetime
class UserBase(BaseModel):
    """Class with the basic info needed for all user shemas"""
    username : str
    email : str

class User(UserBase):
    """Basic user model sterilized of secrets"""
    id : int

class LoginUser(BaseModel):
    """User model for login"""
    username : str
    password : str

class RegisterUser(UserBase):
    """User model for regitering"""
    password : str
class CreateUser(RegisterUser):
    salt : str
    

class Token(BaseModel):
    """"Token model"""
    access_token : str
    token_type : str

class TokenReturn(Token):
    """Token model containing expiry"""
    expiry : datetime