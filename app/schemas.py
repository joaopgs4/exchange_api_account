# schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr

#########################################################################
##### Uses pydantic for cache/dynamic objects; not referenced in DB #####
#########################################################################

# Base JWT AuthToken model
class AuthToken(BaseModel):
    uuid: str
    username: str
    email: EmailStr
    role: Optional[str] = None
    exp: Optional[int] = None  # Optional expiry (timestamp) for the JWT

    class Config:
        extra = "allow"

class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserReadDTO(BaseModel):
    uuid: str
    username: str
    email: EmailStr

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
