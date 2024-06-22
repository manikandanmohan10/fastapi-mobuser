import requests
from app.core.logger import LoggerConfig

logger = LoggerConfig(__name__).get_logger()


class Cloudinary:
    def __init__(self):
        self.url = "https://api.cloudinary.com/v1_1/zysec-ai/upload"

    def upload_to_cloudinary(self, file):
        try:
            payload = {
                'upload_preset': 'upload-api'
            }   
            files = {
                'file': file
            }
            response = requests.post(self.url, files=files, data=payload)
            if response.status_code == 200:
                logger.info("File uploaded successfully in the cloudinary")
                return response.json()
            else:
                logger.info(f"An error acccured {response.json()}")
                return False
        except Exception as e:
            logger.info(f"An error acccured {e}")
            return False
