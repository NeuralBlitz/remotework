#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <algorithm>

#ifdef LLAMA_CPP_AVAILABLE
#include "llama.h"
#endif

namespace {
    const std::string VERSION = "1.0.0";

    void printUsage(const std::string& progName) {
        std::cout << "Mito CLI v" << VERSION << "\n\n";
        std::cout << "Usage: " << progName << " [options]\n\n";
        std::cout << "Options:\n";
        std::cout << "  -m, --model <file>     Path to GGUF model file (required)\n";
        std::cout << "  -p, --prompt <text>    Input prompt\n";
        std::cout << "  -i, --interactive      Start interactive mode\n";
        std::cout << "  -t, --threads <n>      Number of threads (default: 4)\n";
        std::cout << "  -c, --context <n>      Context size (default: 512)\n";
        std::cout << "  --temp <n>             Temperature (default: 0.7)\n";
        std::cout << "  --top-p <n>            Top-p sampling (default: 0.95)\n";
        std::cout << "  --top-k <n>            Top-k sampling (default: 40)\n";
        std::cout << "  --max-tokens <n>       Max tokens to generate (default: 128)\n";
        std::cout << "  -v, --version          Show version\n";
        std::cout << "  -h, --help             Show this help\n\n";
        std::cout << "Examples:\n";
        std::cout << "  " << progName << " -m model.gguf -p \"Hello, how are you?\"\n";
        std::cout << "  " << progName << " -m model.gguf -i\n";
    }

    void printVersion() {
        std::cout << "Mito CLI v" << VERSION << "\n";
#ifdef LLAMA_CPP_AVAILABLE
        std::cout << "llama.cpp: linked\n";
#else
        std::cout << "llama.cpp: not linked (build with -DLLAMA_CPP_AVAILABLE)\n";
#endif
    }

    bool fileExists(const std::string& path) {
        std::ifstream file(path);
        return file.good();
    }

#ifdef LLAMA_CPP_AVAILABLE
    struct LlamaContext {
        llama_model* model = nullptr;
        llama_context* ctx = nullptr;
        int n_threads = 4;
        int n_ctx = 512;
        float temperature = 0.7f;
        float top_p = 0.95f;
        int top_k = 40;
        int max_tokens = 128;

        bool load(const std::string& modelPath) {
            llama_backend_init();

            auto mparams = llama_model_default_params();
            model = llama_load_model_from_file(modelPath.c_str(), mparams);
            if (!model) {
                std::cerr << "Error: Failed to load model: " << modelPath << "\n";
                return false;
            }

            auto cparams = llama_context_default_params();
            cparams.n_ctx = n_ctx;
            cparams.n_threads = n_threads;

            ctx = llama_new_context_with_model(model, cparams);
            if (!ctx) {
                std::cerr << "Error: Failed to create context\n";
                llama_free_model(model);
                model = nullptr;
                return false;
            }

            return true;
        }

        std::string generate(const std::string& prompt) {
            if (!ctx || !model) return "";

            std::vector<llama_token> tokens_list;
            tokens_list.resize(prompt.size() + 1);
            int n = llama_tokenize(model, prompt.c_str(), prompt.size(),
                                   tokens_list.data(), tokens_list.size(), true, false);
            tokens_list.resize(n);

            if (llama_decode(ctx, llama_batch_get_one(tokens_list.data(), n))) {
                std::cerr << "Error: Failed to eval prompt\n";
                return "";
            }

            std::string result;
            const int n_vocab = llama_n_vocab(model);

            for (int i = 0; i < max_tokens; i++) {
                float* logits = llama_get_logits_ith(ctx, -1);

                std::vector<llama_token_data> candidates;
                candidates.reserve(n_vocab);
                for (llama_token token_id = 0; token_id < n_vocab; token_id++) {
                    candidates.emplace_back(llama_token_data{token_id, logits[token_id], 0.0f});
                }

                llama_token_data_array candidates_p = { candidates.data(), candidates.size(), false };

                llama_sample_top_k(ctx, &candidates_p, top_k, 1);
                llama_sample_top_p(ctx, &candidates_p, top_p, 1);
                llama_sample_temp(ctx, &candidates_p, temperature);

                llama_token new_token_id = llama_sample_token(ctx, &candidates_p);

                if (new_token_id == llama_token_eos(model)) {
                    break;
                }

                char buf[256];
                int piece_len = llama_token_to_piece(model, new_token_id, buf, sizeof(buf), 0, false);
                if (piece_len > 0) {
                    result.append(buf, piece_len);
                }

                if (llama_decode(ctx, llama_batch_get_one(&new_token_id, 1))) {
                    std::cerr << "Error: Failed to eval token\n";
                    break;
                }
            }

            return result;
        }

        ~LlamaContext() {
            if (ctx) llama_free(ctx);
            if (model) llama_free_model(model);
            llama_backend_free();
        }
    };

    void runInteractive(const std::string& modelPath, int threads, int context, float temp,
                        float top_p, int top_k, int max_tokens) {
        LlamaContext llama;
        llama.n_threads = threads;
        llama.n_ctx = context;
        llama.temperature = temp;
        llama.top_p = top_p;
        llama.top_k = top_k;
        llama.max_tokens = max_tokens;

        if (!llama.load(modelPath)) {
            return;
        }

        std::cout << "Starting interactive mode with model: " << modelPath << "\n";
        std::cout << "Type 'quit' or 'exit' to stop.\n\n";

        std::string prompt;
        std::string conversation;

        while (true) {
            std::cout << "> ";
            std::getline(std::cin, prompt);

            if (prompt == "quit" || prompt == "exit") {
                std::cout << "Goodbye!\n";
                break;
            }

            if (prompt.empty()) {
                continue;
            }

            conversation += "User: " + prompt + "\n\nAssistant:";
            std::string response = llama.generate(conversation);
            conversation += response;

            std::cout << response << "\n\n";
        }
    }

    void runPrompt(const std::string& modelPath, const std::string& prompt,
                   int threads, int context, float temp,
                   float top_p, int top_k, int max_tokens) {
        LlamaContext llama;
        llama.n_threads = threads;
        llama.n_ctx = context;
        llama.temperature = temp;
        llama.top_p = top_p;
        llama.top_k = top_k;
        llama.max_tokens = max_tokens;

        if (!llama.load(modelPath)) {
            return;
        }

        std::string fullPrompt = "User: " + prompt + "\n\nAssistant:";
        std::string response = llama.generate(fullPrompt);
        std::cout << response << "\n";
    }
#else
    void runInteractive(const std::string& modelPath, int threads, int context, float temp,
                        float top_p, int top_k, int max_tokens) {
        (void)threads; (void)context; (void)temp;
        (void)top_p; (void)top_k; (void)max_tokens;
        std::cout << "Starting interactive mode with model: " << modelPath << "\n";
        std::cout << "Type 'quit' or 'exit' to stop.\n\n";
        std::cout << "[Stub] Build with llama.cpp to enable inference.\n";
        std::cout << "  git clone https://github.com/ggerganov/llama.cpp.git\n";
        std::cout << "  cd llama.cpp && make && sudo make install\n";
        std::cout << "  Then rebuild: g++ -std=c++17 -DLLAMA_CPP_AVAILABLE -o llama-cli main.cpp -lllama\n\n";

        std::string prompt;
        while (true) {
            std::cout << "> ";
            std::getline(std::cin, prompt);

            if (prompt == "quit" || prompt == "exit") {
                std::cout << "Goodbye!\n";
                break;
            }

            if (prompt.empty()) {
                continue;
            }

            std::cout << "[Stub] You said: " << prompt << "\n\n";
        }
    }

    void runPrompt(const std::string& modelPath, const std::string& prompt,
                   int threads, int context, float temp,
                   float top_p, int top_k, int max_tokens) {
        (void)threads; (void)context; (void)temp;
        (void)top_p; (void)top_k; (void)max_tokens;
        std::cout << "Model: " << modelPath << "\n";
        std::cout << "Prompt: " << prompt << "\n\n";
        std::cout << "[Stub] Build with llama.cpp to enable inference.\n";
    }
#endif
}

int main(int argc, char* argv[]) {
    std::string modelPath;
    std::string prompt;
    bool interactive = false;
    int threads = 4;
    int context = 512;
    float temp = 0.7f;
    float top_p = 0.95f;
    int top_k = 40;
    int max_tokens = 128;
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-h" || arg == "--help") {
            printUsage(argv[0]);
            return 0;
        }

        if (arg == "-v" || arg == "--version") {
            printVersion();
            return 0;
        }

        if ((arg == "-m" || arg == "--model") && i + 1 < argc) {
            modelPath = argv[++i];
            continue;
        }

        if ((arg == "-p" || arg == "--prompt") && i + 1 < argc) {
            prompt = argv[++i];
            continue;
        }

        if (arg == "-i" || arg == "--interactive") {
            interactive = true;
            continue;
        }

        if ((arg == "-t" || arg == "--threads") && i + 1 < argc) {
            threads = std::atoi(argv[++i]);
            continue;
        }

        if ((arg == "-c" || arg == "--context") && i + 1 < argc) {
            context = std::atoi(argv[++i]);
            continue;
        }

        if (arg == "--temp" && i + 1 < argc) {
            temp = std::atof(argv[++i]);
            continue;
        }

        if (arg == "--top-p" && i + 1 < argc) {
            top_p = std::atof(argv[++i]);
            continue;
        }

        if (arg == "--top-k" && i + 1 < argc) {
            top_k = std::atoi(argv[++i]);
            continue;
        }

        if (arg == "--max-tokens" && i + 1 < argc) {
            max_tokens = std::atoi(argv[++i]);
            continue;
        }
    }

    if (modelPath.empty()) {
        std::cerr << "Error: Model file is required. Use -m <model.gguf>\n";
        std::cerr << "Run with -h for help.\n";
        return 1;
    }

    if (!fileExists(modelPath)) {
        std::cerr << "Error: Model file not found: " << modelPath << "\n";
        return 1;
    }

    if (interactive) {
        runInteractive(modelPath, threads, context, temp, top_p, top_k, max_tokens);
    } else if (!prompt.empty()) {
        runPrompt(modelPath, prompt, threads, context, temp, top_p, top_k, max_tokens);
    } else {
        std::cerr << "Error: Either -p <prompt> or -i (interactive) required.\n";
        std::cerr << "Run with -h for help.\n";
        return 1;
    }

    return 0;
}
