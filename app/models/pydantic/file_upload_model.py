from typing import Optional, Dict, Union
from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    message: str
    metadata_id: Optional[int] = None
    details: Optional[Dict[str, Union[str, int, float]]] = None