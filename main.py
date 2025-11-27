"""
FastAPI application for Guaraní-Spanish translation.
"""
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import API_KEY, RATE_LIMIT, ALLOWED_ORIGINS, ALLOWED_METHODS, ALLOWED_HEADERS
from models import TranslateRequest, TranslateResponse
from security import verify_api_key
from translator import translation_service


# Initialize FastAPI app
app = FastAPI(
    title="Translator GN<->ES",
    description="Translation API for Guaraní and Spanish using NLLB-200",
    version="1.0.0"
)

# Security check
if not API_KEY:
    print("⚠ WARNING: No API key set (TRANSLATOR_API_KEY)")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Translator GN<->ES",
        "version": "1.0.0",
        "supported_languages": ["gn", "es"]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/translate", response_model=TranslateResponse)
@limiter.limit(RATE_LIMIT)
async def translate(
    request: Request,
    req: TranslateRequest,
    _: None = Depends(verify_api_key)
) -> TranslateResponse:
    """
    Translate text between Guaraní and Spanish.
    
    Args:
        request: FastAPI request object (required for rate limiting)
        req: Translation request with text and language codes
        
    Returns:
        Translation response with translated text
    """
    result = translation_service.translate(
        text=req.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang
    )
    
    return TranslateResponse(translated_text=result)

