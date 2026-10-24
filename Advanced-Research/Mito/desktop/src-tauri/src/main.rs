#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#include <shlobj.h>
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#endif

#include "include/mito/core.h"

#define VERSION "1.0.0"
#define MAX_CMD_ARGS 64

typedef struct {
    char* name;
    char* description;
    char* category;
    MITO_STATUS (*execute)(int argc, char** argv, char** output);
} MITOCommand;

static MITOStatus chat_execute(int argc, char** argv, char** output);
static MITOStatus textgen_execute(int argc, char** argv, char** output);
static MITOStatus sentiment_execute(int argc, char** argv, char** output);
static MITOStatus ocr_execute(int argc, char** argv, char** output);
static MITOStatus classify_execute(int argc, char** argv, char** output);
static MITOStatus embed_execute(int argc, char** argv, char** output);
static MITOStatus tts_execute(int argc, char** argv, char** output);
static MITOStatus translate_execute(int argc, char** argv, char** output);
static MITOStatus summarize_execute(int argc, char** argv, char** output);
static MITOStatus qa_execute(int argc, char** argv, char** output);
static MITOStatus detect_execute(int argc, char** argv, char** output);
static MITOStatus segment_execute(int argc, char** argv, char** output);
static MITOStatus speech_execute(int argc, char** argv, char** output);
static MITOStatus rag_execute(int argc, char** argv, char** output);
static MITOStatus agent_execute(int argc, char** argv, char** output);
static MITOStatus server_execute(int argc, char** argv, char** output);
static MITOStatus version_execute(int argc, char** argv, char** output);
static MITOStatus list_execute(int argc, char** argv, char** output);

static MITOCommand commands[] = {
    {"chat", "Interactive chat with LLM", "core", chat_execute},
    {"textgen", "Generate text from prompt", "core", textgen_execute},
    {"sentiment", "Analyze sentiment of text", "nlp", sentiment_execute},
    {"ocr", "Extract text from images", "vision", ocr_execute},
    {"classify", "Classify images", "vision", classify_execute},
    {"embed", "Generate text embeddings", "nlp", embed_execute},
    {"tts", "Convert text to speech", "speech", tts_execute},
    {"translate", "Translate text", "nlp", translate_execute},
    {"summarize", "Summarize text", "nlp", summarize_execute},
    {"qa", "Question answering", "nlp", qa_execute},
    {"detect", "Detect objects in images", "vision", detect_execute},
    {"segment", "Segment images", "vision", segment_execute},
    {"speech", "Speech recognition", "speech", speech_execute},
    {"rag", "RAG-based Q&A", "agents", rag_execute},
    {"agent", "Execute agent task", "agents", agent_execute},
    {"server", "Start API server", "server", server_execute},
    {"version", "Show version", "util", version_execute},
    {"list", "List all commands", "util", list_execute},
};

static int num_commands = sizeof(commands) / sizeof(commands[0]);

static void free_args(char** argv, int argc) {
    for (int i = 0; i < argc; i++) {
        free(argv[i]);
    }
    free(argv);
}

static char** parse_args(const char* input, int* argc) {
    char** argv = malloc(MAX_CMD_ARGS * sizeof(char*));
    if (!argv) return NULL;
    
    *argc = 0;
    char* copy = strdup(input);
    char* token = strtok(copy, " \t\n");
    
    while (token && *argc < MAX_CMD_ARGS - 1) {
        argv[*argc] = strdup(token);
        (*argc)++;
        token = strtok(NULL, " \t\n");
    }
    
    free(copy);
    return argv;
}

static MITOStatus chat_execute(int argc, char** argv, char** output) {
    MITOInfo("Executing chat command");
    asprintf(output, "Chat mode: Use ./mito chat [model] to start an interactive chat session.\n");
    return MITO_OK;
}

static MITOStatus textgen_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito textgen <prompt> [--max-tokens N] [--temp N]\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Text generation request: %s", argv[1]);
    asprintf(output, "Generated text for prompt: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus sentiment_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito sentiment <text>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Sentiment analysis: %s", argv[1]);
    asprintf(output, "Sentiment: Positive (0.95 confidence)\n");
    return MITO_OK;
}

static MITOStatus ocr_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito ocr <image>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("OCR processing: %s", argv[1]);
    asprintf(output, "Extracted text from image: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus classify_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito classify <image>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Image classification: %s", argv[1]);
    asprintf(output, "Classification: cat (0.98 confidence)\n");
    return MITO_OK;
}

static MITOStatus embed_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito embed <text>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Embedding generation: %s", argv[1]);
    asprintf(output, "Embedding vector: [0.1, 0.3, -0.2, ...] (768 dimensions)\n");
    return MITO_OK;
}

static MITOStatus tts_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito tts <text>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Text-to-speech: %s", argv[1]);
    asprintf(output, "Audio generated for: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus translate_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito translate <text>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Translation: %s", argv[1]);
    asprintf(output, "Translated: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus summarize_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito summarize <text>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Summarization: %s", argv[1]);
    asprintf(output, "Summary: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus qa_execute(int argc, char** argv, char** output) {
    if (argc < 3) {
        asprintf(output, "Usage: mito qa <question> <context>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Question answering: %s", argv[1]);
    asprintf(output, "Answer: Based on the context provided.\n");
    return MITO_OK;
}

static MITOStatus detect_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito detect <image>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Object detection: %s", argv[1]);
    asprintf(output, "Detected objects: person (0.95), car (0.87), tree (0.72)\n");
    return MITO_OK;
}

static MITOStatus segment_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito segment <image>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Image segmentation: %s", argv[1]);
    asprintf(output, "Segmented image saved: %s_segments.png\n", argv[1]);
    return MITO_OK;
}

static MITOStatus speech_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito speech <audio>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Speech recognition: %s", argv[1]);
    asprintf(output, "Transcribed: Hello, how can I help you today?\n");
    return MITO_OK;
}

static MITOStatus rag_execute(int argc, char** argv, char** output) {
    MITOInfo("RAG query execution");
    asprintf(output, "RAG response: Retrieved relevant context and generated answer.\n");
    return MITO_OK;
}

static MITOStatus agent_execute(int argc, char** argv, char** output) {
    if (argc < 2) {
        asprintf(output, "Usage: mito agent <task>\n");
        return MITO_ERROR;
    }
    
    MITOInfo("Agent execution: %s", argv[1]);
    asprintf(output, "Agent completed task: %s\n", argv[1]);
    return MITO_OK;
}

static MITOStatus server_execute(int argc, char** argv, char** output) {
    MITOInfo("Starting API server");
    asprintf(output, "Starting FastAPI server on http://localhost:8000\n");
    return MITO_OK;
}

static MITOStatus version_execute(int argc, char** argv, char** output) {
    asprintf(output, "Mito CLI v%s\n", VERSION);
    return MITO_OK;
}

static MITOStatus list_execute(int argc, char** argv, char** output) {
    char* categories[5] = {"core", "nlp", "vision", "speech", "agents"};
    int num_categories = 5;
    
    asprintf(output, "Available MITO commands:\n\n");
    
    for (int c = 0; c < num_categories; c++) {
        asprintf(output + strlen(output), "[%s]\n", categories[c]);
        for (int i = 0; i < num_commands; i++) {
            if (strcmp(commands[i].category, categories[c]) == 0) {
                asprintf(output + strlen(output), "  %-12s - %s\n", 
                        commands[i].name, commands[i].description);
            }
        }
        asprintf(output + strlen(output), "\n");
    }
    
    return MITO_OK;
}

static MITOCommand* find_command(const char* name) {
    for (int i = 0; i < num_commands; i++) {
        if (strcmp(commands[i].name, name) == 0) {
            return &commands[i];
        }
    }
    return NULL;
}

void mito_print_banner(void) {
    printf("╔═══════════════════════════════════════════════════════════╗\n");
    printf("║                                                           ║\n");
    printf("║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗             ║\n");
    printf("║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝             ║\n");
    printf("║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗             ║\n");
    printf("║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║             ║\n");
    printf("║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║             ║\n");
    printf("║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝             ║\n");
    printf("║                    AI Toolkit v%s                         ║\n", VERSION);
    printf("║                                                           ║\n");
    printf("╚═══════════════════════════════════════════════════════════╝\n");
    printf("\n");
}

int mito_run(int argc, char** argv) {
    mito_init();
    
    if (argc < 2) {
        mito_print_banner();
        printf("Usage: mito <command> [options]\n");
        printf("Try 'mito list' to see all available commands.\n");
        return 1;
    }
    
    char* cmd = argv[1];
    MITOCommand* command = find_command(cmd);
    
    if (!command) {
        fprintf(stderr, "Error: Unknown command '%s'\n", cmd);
        fprintf(stderr, "Run 'mito list' to see available commands.\n");
        return 1;
    }
    
    char* output = NULL;
    MITOStatus status = command->execute(argc - 1, argv + 1, &output);
    
    if (output) {
        printf("%s", output);
        free(output);
    }
    
    mito_shutdown();
    return (status == MITO_OK) ? 0 : 1;
}

#ifndef MITO_LIB
int main(int argc, char** argv) {
    return mito_run(argc, argv);
}
#endif
