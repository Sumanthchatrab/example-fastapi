from ast import Str
from datetime import datetime
from secrets import token_bytes
from click import INT
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional

class base(BaseModel):
    title : str
    content : str
    published: bool = True
class postschema(base):
    pass
    #place: str

class putscehma(base):
    pass

class userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

#response schema
class respost(base):
    id: int
    owner_id: int
    owner: userout
    class Config:
        orm_mode = True
    
class user(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Votes(BaseModel):
    post_id: int
    dir: bool
