from abc import ABC, abstractmethod
from typing import Dict, Union, Optional
from fastapi import UploadFile

class UserRepository(ABC):
    @abstractmethod
    async def fetch_user_by_email(self, email: str) -> Optional[Dict[str, Union[str, int]]]:
        pass

class FileStorage(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile, object_key: str, md_format: bool = False) -> Dict[str, Union[str, int, float]]:
        pass

class FileRepository(ABC):
    @abstractmethod
    def store_file_metadata(self, metadata: Dict[str, Union[str, int, float]]) -> int:
        pass

    @abstractmethod
    def store_llama_index_metadata(self, metadata: Dict[str, Union[str, int, float]]) -> int:
        pass

    @abstractmethod
    def get_file_metadata(self):
        pass

    @abstractmethod
    def get_llama_index_metadata(self):
        pass
