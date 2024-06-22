from typing import List, Dict
from app.models.pydantic.post_common_model import PostUpdate
from app.services.firestore_service import FireStoreService

class PostService:
    def __init__(self):
        self.db = FireStoreService()
        self.collection_name = 'appContentDB'
    
    def _return_data(self, collection_name, doc_id):
        data = self.db.fetch_data(collection_name, doc_id=doc_id)
        return data
    
    @staticmethod
    def _process_filter(data, key, any_value='any'):
        if data.get(key):
            if key == 'category_filter':
                type_ = data[key].lower()
            else:
                type_ = [data.lower() for data in data.get(key)]
            if any_value in type_:
                return None
            return data.get(key)

    async def get_post_list(self, post_type: str, page: int=1, page_size: int=50) -> List[Dict]:
        post_list = await self.db.fetch_data(
            collection_name=self.collection_name,
            post_type=post_type,
            page=page,
            page_size=page_size
        )
        return post_list

    async def update_post(self, post_id: str, data: PostUpdate) -> bool:
        data_ = {
            field_name: field_value
            for field_name, field_value in data.dict().items()
            if field_value is not None
        }
        await self.db.update_data(collection_name=self.collection_name, doc_id=post_id, data=data_)

        return {'message': 'updated successfully'}

    async def create_post(self, post_data: List):
        doc_id = await self.db.add_data(collection_name=self.collection_name, data=post_data)
        created_data = self._return_data(collection_name=self.collection_name, doc_id=doc_id)

        return created_data
    
    async def get_post_list_with_filter(self, filters_: Dict):
        filters_data = {
            field_name: field_value
            for field_name, field_value in filters_.dict().items()
            if field_value is not None
        }

        filters_data['post_type'] = self._process_filter(filters_data, 'post_type', 'any')
        filters_data['category_filter'] = self._process_filter(filters_data, 'category_filter', 'any')
        filters_data['tags_filter'] = self._process_filter(filters_data, 'tags_filter', 'any')
        filters_data['date_filter'] = self._process_filter(filters_data, 'date_filter', 'anytime')

        post_list = await self.db.fetch_data(
            collection_name=self.collection_name,
             **filters_data
        )
        return post_list
