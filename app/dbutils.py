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

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_uuid(db: Session, uuid_: str) -> User | None:
    return db.query(User).filter(User.uuid == uuid_).first()

def pass_hasher(password: str) -> str:
    hasher = hashlib.sha256()
    hasher.update((password + PASS_SALT).encode('utf-8'))
    return hasher.hexdigest()

def create_user(db: Session, userDTO: UserCreateDTO) -> UserReadDTO:
    hashed_password = pass_hasher(userDTO.password)

    user = User(
        username=userDTO.username,
        email=userDTO.email,
        password256=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserReadDTO(uuid=user.uuid, username=user.username, email=user.email)
