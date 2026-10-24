#!/bin/bash
# Interactive chat with Llama model

MODEL="${1:-model.gguf}"
CTX_SIZE="${2:-2048}"
THREADS="${3:-4}"

# Check if model exists
if [ ! -f "$MODEL" ]; then
    echo "Error: Model file '$MODEL' not found"
    echo "Download a model first: ./scripts/download-model.sh"
    exit 1
fi

echo "Starting Llama Chat..."
echo "Model: $MODEL"
echo "Context: $CTX_SIZE, Threads: $THREADS"
echo "Type 'quit' to exit"
echo ""

# Try Python wrapper first (if installed)
if python3 -c "import python.ai.llama" 2>/dev/null; then
    python3 -c "
from python.ai.llama import LlamaModel
import sys

model = LlamaModel('$MODEL', n_ctx=$CTX_SIZE, n_threads=$THREADS, verbose=False)
model.load()

messages = []
print('Llama Chat Ready!')
print('(Using llama-cpp-python)')

while True:
    try:
        user_input = input('> ')
        if user_input.lower() in ['quit', 'exit']:
            break
        if not user_input.strip():
            continue
            
        messages.append({'role': 'user', 'content': user_input})
        result = model.generate(
            f\"User: {user_input}\n\nAssistant:\",
            max_tokens=256,
            temperature=0.7
        )
        response = result['choices'][0]['text'].strip()
        messages.append({'role': 'assistant', 'content': response})
        print(f'Assistant: {response}')
        print()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f'Error: {e}')

print('Goodbye!')
"
else
    echo "llama-cpp-python not installed, using stub CLI"
    ./llama-cli -m "$MODEL" -i -c "$CTX_SIZE" -t "$THREADS"
fi
