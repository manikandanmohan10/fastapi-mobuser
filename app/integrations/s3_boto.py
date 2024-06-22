import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from app.core.logger import LoggerConfig
from app.core.config import config

logger = LoggerConfig(__name__).get_logger()


class S3Boto:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config.get_aws_access_key_id(),
            aws_secret_access_key=config.get_aws_secret_access_key()
        )

    async def upload_to_s3(self, upload_file, bucket_name, object_key):
        try:
            res = self.s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=upload_file)
            logger.info(f"Successfully uploaded {object_key} to bucket {bucket_name}")

        except NoCredentialsError:
            logger.error("Credentials not available for S3 upload")
            return False
        
        except PartialCredentialsError:
            logger.error("Incomplete credentials provided")
            return False
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False

        return res
