#!/bin/bash
# Setup script for Llama CLI Assistant

set -e

echo "=== Llama CLI Assistant Setup ==="
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python found"
    python3 --version
else
    echo "✗ Python not found"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null || true

# Try to install optional dependencies
echo "Installing optional AI dependencies..."
pip install -q llama-cpp-python 2>/dev/null || true

# Build C++ CLI
echo ""
echo "Building C++ CLI..."
make clean 2>/dev/null || true
make

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Download a model: ./scripts/download-model.sh <url> <name>"
echo "  2. Start chatting: ./scripts/chat.sh model.gguf"
echo "  3. Or use Python: python -m python.ai.llama model.gguf \"your prompt\""
echo ""
echo "Run './llama-cli -h' for CLI options"
