from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY = "your_super_secret_api_key"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
