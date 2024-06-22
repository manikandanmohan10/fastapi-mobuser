from datetime import timedelta, datetime, timezone

import jwt
from typing import Annotated, Union
from app.core.config import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from app.models.pydantic.user_model import TokenData
from app.services.firestore_service import FireStoreService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTManager:
    def __init__(self) -> None:
        self.db = FireStoreService()

    def create_access_token(self, data: dict,
                            expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=300)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.get_security_key(), algorithm=config.get_jwt_algorithm())
        return encoded_jwt

    def decode_token(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, config.secret_key, algorithms=[config.jwt_algorithm])
            email: str = payload.get("email")
            if email is None:
                return False
            token_data = TokenData(email=email)
        except InvalidTokenError:
            return False
        user = self.get_user(email=token_data.email)
        if user is None:
            return False
        return user

    def get_user(self, email):
        user = self.db.fetch_data('tabUserss', email)
        return user[0] if user else None
