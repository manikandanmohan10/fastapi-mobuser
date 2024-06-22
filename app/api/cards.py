from typing import List, Dict
from app.models.pydantic.cards_model import CardsUpdate, CardsCreate, CardsResponse
from app.models.pydantic.post_common_model import PostUpdateResponse
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from app.services.posts_service import PostService
from app.core.logger import LoggerConfig
from app.core.auth import get_current_user

router = APIRouter(prefix='/cards', tags=['Cards'])

post_service = PostService()
logger = LoggerConfig(__name__).get_logger()


@router.get('', response_model=List[CardsResponse], status_code=200)
async def get_cards_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100)
):
    try:
        logger.info(f'{request.url.path} - Fetching Cards by {"user"}')
        return await post_service.get_post_list(post_type='cards', page=page, page_size=page_size)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('', response_model=CardsResponse, status_code=201)
async def create_card(
    request: Request,
    post: CardsCreate,
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
    

@router.put('/{card_id}', response_model=PostUpdateResponse, status_code=200)
async def update_card(
    request: Request,
    card_id: str,
    shot: CardsUpdate
):
    try:
        logger.info(f'{request.url.path} - Updating {card_id}')
        return await post_service.update_post(post_id=card_id, data=shot)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        return HTTPException(status_code=500, detail=str(e))
