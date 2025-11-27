"""
Security utilities for API authentication.
"""
from fastapi import HTTPException, Request
from config import API_KEY


def verify_api_key(request: Request):
    """
    Verify that the request contains a valid API key.
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
