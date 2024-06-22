from typing import List, Dict, Optional
from pydantic import BaseModel

class EventUpdate(BaseModel):
    description: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    endTime: Optional[str] = None
    allowAction: Optional[bool] = None
    caption: Optional[str] = None
    active: Optional[bool] = None
    category: Optional[str] = None
    startTime: Optional[str] = None
    title: Optional[str] = None
    showOnce: Optional[bool] = None
    featured: Optional[bool] = None
    imageId: Optional[bool] = None
    sourceUrl: Optional[bool] = None


class EventCreate(BaseModel):
    description: str
    type: str
    tags: List[str]
    endTime: str
    allowAction: bool
    caption: str
    active: bool
    category: str
    startTime: str
    title: str
    showOnce: bool
    featured: bool
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class EventResponse(BaseModel):
    description: str
    type: str
    tags: List[str]
    endTime: str
    allowAction: bool
    caption: str
    active: bool
    dateUpdated: str
    category: str
    startTime: str
    title: str
    showOnce: bool
    featured: bool
    imageId: bool
    sourceUrl: bool
    id: bool
