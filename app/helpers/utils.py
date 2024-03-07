import re
from functools import wraps
from fastapi import Header, status, HTTPException
from app.settings import OWNER_PASSWORD


def extract_dates(string):
    pattern = r"Posted (\d{2}\.\d{2}\.\d{4})(?:Renewed (\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}))?"
    matches = re.search(pattern, string)
    
    if matches:
        creating_date = matches.group(1)
        updating_date = matches.group(2)
        
        if updating_date is None:
            return {"creating": creating_date, "updating": None}
        else:
            return {"creating": creating_date, "updating": updating_date}
    
    return None


def is_signed_middleware(endpoint):
    @wraps(endpoint)
    async def middleware(*args, authorization: str, **kwargs):
        if authorization != OWNER_PASSWORD:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return await endpoint(*args, authorization=authorization, **kwargs)
    return middleware
