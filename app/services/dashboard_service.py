import calendar
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.services.firestore_service import FireStoreService


class DashboardService:
    def __init__(self):
        self.db = FireStoreService()
        self.collection_name = 'appContentDB'

    @staticmethod
    def get_date_range(filter_type: str):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        if filter_type == 'today':
            start_date = today
        elif filter_type == 'week':
            start_date = today - timedelta(days=7)
        elif filter_type == 'month':
            start_date = today - timedelta(days=30)
        elif filter_type == 'year':
            start_date = today - timedelta(days=365)
        else:
            raise ValueError(f"Invalid filter_type: {filter_type}")

        return start_date, end_date
    
    @staticmethod
    def group_by_date(data: List[Dict], date_field: str = 'dateUpdated', date_format: str = '%Y-%m-%dT%H:%M:%S.%f%z', group_by: str = 'day') -> List[Dict]:
        grouped_data = defaultdict(lambda: {'value': None, 'count': 0})
        
        for item in data:
            if date_field in item:
                date_str = item[date_field]
                try:
                    date_obj = datetime.strptime(date_str, date_format)
                    if group_by == 'today':
                        date_key = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                    elif group_by == 'week':
                        date_key = date_obj.strftime('%Y-%m-%d')
                    elif group_by == 'month':
                        date_key = date_obj.strftime('%Y-%m-%d')
                    elif group_by == 'year':
                        date_key = date_obj.strftime('%Y-%m')
                    else:
                        raise ValueError(f"Invalid group_by value: {group_by}. Must be 'day', 'month', or 'year'.")
                    grouped_data[date_key]['value'] = date_key
                    grouped_data[date_key]['count'] += 1
                except ValueError:
                    print(f"Invalid date format for {date_str}, expected format {date_format}")
                    continue

        return list(grouped_data.values())
    
    async def get_card_values(self):
        total_data = await self.db.fetch_all_data(collection_name=self.collection_name)

        active_count = 0
        inactive_count = 0
        featured_count = 0

        for data in total_data:
            if data.get('active', False):
                active_count += 1
            else:
                inactive_count += 1
            if data.get('featured', False):
                featured_count += 1

        result = [
            {'name': 'total_count', 'count': len(total_data)},
            {'name': 'active_count', 'count': active_count},
            {'name': 'inactive_count', 'count': inactive_count},
            {'name': 'featured_count', 'count': featured_count}
        ]
        
        return result

    async def get_line_chart_values(self, filter_type: str):
        try:
            if not filter_type:
                raise HTTPException(detail="Month not specified", status_code=404)
            start_date, end_date = self.get_date_range(filter_type)
            data = await self.db.fetch_all_data(collection_name=self.collection_name, from_date=start_date, end_date=end_date)
            return self.group_by_date(data, group_by=filter_type)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
