# Translator GN ↔ ES

A FastAPI-based translation API for Guaraní (gn) and Spanish (es) using the NLLB-200 model from Meta.

## Features

- 🔄 Bidirectional translation between Guaraní and Spanish
- 🔒 API key authentication
- ⏱️ Rate limiting (10 requests/minute)
- 🚀 Fast inference with transformers
- 🐳 Docker support

## Requirements

- Python 3.10+
- pip

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd translator-gn-es
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```bash
TRANSLATOR_API_KEY=your_secret_key_here
```

Replace `your_secret_key_here` with a secure API key of your choice.

## Usage

### Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Endpoint

**POST** `/translate`

**Headers:**

- `x-api-key`: Your API key (from `.env`)
- `Content-Type`: `application/json`

**Request Body:**

```json
{
  "text": "Mba'éichapa nde?",
  "source_lang": "gn",
  "target_lang": "es"
}
```

**Response:**

```json
{
  "translated_text": "¿Cómo estás?"
}
```

### Example cURL requests

**Guaraní to Spanish:**

```bash
curl -X POST "http://127.0.0.1:8000/translate" \
  -H "x-api-key: your_secret_key_here" \
  -H "Content-Type: application/json" \
  -d '{"text":"Mba'\''éichapa nde?", "source_lang":"gn", "target_lang":"es"}'
```

**Spanish to Guaraní:**

```bash
curl -X POST "http://127.0.0.1:8000/translate" \
  -H "x-api-key: your_secret_key_here" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola, ¿cómo estás?", "source_lang":"es", "target_lang":"gn"}'
```

## Docker

### Build the image

```bash
docker build -t translator-gn-es .
```

### Run the container

```bash
docker run -d -p 8000:8000 -e TRANSLATOR_API_KEY=your_secret_key_here translator-gn-es
```

## Project Structure

```
translator-gn-es/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .env                # Environment variables (not versioned)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

### Rate Limiting

Default: 10 requests per minute per IP

To modify, edit the decorator in `main.py`:

```python
@limiter.limit("10/minute")  # Change as needed
```

### CORS

By default, CORS is configured for a specific origin. Update in `main.py`:

```python
allow_origins=["https://your-project.vercel.app"],
```

## Model

This project uses the **facebook/nllb-200-distilled-600M** model, which supports 200 languages including:

- Guaraní (`grn_Latn`)
- Spanish (`spa_Latn`)

The model is downloaded automatically on first run and cached locally.

## Security

- Never commit your `.env` file
- Use strong API keys in production
- Consider using HTTPS in production
- Adjust rate limits based on your needs

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
