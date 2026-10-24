"""Tests for API server"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestServerImports:
    def test_api_import(self):
        from server.api import app, VERSION
        assert VERSION == "1.0.0"
        assert app.title == "Mito API"

    def test_request_models(self):
        from server.api import (
            GenerateRequest, SummarizeRequest, TranslateRequest,
            QARequest, SentimentRequest, EmbedRequest
        )
        req = GenerateRequest(prompt="Hello")
        assert req.prompt == "Hello"
        assert req.model == "gpt2"
        assert req.max_tokens == 100


class TestCLI:
    def test_mito_cli_exists(self):
        mito_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mito"
        )
        assert os.path.isfile(mito_path)
        with open(mito_path) as f:
            content = f.read()
        assert "VERSION" in content
        assert "argparse" in content
