from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str = "User logged in successfully"
    access_token: str

class TokenData(BaseModel):
    email: EmailStr
    exp: int  # Token expiration time


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str