from sqlalchemy import Column, Integer, String
from app.core.sqllite import Base

# app/models/user_model.py
from sqlalchemy import Column, Integer, String
from app.core.sqllite import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, unique=True, index=True)
    id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
