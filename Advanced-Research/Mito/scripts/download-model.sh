#!/bin/bash
# Download a Llama model

MODEL_DIR="${MODEL_DIR:-.}"
MODEL_URL="${1:-}"
MODEL_NAME="${2:-llama-7b.gguf}"

if [ -z "$MODEL_URL" ]; then
    echo "Usage: $0 <model_url> [output_name]"
    echo ""
    echo "Example URLs:"
    echo "  HuggingFace direct links to GGUF files"
    echo ""
    exit 1
fi

echo "Downloading $MODEL_NAME from $MODEL_URL..."
echo "This may take a while for large models."

mkdir -p "$MODEL_DIR"

if command -v curl &> /dev/null; then
    curl -L -o "$MODEL_DIR/$MODEL_NAME" "$MODEL_URL"
elif command -v wget &> /dev/null; then
    wget -O "$MODEL_DIR/$MODEL_NAME" "$MODEL_URL"
else
    echo "Error: Neither curl nor wget found"
    exit 1
fi

if [ -f "$MODEL_DIR/$MODEL_NAME" ]; then
    SIZE=$(du -h "$MODEL_DIR/$MODEL_NAME" | cut -f1)
    echo "Success! Model saved to $MODEL_DIR/$MODEL_NAME ($SIZE)"
else
    echo "Download failed"
    exit 1
fi
