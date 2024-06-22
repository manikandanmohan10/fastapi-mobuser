from app.core.firestore_handler import FirestoreHandler


class FireStoreService:
    def __init__(self):
        self.db = FirestoreHandler()
    
    async def fetch_data(self, collection_name, *args, **kwargs):
        return self.db.fetch_data(collection_name, **kwargs)

    async def update_data(self, collection_name, *args, **kwargs):
        return self.db.update_data(collection_name, **kwargs)

    async def add_data(self, collection_name, *args, **kwargs):
        return self.db.add_data(collection_name, **kwargs)
    
    async def fetch_all_data(self, collection_name, *args, **kwargs):
        return self.db.fetch_all_data(collection_name, **kwargs)
