from typing import List, Optional
from pydantic import BaseModel


class ShotResponse(BaseModel):
    id: str
    title: str
    active: bool
    description: str
    type: str
    tags: List[str]
    dateUpdated: str
    category: str
    featured: bool
    imageId: str
    sourceUrl: str


class ShotUpdate(BaseModel):
    title: Optional[str] = None
    active: Optional[bool] = None
    description: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    featured: Optional[bool] = None
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class ShotCreate(BaseModel):
    title: str
    active: bool = False
    description: str
    type: str
    tags: List[str]
    category: str
    featured: bool = False
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class ShotFilter(BaseModel):
    category_filter: Optional[str] = None
    date_filter: Optional[str] = None
    tags_filter: Optional[List[str]] = None
