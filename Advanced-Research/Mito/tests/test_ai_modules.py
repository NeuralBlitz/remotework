"""Tests for AI modules - import and structure validation"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports:
    def test_ocr_import(self):
        from python.ai.ocr import OCREngine, quick_ocr
        assert callable(quick_ocr)

    def test_textgen_import(self):
        from python.ai.textgen import TextGenerator, quick_generate
        assert callable(quick_generate)

    def test_sentiment_import(self):
        from python.ai.sentiment import SentimentAnalyzer, EmotionDetector, quick_sentiment, quick_emotion
        assert callable(quick_sentiment)
        assert callable(quick_emotion)

    def test_embeddings_import(self):
        from python.ai.embeddings import Embedder, quick_embed
        assert callable(quick_embed)

    def test_speech_import(self):
        from python.ai.speech import SpeechRecognizer, quick_transcribe
        assert callable(quick_transcribe)

    def test_tts_import(self):
        from python.ai.tts import TTSEngine, quick_speak
        assert callable(quick_speak)

    def test_summarize_import(self):
        from python.ai.summarize import Summarizer, quick_summarize
        assert callable(quick_summarize)

    def test_qa_import(self):
        from python.ai.qa import QAModel, quick_qa
        assert callable(quick_qa)

    def test_translate_import(self):
        from python.ai.translate import Translator, quick_translate
        assert callable(quick_translate)

    def test_detect_import(self):
        from python.ai.detect import ObjectDetector, quick_detect
        assert callable(quick_detect)

    def test_segment_import(self):
        from python.ai.segment import Segmenter, quick_segment
        assert callable(quick_segment)

    def test_classify_import(self):
        from python.ai.image_classify import ImageClassifier, quick_classify
        assert callable(quick_classify)

    def test_llama_import(self):
        from python.ai.llama import LlamaModel, load_model, quick_generate
        assert callable(load_model)
        assert callable(quick_generate)

    def test_package_init(self):
        from python.ai import __version__, __all__
        assert __version__ == "1.0.0"
        assert len(__all__) > 0


class TestAgents:
    def test_agent_import(self):
        from agents import Agent, ReActAgent, MultiAgentSystem, AgentState
        assert AgentState.IDLE.value == "idle"

    def test_rag_import(self):
        from agents.rag import RAG, Document, VectorStore
        doc = Document("test content", {"source": "test"})
        assert doc.content == "test content"
        assert doc.metadata["source"] == "test"


class TestConfig:
    def test_config_import(self):
        from config import MitoConfig, ConfigManager, ModelConfig, APIConfig
        config = MitoConfig()
        assert config.version == "1.0.0"
        assert config.model.default_model == "gpt2"

    def test_logging_import(self):
        from config.logging import MitoLogger, get_logger
        logger = get_logger("test")
        assert logger is not None

    def test_observability_import(self):
        from config.observability import RateLimiter, APIKeyManager
        limiter = RateLimiter(rate=10, period=60)
        assert limiter.allow("test") is True

        manager = APIKeyManager()
        key = manager.create_key("test")
        assert manager.validate_key(key) is True


class TestDataStore:
    def test_store_import(self):
        from data.store import SQLiteStore, InMemoryCache, DiskCache

    def test_memory_cache(self):
        from data.store import InMemoryCache
        cache = InMemoryCache(max_size=10)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.has("key1") is True
        cache.delete("key1")
        assert cache.has("key1") is False


class TestPipeline:
    def test_pipeline_import(self):
        from pipeline import Pipeline, PipelineStep, PipelineStepType, Chain, Parallel

    def test_chain(self):
        from pipeline import Chain
        chain = Chain()
        chain.add(str.upper)
        chain.add(lambda x: x + "!")
        result = chain.execute("hello")
        assert result == "HELLO!"


class TestPlugins:
    def test_plugin_import(self):
        from plugins import (
            PluginManager, Plugin, PluginMetadata, PluginState,
            EventBus, SecuritySandbox, Permission
        )
        assert PluginState.DISCOVERED.value == "discovered"


class TestUtils:
    def test_utils_import(self):
        from utils import sanitize_filename, slugify, truncate, batch, flatten
        assert sanitize_filename("test@file!.txt") == "testfiletxt"
        assert slugify("Hello World!") == "hello-world"
        assert truncate("hello world", 5) == "he..."

    def test_batch(self):
        from utils import batch
        result = batch([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_flatten(self):
        from utils import flatten
        result = flatten([[1, 2], [3, [4, 5]], 6])
        assert result == [1, 2, 3, 4, 5, 6]


class TestModels:
    def test_model_manager_import(self):
        from utils.models import ModelManager, ModelType, ModelStatus
        assert ModelType.LLAMA.value == "llama"
