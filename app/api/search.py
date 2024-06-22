from typing import List, Dict, Optional, Union
from fastapi import APIRouter, HTTPException, Request, Query
from app.models.pydantic.filter_model import FilterRequest, DateFilterType
from app.models.pydantic.shots_model import ShotResponse
from app.models.pydantic.cards_model import CardsResponse
from app.models.pydantic.event_model import EventResponse
from app.models.pydantic.product_model import ProductResponse
from app.services.posts_service import PostService
from app.core.logger import LoggerConfig

logger = LoggerConfig(__name__).get_logger()
post_service = PostService()

router = APIRouter(prefix='/search', tags=['Search'])

@router.get('', response_model=List[Union[ShotResponse, CardsResponse, ProductResponse, EventResponse]], status_code=200)
async def search_api(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100),
    post_type: List[str] = Query(None, description="Filter by type"),
    date_filter: Optional[str] = Query("2024-05-10", description="Filter by date updated"),
    date_filter_type: Optional[DateFilterType] = Query("less_than", description="Filter by type"),
    category_filter: Optional[str] = Query(None, description="Filter by category"),
    tags_filter: Optional[List[str]] = Query(None, description="Filter by tags")
):
    try:
        logger.info(f"{request.url.path} Filtering the data")
        filters_ = FilterRequest(
            page=page,
            page_size=page_size,
            post_type=post_type,
            date_filter=date_filter,
            date_filter_type=date_filter_type,
            category_filter=category_filter,
            tags_filter=tags_filter
        )
        return await post_service.get_post_list_with_filter(filters_)
    except HTTPException as e:
        logger.error(f"{request.url.path} {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"An error occured {str(e)}")
        raise HTTPException(detail=str(e), status_code=500)
