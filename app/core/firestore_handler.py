import json
import firebase_admin
from fastapi import HTTPException
from firebase_admin import firestore, credentials
from datetime import datetime
from google.cloud.firestore_v1 import FieldFilter, aggregation
from google.api_core.exceptions import FailedPrecondition
from app.core.logger import LoggerConfig

logger = LoggerConfig(__name__).get_logger()

cred = credentials.Certificate("app/zysec-app.json")
firebase_admin.initialize_app(cred)


class FirestoreHandler:
    def __init__(self):
        self.db = firestore.client()
    
    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d') if isinstance(date_str, str) else date_str

    def _convert_to_serializable(self, value):
        if isinstance(value, firestore.DocumentReference):
            return {'id': value.id, 'path': value.path}
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, dict):
            return {k: self._convert_to_serializable(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._convert_to_serializable(v) for v in value]
        else:
            return value

    def _doc_to_dict(self, doc):
        data = doc.to_dict()
        data['id'] = doc.id
        return self._convert_to_serializable(data)

    def fetch_data(self, collection_name, date_filter=None, post_type=None, title_search=None, email_filter=None,
                   page_size=50, page=1, category_filter=None, tags_filter=None, date_filter_type=None, doc_id=None):
        try:
            query = self.db.collection(collection_name)
            if doc_id:
                query = query.where(filter=FieldFilter('id', '==', doc_id))
            if date_filter:
                date_filter_parsed = self._parse_date(date_filter)
                
                if date_filter_type:
                    if date_filter_type == 'less_than':
                        query = query.where(filter=FieldFilter('dateUpdated', '<=', date_filter_parsed))
                    elif date_filter_type == 'greater_than':
                        query = query.where(filter=FieldFilter('dateUpdated', '>=', date_filter_parsed))
                else:
                    query = query.where(filter=FieldFilter('dateUpdated', '>=', date_filter_parsed))
            if title_search:
                query = query.where(filter=FieldFilter('title', '>=', title_search)).where('title', '<=', title_search + '\uf8ff')
            if email_filter:
                query = query.where(filter=FieldFilter('email', '==', email_filter))
            if category_filter:
                query = query.where(filter=FieldFilter('category', '==', category_filter))
            if tags_filter:
                query = query.where(filter=FieldFilter('tags', 'array_contains_any', tags_filter))
            if post_type:
                if isinstance(post_type, str):
                    query = query.where('type', '==', post_type)
                elif isinstance(post_type, list):
                    query = query.where('type', 'in', post_type)
                else:
                    raise HTTPException(status_code=400, detail="Invalid post_type parameter")
            
            offset = (page - 1) * page_size
            
            query = query.order_by('dateUpdated', direction='DESCENDING').offset(offset).limit(page_size)
            docs = query.stream()

            results = [self._doc_to_dict(doc) for doc in docs]
            return results

        except FailedPrecondition as e:
            logger.error(f'Firestore requires a composite index for this query: {str(e)}')
            raise HTTPException(status_code=400, detail="Firestore requires a composite index for this query. Please create the required index in the Firebase Console.")

        except Exception as e:
            logger.error(f'Exception occured {str(e)}')
            raise e

    def fetch_all_data(self, collection_name, from_date=None, end_date=None):
        try:
            query = self.db.collection(collection_name)
            if from_date and end_date:
                query = query.where(filter=FieldFilter('dateUpdated', '>=', from_date)).where(filter=FieldFilter('dateUpdated', '<=', end_date))
            
            docs = query.stream()

            results = [self._doc_to_dict(doc) for doc in docs]
            return results

        except Exception as e:
            logger.error(f'Exception occured {str(e)}')
            raise e

    def add_data(self, collection_name, data):
        doc_ref, _ = self.db.collection(collection_name).add(data)
        return doc_ref.id

    def update_data(self, collection_name, doc_id, data):
        self.db.collection(collection_name).document(doc_id).update(data)

    def delete_data(self, collection_name, doc_id):
        self.db.collection(collection_name).document(doc_id).delete()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, firestore.DocumentReference):
            return {'id': obj.id, 'path': obj.path}
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
