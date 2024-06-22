from fastapi import HTTPException
from app.repositories.repository_factory import RepositoryFactory

class FileFetchService:
    def __init__(self):
        self.file_storage = RepositoryFactory.create_file_storage()

    async def get_job_id_list(self):
        try:
            return await self.file_storage.get_llama_index_metadata()
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
