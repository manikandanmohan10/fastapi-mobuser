from fastapi import HTTPException
from app.core.jwt_auth import JWTManager
from app.core.password_manager import PasswordManager
from app.models.pydantic.user_model import Login
from app.repositories.base import UserRepository
from app.repositories.repository_factory import RepositoryFactory

class AuthenticationService:
    def __init__(self) -> None:
        self.user_repository = RepositoryFactory.create_user_repository()
        self.jwt_auth = JWTManager()
        self.password_manager = PasswordManager()

    async def on_login(self, form_data: Login):
        email = form_data.email
        password = form_data.password
        
        user = await self.user_repository.fetch_user_by_email(email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not self.password_manager.verify_password(password, user.get('password')):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        access_token = self.jwt_auth.create_access_token(user)
        response_data = {
            "message": "User Logged in successfully",
            "access_token": access_token
        }

        return response_data
