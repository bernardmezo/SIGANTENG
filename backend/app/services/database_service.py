import os
from supabase import create_client, Client

from app.core.config import settings

class SupabaseService:
    def __init__(self):
        self.supabase_url: str = settings.SUPABASE_URL
        self.supabase_key: str = settings.SUPABASE_KEY
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    async def insert_data(self, table_name: str, data: dict):
        try:
            response = self.client.table(table_name).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error inserting data into Supabase: {e}")
            return None

    async def fetch_data(self, table_name: str, query_params: dict = None):
        try:
            query = self.client.table(table_name).select("*")
            if query_params:
                for key, value in query_params.items():
                    query = query.eq(key, value)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error fetching data from Supabase: {e}")
            return None
