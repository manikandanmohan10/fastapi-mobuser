import pydantic
from typing import List, Dict
from app.models.pydantic.product_model import ProductUpdate, ProductCreate, ProductResponse
from app.models.pydantic.post_common_model import PostUpdateResponse
from fastapi import APIRouter, Request, HTTPException, Depends, Response, Query
from app.services.posts_service import PostService
from app.core.logger import LoggerConfig
from app.core.auth import get_current_user

router = APIRouter(prefix='/products', tags=['Products'])

post_service = PostService()
logger = LoggerConfig(__name__).get_logger()


@router.get('', response_model=List[ProductResponse], status_code=200)
async def get_products_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, le=100)
):
    try:
        logger.info(f'{request.url.path} - Fetching Product by {"user"}')
        return await post_service.get_post_list(post_type="product", page=page, page_size=page_size)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('', response_model=ProductResponse, status_code=201)
async def create_product(
    request: Request,
    post: ProductCreate
    # user: dict = Depends(get_current_user("editor"))
):
    try:
        logger.info(f'{request.url.path} - Creating by {"user"}')
        return await post_service.create_post(post_data=post)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        return HTTPException(status_code=500, detail=str(e))
    

@router.put('/{product_id}', response_model=PostUpdateResponse, status_code=200)
async def update_product(
    request: Request,
    product_id: str,
    product: ProductUpdate
):
    try:
        logger.info(f'{request.url.path} - Updating {product_id}')
        return await post_service.update_post(post_id=product_id, data=product)
    except HTTPException as e:
        logger.error(f'{request.url.path} - {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'{request.url.path} - {str(e)}')
        return HTTPException(status_code=500, detail=str(e))
