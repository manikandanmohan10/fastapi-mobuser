from typing import List, Dict, Optional
from pydantic import BaseModel

class CardsUpdate(BaseModel):
    active: Optional[bool] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    captions: Optional[str] = None
    items: Optional[List[Dict]] = None
    category: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    featured: Optional[bool] = None
    difficulty: Optional[str] = None
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class CardsCreate(BaseModel):
    active: bool
    type: str
    tags: List[str]
    captions: str
    items: List[Dict]
    category: str
    title: str
    caption: str
    featured: bool
    difficulty: str
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class CardsResponse(BaseModel):
    active: bool
    dateUpdated: str
    type: str
    tags: List[str]
    captions: str
    items: List[Dict]
    category: str
    title: str
    caption: str
    featured: bool
    difficulty: str
    imageId: str
    sourceUrl: str
    id: str
