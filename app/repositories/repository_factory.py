from typing import Type, Dict
from app.repositories.base import UserRepository, FileStorage, FileRepository
from app.repositories.firestore_repository import FirestoreUserRepository
from app.repositories.sqlite_repository import SQLiteUserRepository
from app.repositories.s3_repository import S3Repository
from app.core.config import config

class RepositoryFactory:
    _user_repositories: Dict[str, Type[UserRepository]] = {
        'firestore': FirestoreUserRepository,
        'sqlite': SQLiteUserRepository,
    }

    _file_storages: Dict[str, Type[FileStorage]] = {
        's3': S3Repository,
        'local': SQLiteUserRepository  # Assuming SQLiteUserRepository handles local file storage
    }

    _file_repositories: Dict[str, Type[FileRepository]] = {
        'firestore': FirestoreUserRepository,
        'sqlite': SQLiteUserRepository,
        # Add other repositories as needed
    }

    @classmethod
    def create_user_repository(cls) -> UserRepository:
        database_type = config.get_database_type()
        repository_class = cls._user_repositories.get(database_type)
        
        if not repository_class:
            raise ValueError(f"Unsupported database type: {database_type}")
        
        if database_type == 'sqlite':
            return repository_class(base_path=config.get_local_storage_path())
        else:
            return repository_class()

    @classmethod
    def create_file_storage(cls) -> FileStorage:
        storage_type = config.get_file_storage_type()
        storage_class = cls._file_storages.get(storage_type)
        
        if not storage_class:
            raise ValueError(f"Unsupported storage type: {storage_type}")

        if storage_type == 'local':
            return storage_class(base_path=config.get_local_storage_path())
        else:
            return storage_class()

    @classmethod
    def create_file_repository(cls) -> FileRepository:
        repository_type = config.get_file_repository_type()
        repository_class = cls._file_repositories.get(repository_type)
        
        if not repository_class:
            raise ValueError(f"Unsupported repository type: {repository_type}")

        if repository_type == 'sqlite':
            return repository_class(base_path=config.get_local_storage_path())
        else:
            return repository_class()
