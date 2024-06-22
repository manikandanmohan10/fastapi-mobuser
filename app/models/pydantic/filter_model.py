from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum


class DateFilterType(str, Enum):
    lt = "less_than"
    gt = "greater_than"


class FilterRequest(BaseModel):
    page: int = None
    page_size: int = None
    post_type: Optional[List[str]] = None
    date_filter: Optional[str] = None
    category_filter: Optional[str] = None
    tags_filter: Optional[List[str]] = None
    date_filter_type: Optional[str] = None
