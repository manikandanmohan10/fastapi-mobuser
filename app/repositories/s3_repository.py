from typing import Dict, Union
from fastapi import UploadFile
from app.integrations.s3_boto import S3Boto
from app.repositories.base import FileStorage
from app.core.config import config

class S3Repository(FileStorage):
    def __init__(self):
        self.s3 = S3Boto()
        self.bucket_name = config.get_aws_s3_bucket()
        self.region_name = "ap-south-1"

    async def upload_file(self, file: UploadFile, object_key: str, md_format: bool = False, job_id=None) -> Dict[str, Union[str, int, float]]:
        if md_format:
            await self.s3.upload_to_s3(file, self.bucket_name, object_key)
        else:
            with file.file as file_obj:
                await self.s3.upload_to_s3(file_obj, self.bucket_name, object_key)
        
        return {
            "message": "File uploaded successfully",
            "details": {
                "url": f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{object_key}",
                "filename": object_key
            }
        }
