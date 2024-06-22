import os
from typing import Dict, Union, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.repositories.base import UserRepository, FileRepository, FileStorage
from app.models.sqlite.file_upload_model import FileMetadata, LLaMAIndexMetadata
from app.models.sqlite.user_model import User
from app.core.sqllite import SessionLocal

class SQLiteUserRepository(UserRepository, FileRepository, FileStorage):
    def __init__(self, base_path: str):
        self.db: Session = SessionLocal()
        self.base_path = base_path

    async def fetch_user_by_email(self, email: str) -> Optional[Dict]:
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return {"email": user.email, "password": user.password}
        return None

    def store_file_metadata(self, metadata: Dict[str, Union[str, int, float]]) -> int:
        db_metadata = FileMetadata(**metadata)
        self.db.add(db_metadata)
        self.db.commit()
        self.db.refresh(db_metadata)
        return db_metadata.id
    
    async def get_file_metadata(self):
        pass
    
    async def get_llama_index_metadata(self):
        data = self.db.query(LLaMAIndexMetadata).all()
        job_id_list = [{'job_id': job.job_id} for job in data]
        return {"status": "success", "message": "fetched successfully", "data": job_id_list}

    def store_llama_index_metadata(self, metadata: Dict[str, Union[str, int, float]]) -> int:
        db_metadata = LLaMAIndexMetadata(**metadata)
        self.db.add(db_metadata)
        self.db.commit()
        self.db.refresh(db_metadata)
        return db_metadata.id

    async def upload_file(self, file: UploadFile, object_key: str, md_format: bool = False, job_id: str=None) -> Dict[str, Union[str, int, float]]:
        file_path = os.path.join(self.base_path, object_key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if md_format:
            with open(file_path, 'w') as f:
                f.write(file)
            
            return {
                "message": "File uploaded successfully",
                "details": {
                    "path": object_key,
                    "job_id": job_id,
                    "filename": job_id + '.md' if job_id else ''
                }
            }
        
        else:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
        
        return {
            "message": "File uploaded successfully",
            "details": {
                "path": file_path,
                "filename": object_key,
            }
        }
