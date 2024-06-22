from typing import List, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.file_fetch_service import FileFetchService
from app.models.pydantic.file_fetch_model import FileFetchResponse
from app.core.logger import LoggerConfig

logger = LoggerConfig(__name__).get_logger()
llama_service = FileFetchService()

router = APIRouter(prefix='/job_id_list', tags=['Jobs'])

@router.post('', response_model=FileFetchResponse, status_code=200)
async def get_job_list(request: Request):
    try:
        logger.info(f'{request.url.path} - Fetching job id list')
        return await llama_service.get_job_id_list()
    except HTTPException as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise HTTPException(status_code=500, detail="Could not fetch job information")
