"""
Mito API Server
FastAPI server for Mito AI toolkit
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware
from config.observability import RateLimiter, APIKeyManager, track_metrics, get_metrics
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import tempfile
import os
import base64

VERSION = "1.0.0"

app = FastAPI(
    title="Mito API",
    description="The Powerhouse AI Toolkit API",
    version=VERSION
)


def run_server(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(app, host=host, port=port)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_ENV = os.getenv("MITO_API_KEY")
API_KEY_HEADER = "X-API-Key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)
JWT_ISSUER = os.getenv("MITO_JWT_ISSUER")
JWT_AUDIENCE = os.getenv("MITO_JWT_AUDIENCE")
JWT_PUBLIC_KEY = os.getenv("MITO_JWT_PUBLIC_KEY")
JWT_PRIVATE_KEY = os.getenv("MITO_JWT_PRIVATE_KEY")
JWT_SECRET = os.getenv("MITO_JWT_SECRET")
JWT_PASSWORD = os.getenv("MITO_JWT_PASSWORD")
JWT_USERS = os.getenv("MITO_JWT_USERS")
JWT_REFRESH_TTL = int(os.getenv("MITO_JWT_REFRESH_TTL", "86400"))
api_keys = APIKeyManager()
limiter = RateLimiter(rate=int(os.getenv("MITO_RATE_LIMIT", "120")), period=60)
if API_KEY_ENV:
    api_keys.create_key("env-key", rate_limit=limiter.rate)
    # replace placeholder key with actual env value
    api_keys.keys[API_KEY_ENV] = api_keys.keys.pop(list(api_keys.keys.keys())[0])

def require_api_key(request: Request):
    if API_KEY_ENV:
        key = request.headers.get(API_KEY_HEADER)
        if not key or not api_keys.validate_key(key):
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
        return key
    return None

def enforce_rate_limit(request: Request):
    key = request.headers.get(API_KEY_HEADER) or "anonymous"
    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return None

def validate_jwt(token: Optional[str] = Depends(oauth2_scheme)):
    if API_KEY_ENV is None:
        return token  # allow passthrough when API key is disabled
    if not token:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    try:
        if JWT_PUBLIC_KEY:
            return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=["RS256"], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
        if JWT_SECRET:
            return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    return token


def _verify_credentials(username: str, password: str) -> bool:
    if JWT_USERS:
        try:
            users = json.loads(JWT_USERS)
            return users.get(username) == password
        except Exception:
            return False
    if JWT_PASSWORD:
        return password == JWT_PASSWORD
    return True  # allow when no credential config provided


def _issue_token(sub: str, scopes, ttl: int = None):
    now = int(time.time())
    exp = now + (ttl or int(os.getenv("MITO_JWT_TTL", "3600")))
    payload = {"sub": sub, "scope": scopes, "iat": now, "exp": exp}
    if JWT_ISSUER:
        payload["iss"] = JWT_ISSUER
    if JWT_AUDIENCE:
        payload["aud"] = JWT_AUDIENCE
    if JWT_PRIVATE_KEY:
        token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm="RS256")
    elif JWT_SECRET:
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    else:
        raise HTTPException(status_code=501, detail="JWT signing not configured; set MITO_JWT_PRIVATE_KEY or MITO_JWT_SECRET")
    return token, exp


class GenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "gpt2"
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7


class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 130


class TranslateRequest(BaseModel):
    text: str
    model: Optional[str] = "Helsinki-NLP/opus-mt-en-es"


class QARequest(BaseModel):
    question: str
    context: str


class SentimentRequest(BaseModel):
    text: str


class EmbedRequest(BaseModel):
    text: str
    model: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"



class TTSRequest(BaseModel):
    text: str
    model: Optional[str] = "tts_models/en/ljspeech/glow-tts"

@app.get("/")
def root():
    return {
        "name": "Mito API",
        "version": VERSION,
        "status": "running"
    }

@app.post("/token")
async def token_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), api_key: str = Depends(require_api_key)):
    """Issue JWT bearer tokens after simple credential validation."""
    if not _verify_credentials(form_data.username, form_data.password or ""):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token, exp = _issue_token(form_data.username, form_data.scopes)
    return {"access_token": token, "token_type": "bearer", "expires_in": exp - int(time.time())}
@app.post("/token/refresh")
async def token_refresh(claims: dict = Depends(validate_jwt), api_key: str = Depends(require_api_key)):
    """Refresh an existing JWT (requires valid bearer token)."""
    sub = claims.get("sub") if isinstance(claims, dict) else None
    scopes = claims.get("scope", []) if isinstance(claims, dict) else []
    if not sub:
        raise HTTPException(status_code=400, detail="Missing subject in token")
    token, exp = _issue_token(sub, scopes, ttl=JWT_REFRESH_TTL)
    return {"access_token": token, "token_type": "bearer", "expires_in": exp - int(time.time())}



@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "llama", "description": "Llama LLM inference"},
            {"name": "textgen", "description": "Text generation"},
            {"name": "summarize", "description": "Text summarization"},
            {"name": "translate", "description": "Translation"},
            {"name": "qa", "description": "Question answering"},
            {"name": "sentiment", "description": "Sentiment analysis"},
            {"name": "embed", "description": "Text embeddings"},
            {"name": "ocr", "description": "OCR text recognition"},
            {"name": "classify", "description": "Image classification"},
            {"name": "speech", "description": "Speech recognition"},
            {"name": "tts", "description": "Text-to-speech"},
        ]
    }

@app.get("/metrics")
def metrics():
    return Response(get_metrics(), media_type="text/plain; version=0.0.4; charset=utf-8")



@app.post("/generate")
@track_metrics(endpoint="generate", method="POST")
def generate(req: GenerateRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai import TextGenerator
        
        gen = TextGenerator(model_name=req.model)
        result = gen.generate_single(req.prompt, max_length=req.max_tokens)
        
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize")
@track_metrics(endpoint="summarize", method="POST")
def summarize(req: SummarizeRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.summarize import Summarizer
        
        summ = Summarizer()
        result = summ.summarize(req.text, max_length=req.max_length)
        
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate")
@track_metrics(endpoint="translate", method="POST")
def translate(req: TranslateRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.translate import Translator
        
        trans = Translator(model_name=req.model)
        result = trans.translate(req.text)
        
        return {"translation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/qa")
@track_metrics(endpoint="qa", method="POST")
def question_answer(req: QARequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.qa import QAModel
        
        qa = QAModel()
        result = qa.answer(req.question, req.context)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sentiment")
@track_metrics(endpoint="sentiment", method="POST")
def sentiment(req: SentimentRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.sentiment import quick_sentiment, quick_emotion
        
        sent = quick_sentiment(req.text)
        emotion = quick_emotion(req.text)
        
        return {
            "sentiment": sent["label"],
            "score": sent["score"],
            "emotion": emotion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embed")
@track_metrics(endpoint="embed", method="POST")
def embed(req: EmbedRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.embeddings import Embedder
        
        embedder = Embedder(model_name=req.model)
        result = embedder.embed(req.text)
        
        return {"embedding": result.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/ocr")
@track_metrics(endpoint="ocr", method="POST")
async def ocr(file: UploadFile = File(...), api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    tmp_path = None
    try:
        from python.ai.ocr import OCREngine
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        engine = OCREngine()
        results = engine.read_text(tmp_path)
        return {"text": [r["text"] for r in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/classify")
@track_metrics(endpoint="classify", method="POST")
async def classify(file: UploadFile = File(...), api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    tmp_path = None
    try:
        from python.ai.image_classify import ImageClassifier
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        classifier = ImageClassifier()
        results = classifier.classify(tmp_path)
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/speech")
@track_metrics(endpoint="speech", method="POST")
async def speech(file: UploadFile = File(...), api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    tmp_path = None
    try:
        from python.ai.speech import SpeechRecognizer
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        recognizer = SpeechRecognizer()
        result = recognizer.get_text(tmp_path)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/tts")
@track_metrics(endpoint="tts", method="POST")
def tts(req: TTSRequest, api_key: str = Depends(require_api_key), _rl: None = Depends(enforce_rate_limit), token: str = Depends(validate_jwt)):
    try:
        from python.ai.tts import TTSEngine
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_path = tmp.name
        try:
            engine = TTSEngine(model_name=req.model)
            output_path = engine.speak(req.text, output_path=tmp_path)
            with open(output_path, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            return {"audio_base64": audio_b64, "format": "wav"}
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    run_server()
