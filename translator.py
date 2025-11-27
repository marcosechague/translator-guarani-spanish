"""
Translation service using NLLB-200 model.
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import MODEL_NAME, LANG_CODES


class TranslationService:
    """Service for handling translation operations."""
    
    def __init__(self):
        """Initialize the translation model and tokenizer."""
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (gn or es)
            target_lang: Target language code (gn or es)
            
        Returns:
            Translated text
        """
        # Convert language codes to NLLB format
        src_lang = LANG_CODES[source_lang]
        tgt_lang = LANG_CODES[target_lang]
        
        # Set source language
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Get target language token ID
        tgt_token_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        
        # Generate translation
        generated = self.model.generate(
            **inputs,
            forced_bos_token_id=tgt_token_id
        )
        
        # Decode result
        result = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        return result


# Singleton instance
translation_service = TranslationService()
