from typing import Optional
from fastapi import APIRouter, Request, UploadFile, HTTPException, Query
from app.core.logger import LoggerConfig
from app.services.file_storage_service import FileStorageService
from app.models.pydantic.file_upload_model import FileUploadResponse

logger = LoggerConfig(__name__).get_logger()
file_storage_service = FileStorageService()

router = APIRouter(prefix="/file_upload", tags=["File Uploads"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile,
    index_to_llama: Optional[bool] = Query(False)
):
    content_type = file.content_type

    if file.filename.endswith('.exe'):
        logger.error(f"{request.url.path} Attempt to upload unsupported file type.")
        raise HTTPException(status_code=415, detail="Unsupported file type")

    try:
        logger.info(f"{request.url.path} Uploading document to storage...")
        object_key = file.filename
        storage_response = await file_storage_service.upload_to_storage(file, object_key)

        if index_to_llama:
            logger.info(f"{request.url.path} Additionally uploading document to LLAMA index...")
            llama_response = await file_storage_service.upload_to_llama_index(file)
            return llama_response

        return storage_response
    except HTTPException as e:
        logger.error(f"{request.url.path} Failed to upload due to {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"{request.url.path} An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading: {str(e)}")
