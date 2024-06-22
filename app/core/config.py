from dotenv import dotenv_values

class AppConfig:
    def __init__(self, env_file='.env'):
        self.env_file = env_file
        self.configs = dotenv_values(self.env_file)

        # Initialize attributes with default values or None
        self.SECURITY_KEY = self.configs.get('SECURITY_KEY', 'kT385rSv6LYFom28ScUOUuqWdwMlU3QZlbPKoYPPUMc')
        self.JWT_ALGORITHM = self.configs.get('JWT_ALGORITHM', 'HS256')
        self.AWS_ACCESS_KEY_ID = self.configs.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = self.configs.get('AWS_SECRET_ACCESS_KEY')
        self.LUMA_ACCESS_KEY = self.configs.get('LUMA_ACCESS_KEY')
        self.AWS_S3_BUCKET_NAME = self.configs.get('AWS_S3_BUCKET_NAME')
        self.LLAMAINDEX_API_KEY = self.configs.get('LLAMAINDEX_API_KEY')
        
        # Database settings
        self.DATABASE_TYPE = self.configs.get('DATABASE_TYPE', 'sqlite')
        self.SQLITE_DB_PATH = self.configs.get('SQLITE_DB_PATH', 'data_store.db')
        self.MONGODB_CONNECTION_STRING = self.configs.get('MONGODB_CONNECTION_STRING', '')
        self.MONGODB_DB_NAME = self.configs.get('MONGODB_DB_NAME', '')

        self.FILE_STORAGE_TYPE = self.configs.get('FILE_STORAGE_TYPE', 'local') # It can be either local or s3
        self.FILE_REPOSITORY_TYPE = self.configs.get('FILE_REPOSITORY_TYPE', 'sqlite')
        self.LOCAL_STORAGE_PATH = self.configs.get('LOCAL_STORAGE_PATH', './temp')

    def get_security_key(self):
        return self.SECURITY_KEY

    def get_jwt_algorithm(self):
        return self.JWT_ALGORITHM

    def get_aws_access_key_id(self):
        return self.AWS_ACCESS_KEY_ID

    def get_aws_secret_access_key(self):
        return self.AWS_SECRET_ACCESS_KEY
    
    def get_luma_access_key(self):
        return self.LUMA_ACCESS_KEY
    
    def get_aws_s3_bucket(self):
        return self.AWS_S3_BUCKET_NAME
    
    def get_llama_access_key(self):
        return self.LLAMAINDEX_API_KEY
    
    def get_database_type(self):
        return self.DATABASE_TYPE

    def get_sqlite_db_path(self):
        return self.SQLITE_DB_PATH

    def get_mongodb_connection_string(self):
        return self.MONGODB_CONNECTION_STRING

    def get_mongodb_db_name(self):
        return self.MONGODB_DB_NAME
    
    def get_file_storage_type(self):
        return self.FILE_STORAGE_TYPE

    def get_file_repository_type(self):
        return self.FILE_REPOSITORY_TYPE

    def get_local_storage_path(self):
        return self.LOCAL_STORAGE_PATH

config = AppConfig()
