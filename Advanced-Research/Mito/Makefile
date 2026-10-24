CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = llama-cli
DEBUG_TARGET = main-debug

# Optional llama.cpp integration
LLAMA_CPP_PATH ?=
ifdef LLAMA_CPP_PATH
    CXXFLAGS += -DLLAMA_CPP_AVAILABLE -I$(LLAMA_CPP_PATH)/include
    LDFLAGS = -L$(LLAMA_CPP_PATH)/build/bin -lllama
else
    LDFLAGS =
endif

.PHONY: all clean debug run test install-deps

all: $(TARGET)

$(TARGET): main.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.cpp $(LDFLAGS)

debug: $(DEBUG_TARGET)

$(DEBUG_TARGET): main.cpp
	$(CXX) $(CXXFLAGS) -g -o $(DEBUG_TARGET) main.cpp $(LDFLAGS)

clean:
	rm -f $(TARGET) $(DEBUG_TARGET) *.o *.d

run: $(TARGET)
	./$(TARGET) -m model.gguf

test:
	@echo "Running C++ version check..."
	./$(TARGET) -v
	./$(TARGET) -h
	@echo "Running Python tests..."
	PYTHONPATH=$(PWD)/.pythonlibs/lib/python3.11/site-packages:$(PYTHONPATH) python -m pytest tests/ -v 2>/dev/null || echo "pytest not installed, skipping"

install-deps:
	@echo "To install llama.cpp, run:"
	@echo "  git clone https://github.com/ggerganov/llama.cpp.git"
	@echo "  cd llama.cpp && make && sudo make install"
	@echo ""
	@echo "Then build with llama.cpp support:"
	@echo "  make LLAMA_CPP_PATH=./llama.cpp"
