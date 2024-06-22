from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.sqllite import Base


class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    filename = Column(String, index=True)
    url = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", backref="file_metadata")


class LLaMAIndexMetadata(Base):
    __tablename__ = "llama_index_metadata"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    path = Column(String, index=True)
    filename = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", backref="llama_index_metadata")
