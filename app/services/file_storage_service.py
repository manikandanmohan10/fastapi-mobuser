import json
import urllib3
from typing import Dict, Union
from fastapi import HTTPException, UploadFile
from urllib.parse import quote
from app.repositories.repository_factory import RepositoryFactory
from app.core.logger import LoggerConfig
from app.core.config import config
from app.models.pydantic.file_upload_model import FileUploadResponse

logger = LoggerConfig(__name__).get_logger()

class FileStorageService:
    def __init__(self):
        self.file_storage = RepositoryFactory.create_file_storage()
        self.file_repository = RepositoryFactory.create_file_repository()
        self.llama_http = urllib3.PoolManager()
        self.llama_update_api_url = "https://api.cloud.llamaindex.ai/api/parsing/upload"
        self.llama_access_key = config.get_llama_access_key()

    async def upload_to_storage(self, file: UploadFile, object_key: str, md_format: bool = False, job_id: str=None) -> FileUploadResponse:
        try:
            upload_result = await self.file_storage.upload_file(file, object_key, md_format=md_format, job_id=job_id)
            if md_format:
                metadata = {
                    "job_id": upload_result["details"].get("job_id", ""),
                    "filename": object_key,
                }
                metadata_id = self.file_repository.store_llama_index_metadata(metadata)
            else:
                metadata = {
                    "path": upload_result["details"].get("path", ""),
                    "filename": object_key,
                    "url": upload_result["details"].get("url", "")
                }
                metadata_id = self.file_repository.store_file_metadata(metadata)
            return FileUploadResponse(
                message="File uploaded successfully",
                metadata_id=metadata_id,
                details=upload_result["details"]
            )
        except Exception as e:
            logger.error(f"Error uploading to storage: {str(e)}")
            raise HTTPException(detail=str(e), status_code=500)

    async def upload_to_llama_index(self, file: UploadFile) -> FileUploadResponse:
        try:
            content = await file.read()
            encoded_key = quote(file.filename)
            headers = {
                'Authorization': f'Bearer {self.llama_access_key}'
            }
            fields = {
                'file': (encoded_key, content)
            }
            response = self.llama_http.request('POST', self.llama_update_api_url, headers=headers, fields=fields)
            if response.status != 200:
                logger.error(f"Failed to upload document to LLAMA index: {response.status}")
                raise HTTPException(status_code=response.status, detail=f"Failed to upload document to LLAMA index: {response.status}")

            response_data = json.loads(response.data.decode('utf-8'))
            return await self.access_parse_file(response_data.get('id'))
        except Exception as e:
            logger.error(f"Error uploading document to LLAMA index: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error uploading document to LLAMA index: {str(e)}")

    async def access_parse_file(self, job_id: str) -> FileUploadResponse:
        url = f"https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.llama_access_key}'
        }
        try:
            response = self.llama_http.request('GET', url, headers=headers)
            response_data = json.loads(response.data.decode('utf-8'))
            markdown_content = response_data.get("markdown", "")
            object_key = f"results/{job_id}.md"
            upload_result = await self.upload_to_storage(markdown_content, object_key=object_key, md_format=True, job_id=job_id)
            metadata = {
                "path": upload_result.details["path"],
                "filename": object_key
            }
            metadata_id = self.file_repository.store_file_metadata(metadata)
            return FileUploadResponse(
                message="File uploaded successfully",
                metadata_id=metadata_id,
                details=upload_result.details
            )
        except Exception as e:
            logger.error(f"Error fetching job result: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching job result: {str(e)}")
