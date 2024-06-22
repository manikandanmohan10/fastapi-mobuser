from datetime import datetime
from typing import List, Dict, Optional
from app.models.pydantic.shots_model import ShotResponse, ShotUpdate, ShotCreate
from app.models.pydantic.post_common_model import PostUpdateResponse
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from app.services.posts_service import PostService
from app.core.logger import LoggerConfig
from app.core.auth import get_current_user

router = APIRouter(prefix='/shots', tags=['Shots'])

post_service = PostService()
logger = LoggerConfig(__name__).get_logger()
    

@router.get('', response_model=List[ShotResponse], status_code=200)
async def get_shots_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100),
):
    try:
        logger.info(f'{request.url.path} - Fetching Shots by {"user"}')
        return await post_service.get_post_list(post_type="shot", page=page, page_size=page_size)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('', response_model=ShotResponse, status_code=201)
async def create_shot(
    request: Request,
    post: ShotCreate,
    user: dict = Depends(get_current_user("editor"))
):
    try:
        logger.info(f'{request.url.path} - Creating by {user}')
        return await post_service.create_post(post_data=post)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        return HTTPException(status_code=500, detail=str(e))


@router.put('/{shot_id}', response_model=PostUpdateResponse, status_code=200)
async def update_shot(
    request: Request,
    shot_id: str,
    shot: ShotUpdate
):
    try:
        logger.info(f'{request.url.path} - Updating {shot_id}')
        return await post_service.update_post(post_id=shot_id, data=shot)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        return HTTPException(status_code=500, detail=str(e))
