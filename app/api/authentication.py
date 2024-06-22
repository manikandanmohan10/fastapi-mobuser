from typing import List
from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.pydantic.user_model import Login, LoginResponse, UserCreate
from app.services.authentication_service import AuthenticationService
from app.core.logger import LoggerConfig
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.sqllite import SessionLocal, init_db
from app.models.sqlite.user_model import User
from app.core.password_manager import PasswordManager
from app.core.sqllite import get_db

logger = LoggerConfig(__name__).get_logger()
authentication_service = AuthenticationService()
passwd_manager = PasswordManager()


router = APIRouter(prefix='/login', tags=['Authentication'])

@router.post('', response_model=LoginResponse, status_code=200)
async def login(request: Request, user_data: Login):
    try:
        logger.info(f'{request.url.path} - Login attempt for {user_data.email}')
        response = await authentication_service.on_login(user_data)
        return response
    except HTTPException as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise HTTPException(status_code=500, detail="Could not login")

# @router.on_event("startup")
# def on_startup():
#     init_db()


# @router.post("/users", response_model=UserCreate)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = passwd_manager.hash_password(user.password)
#     db_user = User(name=user.name, email=user.email, password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
