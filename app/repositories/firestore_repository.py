from app.services.firestore_service import FireStoreService
from app.repositories.base import UserRepository

class FirestoreUserRepository(UserRepository):
    def __init__(self):
        self.db = FireStoreService()
    
    async def fetch_user_by_email(self, email: str):
        return self.db.fetch_data('tabUsers', email_filter=email)
