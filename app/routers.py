# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models import *
from schemas import *
from dbutils import *
from database import get_db
from typing import Optional

router = APIRouter(
    prefix="/account",
    tags=["account"]
)

###################################
##### Routers Functions Below #####
###################################

#Default function, change as needed
@router.get("")
async def root_func():
    return {"message": "Root function ran!"}

@router.post("/register", response_model=UserReadDTO, status_code=201)
async def user_register(payload: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        if get_user_by_email(db, payload.email):
            raise HTTPException(400, detail="E-mail já cadastrado")
        if get_user_by_username(db, payload.username):
            raise HTTPException(400, detail="Username já cadastrado")
        
        user = create_user(db, payload)
        return UserReadDTO(id=user.id, username=user.username, email=user.email)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login", response_model=UserReadDTO, status_code=200)
async def user_login(payload: UserLoginDTO, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, payload.email)
        if not user:
            raise HTTPException(400, detail="User não cadastrado")
        pass_hashed = pass_hasher(payload.password)
        if pass_hashed != get_password_by_id(db, user.id_password):
            raise HTTPException(400, detail="Senha incorreta")
        return UserReadDTO(id=user.id, username=user.username, email=user.email)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))