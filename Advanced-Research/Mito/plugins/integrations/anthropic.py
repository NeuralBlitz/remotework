"""
Anthropic Plugin
Claude AI completions and messages API.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.anthropic")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def _client():
    import os
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("anthropic not installed. Run: pip install anthropic")
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


def anthropic_complete_cmd(prompt: str = "", model: str = "claude-sonnet-4-20250514",
                           max_tokens: int = 1024) -> Dict:
    client = _client()
    response = client.messages.create(model=model, max_tokens=max_tokens,
                                     messages=[{"role": "user", "content": prompt}])
    return {"response": response.content[0].text, "model": model, "usage": {"input": response.usage.input_tokens, "output": response.usage.output_tokens}}


def anthropic_messages_cmd(messages: str = "", model: str = "claude-sonnet-4-20250514",
                            system: str = "", max_tokens: int = 1024, temperature: float = 1.0) -> Dict:
    import json
    msgs = json.loads(messages)
    client = _client()
    kwargs = {"model": model, "max_tokens": max_tokens, "messages": msgs}
    if system:
        kwargs["system"] = system
    if temperature != 1.0:
        kwargs["temperature"] = temperature
    response = client.messages.create(**kwargs)
    return {"response": response.content[0].text, "model": model, "stop_reason": response.stop_reason}


def anthropic_count_tokens_cmd(text: str = "", model: str = "claude-sonnet-4-20250514") -> Dict:
    client = _client()
    count = client.count_tokens(text)
    return {"text_length": len(text), "tokens": count, "model": model}


def register(plugin):
    plugin.register_command("complete", anthropic_complete_cmd)
    plugin.register_command("messages", anthropic_messages_cmd)
    plugin.register_command("count_tokens", anthropic_count_tokens_cmd)


PLUGIN_METADATA = {
    "name": "anthropic", "version": "1.0.0",
    "description": "Anthropic Claude AI completions and messages API",
    "author": "Mito Team", "license": "MIT",
    "tags": ["anthropic", "ai", "claude", "llm"],
    "dependencies": ["anthropic"], "permissions": ["anthropic_access"],
    "min_mito_version": "1.0.1",
}

anthropic_plugin = {"metadata": PLUGIN_METADATA, "register": register}
