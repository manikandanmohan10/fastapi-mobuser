from typing import List, Dict, Optional
from pydantic import BaseModel

class ProductUpdate(BaseModel):
    features: Optional[List[str]] = None
    description: Optional[str] = None
    type: Optional[str] = None
    relatedItems: Optional[List[str]] = None
    active: Optional[bool] = None
    category: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    featured: Optional[bool] = None
    relatedProducts: Optional[List[str]] = None
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class ProductCreate(BaseModel):
    features: List[str]
    description: str
    type: str
    relatedItems: List[str]
    active: bool
    category: str
    title: str
    caption: str
    featured: bool
    relatedProducts: List[str]
    imageId: Optional[str] = None
    sourceUrl: Optional[str] = None


class ProductResponse(BaseModel):
    features: List[str]
    description: str
    type: str
    relatedItems: List[str]
    dateUpdated: str
    active: bool
    category: str
    title: str
    caption: str
    featured: bool
    relatedProducts: List[str]
    imageId: str
    sourceUrl: str
    id: str
