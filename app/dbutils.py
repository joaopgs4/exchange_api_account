#dbutils.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import *
from schemas import *
import hashlib
import os

PASS_SALT=os.getenv("PASS_SALT")
if PASS_SALT is None:
    raise ValueError("Environment variable PASS_SALT is not set.")

def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    return None

def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return None

def get_password_by_id(db: Session, id: int) -> str:
    password = db.query(Password).filter(Password.id == id).first()
    if password:
        return password.password256
    return None

def pass_hasher(password : str) -> str:
    hasher = hashlib.sha256()
    hasher.update((password + PASS_SALT).encode('utf-8'))
    return hasher.hexdigest()

def create_user(db: Session, userDTO: UserCreateDTO) -> UserReadDTO:
    #Hash password
    hashed_password = pass_hasher(userDTO.password)

    #Add password to db
    password = Password(password256=hashed_password)
    db.add(password)
    db.commit()
    db.refresh(password)

    #Add user to db
    user = User(
        username=userDTO.username,
        email=userDTO.email,
        id_password=password.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
