"""
Application configuration settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Security
API_KEY = os.environ.get("TRANSLATOR_API_KEY", "")

# Translation Model
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# Language code mapping to NLLB codes
LANG_CODES = {
    "gn": "grn_Latn",  # Guaraní
    "es": "spa_Latn"   # Spanish
}

# Rate Limiting
RATE_LIMIT = "10/minute"

# CORS Settings
ALLOWED_ORIGINS = ["https://your-vercel.app"]
ALLOWED_METHODS = ["POST"]
ALLOWED_HEADERS = ["*"]
