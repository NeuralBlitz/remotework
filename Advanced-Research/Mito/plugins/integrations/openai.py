"""
OpenAI Plugin
Chat completions, embeddings, image generation, and moderation.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.openai")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def _client():
    import os
    if not OPENAI_AVAILABLE:
        raise ImportError("openai not installed. Run: pip install openai")
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def openai_chat_cmd(model: str = "gpt-4o-mini", messages: str = "", temperature: float = 0.7,
                    max_tokens: int = 1000) -> Dict:
    import json
    msgs = json.loads(messages) if messages.startswith("[") else [{"role": "user", "content": messages}]
    client = _client()
    response = client.chat.completions.create(model=model, messages=msgs, temperature=temperature, max_tokens=max_tokens)
    return {"response": response.choices[0].message.content, "model": model, "usage": dict(response.usage)}


def openai_embeddings_cmd(input_text: str = "", model: str = "text-embedding-3-small") -> Dict:
    client = _client()
    response = client.embeddings.create(input=input_text, model=model)
    return {"embedding": response.data[0].embedding, "model": model, "dimensions": len(response.data[0].embedding)}


def openai_image_generate_cmd(prompt: str = "", model: str = "dall-e-3", size: str = "1024x1024",
                               quality: str = "standard") -> Dict:
    client = _client()
    response = client.images.generate(prompt=prompt, model=model, size=size, quality=quality, n=1)
    return {"url": response.data[0].url, "revised_prompt": response.data[0].revised_prompt}


def openai_transcription_cmd(file_path: str = "", model: str = "whisper-1") -> Dict:
    client = _client()
    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(model=model, file=f)
    return {"text": response.text, "model": model}


def openai_moderation_cmd(input_text: str = "", model: str = "omni-moderation-latest") -> Dict:
    client = _client()
    result = client.moderations.create(input=input_text, model=model)
    r = result.results[0]
    flagged = {cat: getattr(r.categories, cat) for cat in dir(r.categories) if not cat.startswith("_")}
    return {"flagged": r.flagged, "categories": flagged}


def openai_completion_cmd(prompt: str = "", model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 500) -> Dict:
    client = _client()
    response = client.completions.create(model=model, prompt=prompt, max_tokens=max_tokens)
    return {"text": response.choices[0].text, "model": model}


def register(plugin):
    plugin.register_command("chat", openai_chat_cmd)
    plugin.register_command("embeddings", openai_embeddings_cmd)
    plugin.register_command("image_generate", openai_image_generate_cmd)
    plugin.register_command("transcription", openai_transcription_cmd)
    plugin.register_command("moderation", openai_moderation_cmd)
    plugin.register_command("completion", openai_completion_cmd)


PLUGIN_METADATA = {
    "name": "openai", "version": "1.0.0",
    "description": "OpenAI chat, embeddings, image generation, and moderation",
    "author": "Mito Team", "license": "MIT",
    "tags": ["openai", "ai", "gpt", "embeddings", "images"],
    "dependencies": ["openai"], "permissions": ["openai_access"],
    "min_mito_version": "1.0.1",
}

openai_plugin = {"metadata": PLUGIN_METADATA, "register": register}
