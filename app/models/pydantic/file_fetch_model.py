from typing import List, Dict
from pydantic import BaseModel

class FileFetchResponse(BaseModel):
    status: str = "success"
    message: str = "Fetched successfully"
    data: List[Dict[str, str]]
