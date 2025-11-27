from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Translator GN<->ES")

# =========================
#  Security
# =========================
API_KEY = os.environ.get("TRANSLATOR_API_KEY", "")
if not API_KEY:
    print("⚠ WARNING: No API key set (TRANSLATOR_API_KEY)")

def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# =========================
#   Rate Limiting
# =========================
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# =========================
#   CORS (only your Next.js)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-proyecto.vercel.app"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# =========================
#   Translation Model
# =========================
MODEL = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)

# Language code mapping to NLLB codes
LANG_CODES = {
    "gn": "grn_Latn",  # Guaraní
    "es": "spa_Latn"   # Spanish
}

# =========================
#   Input Validation
# =========================
class TranslateRequest(BaseModel):
    text: str
    source_lang: str = Field(pattern="^(gn|es)$")
    target_lang: str = Field(pattern="^(gn|es)$")


@app.post("/translate")
@limiter.limit("10/minute")
def translate(request: Request, req: TranslateRequest, _: None = Depends(verify_api_key)):
    # Convert language codes to NLLB format
    src_lang = LANG_CODES[req.source_lang]
    tgt_lang = LANG_CODES[req.target_lang]
    
    # Set source language
    tokenizer.src_lang = src_lang
    inputs = tokenizer(req.text, return_tensors="pt")

    # Get target language token ID
    tgt_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)
    
    generated = model.generate(
        **inputs,
        forced_bos_token_id=tgt_token_id
    )

    result = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

    return {"translated_text": result}

