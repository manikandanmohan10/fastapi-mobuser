from typing import Dict, List
from pydantic import BaseModel
from enum import Enum


class LineChartRequest(str, Enum):
    today: str = 'today'
    month: str = 'month'
    year: str = 'year'
    week: str = 'week'


class LineChartResponse(BaseModel):
    value: str
    count: int


class CardValuesResponse(BaseModel):
    name: str
    count: int
