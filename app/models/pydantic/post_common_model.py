from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from app.models.pydantic.shots_model import ShotResponse
from app.models.pydantic.cards_model import CardsResponse
from app.models.pydantic.event_model import EventResponse
from app.models.pydantic.product_model import ProductResponse

class PostUpdate(BaseModel):
    features: Optional[List[str]] = None
    description: Optional[str] = None
    type: Optional[str] = None
    relatedItems: Optional[List[str]] = None
    dateUpdated: Optional[str] = None
    active: Optional[bool] = None
    category: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    featured: Optional[bool] = None
    relatedProducts: Optional[List[str]] = None
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None
    id: Optional[str] = None
    tags: Optional[List[str]] = None
    endTime: Optional[str] = None
    allowAction: Optional[bool] = None
    caption: Optional[str] = None
    startTime: Optional[str] = None
    showOnce: Optional[bool] = None
    difficulty: Optional[str] = None
    captions: Optional[str] = None
    caption: Optional[str] = None


class PostUpdateResponse(BaseModel):
    message: Dict = 'updated successfully'


class SearchResponse(BaseModel):
    response: Optional[List[Union[ShotResponse, CardsResponse, ProductResponse, EventResponse]]]
