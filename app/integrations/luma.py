import requests
from app.core.logger import LoggerConfig
from app.core.config import config

logger = LoggerConfig(__name__).get_logger()


class LumaEvent:
    def __init__(self):
        self.luma_access_key = config.get_luma_access_key()
    
    def list_luma_events(self):
        try:
            url = "https://api.lu.ma/public/v1/calendar/list-events"

            headers = {
                "accept": "application/json",
                "x-luma-api-key": self.luma_access_key
            }

            response = requests.get(url, headers=headers)

            return response.text
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False

    def get_luma_event(self, event_id: str):
        try:
            url = f"https://api.lu.ma/public/v1/event/get?api_id={event_id}"

            headers = {
                "accept": "application/json",
                "x-luma-api-key": self.luma_access_key
            }

            response = requests.get(url, headers=headers)

            return response.text
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False

    def update_luma_event(self, data: dict):
        try:
            url = "https://api.lu.ma/public/v1/event/update"

            payload = {
                "geo_address_json": { "type": "email" },
                "event_api_id": data.get("event_id"),
                "name": data.get("name"),
                "visibility": data.get("visibility") # Either a public or private
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "x-luma-api-key": self.luma_access_key
            }

            response = requests.post(url, json=payload, headers=headers)

            return response.text
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False
