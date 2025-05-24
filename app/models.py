# models.py
import uuid
from sqlalchemy import (
    Column, String
)
from sqlalchemy.orm import declarative_base
Base = declarative_base()

######################################################################
##### Uses SqlAlchemy bases for static objects; referenced in DB #####
######################################################################

#Default password table for saving the user password as a hash256
#(Receives the hashed string)

class User(Base):
    __tablename__ = 'user'

    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    password256 = Column(String(256), nullable=False)

