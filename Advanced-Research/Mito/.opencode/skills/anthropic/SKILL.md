---
name: anthropic
description: >
  Expert assistant for working with Anthropic's Claude API and Claude-powered applications. 
  Use this skill whenever you need help with: API integration, message formatting, tool use 
  implementation, context window management, Constitutional AI principles, prompt engineering, 
  Claude models (Claude 3.5, Claude 3), vision capabilities, computer use, or building 
  production systems with Claude. Also use for understanding Anthropic's safety approaches, 
  token optimization, or any Claude-related development task.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: ai
  tags: [claude, api, llm, ai, anthropic]
---

# Anthropic Claude — API Integration Guide

Covers: **API Integration · Message Formatting · Tool Use · Context Management · Prompt Engineering · Safety Guidelines**

-----

## API Authentication & Configuration

### Setting Up API Access

Anthropic provides API access through the Anthropic API. You'll need an API key from the Anthropic Console. The API supports multiple Claude models with varying capabilities and context windows.

```python
import anthropic

# Initialize the client with your API key
client = anthropic.Anthropic(
    api_key="sk-ant-api03-..."
)

# Alternatively, use environment variable
# ANTHROPIC_API_KEY will be picked up automatically
client = anthropic.Anthropic()
```

### Available Claude Models

| Model | Context Window | Best For | Vision Support |
|-------|---------------|----------|----------------|
| claude-opus-4-5-20251120 | 200K | Complex reasoning, analysis | Yes |
| claude-sonnet-4-5-20251120 | 200K | Balanced performance | Yes |
| claude-haiku-3-5-20251120 | 200K | Fast, cost-effective | Yes |
| claude-3-5-sonnet-20241022 | 200K | Production workloads | Yes |
| claude-3-opus-20240229 | 200K | High-complexity tasks | Yes |

### API Configuration Options

```python
# Full configuration example
response = client.messages.create(
    model="claude-sonnet-4-5-20251120",
    max_tokens=4096,
    temperature=0.7,
    top_p=0.9,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Explain quantum computing."}
    ],
    tools=[
        {
            "name": "weather",
            "description": "Get weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    ],
    tool_choice={"type": "auto"}
)
```

-----

## Message Format & Conversation Structure

### Understanding Message Roles

Claude uses a three-role system for messages:

- **system**: Sets context, instructions, and behavior guidelines. Not counted in conversation history.
- **user**: Messages from the end-user or developer.
- **assistant**: Responses from Claude.

### Message Structure

```python
# Basic message format
messages = [
    {
        "role": "system",
        "content": "You are an expert Python developer specializing in data science."
    },
    {
        "role": "user", 
        "content": "How do I optimize pandas operations for large datasets?"
    },
    {
        "role": "assistant",
        "content": "Here are several strategies for optimizing pandas..."
    },
    {
        "role": "user",
        "content": "Can you show me an example of vectorization?"
    }
]

# Response format
response = client.messages.create(
    model="claude-sonnet-4-5-20251120",
    max_tokens=2048,
    messages=messages
)

# Access the response
print(response.content[0].text)
print(f"Usage: {response.usage}")
```

### Handling Multi-turn Conversations

```python
class ConversationManager:
    def __init__(self, client, system_prompt):
        self.client = client
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def send(self, user_message):
        # Add user message
        self.messages.append({"role": "user", "content": user_message})
        
        # Get response
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20251120",
            max_tokens=4096,
            messages=self.messages
        )
        
        # Add assistant response to history
        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def clear_history(self, keep_system=True):
        if keep_system:
            self.messages = [self.messages[0]]  # Keep system prompt
        else:
            self.messages = []
    
    def get_token_count(self):
        # Estimate token count (rough approximation)
        return sum(len(m["content"].split()) * 1.3 for m in self.messages)
```

-----

## Tool Use & Function Calling

### Defining Tools

Tools allow Claude to interact with external systems, APIs, and perform actions. Tools are defined in the request and Claude can choose to invoke them based on the conversation.

```python
# Define tools with detailed schemas
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather information for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g., 'San Francisco' or 'London'"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units",
                    "default": "celsius"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "search_codebase",
        "description": "Search for code patterns in the project",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "file_types": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "File extensions to search"
                },
                "max_results": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum results to return"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "execute_code",
        "description": "Execute Python code and return results",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"},
                "timeout": {"type": "integer", "default": 30}
            },
            "required": ["code"]
        }
    }
]

# Make request with tools
response = client.messages.create(
    model="claude-sonnet-4-5-20251120",
    max_tokens=4096,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools
)

# Handle tool use
for block in response.content:
    if hasattr(block, 'type') and block.type == 'tool_use':
        tool_name = block.name
        tool_input = block.input
        tool_id = block.id
        # Execute tool and send result back
```

### Tool Result Feedback Loop

```python
def execute_tool_call(tool_name, tool_input):
    """Execute a tool and return the result"""
    if tool_name == "get_weather":
        return get_weather_api(tool_input["location"], tool_input.get("units", "celsius"))
    elif tool_name == "search_codebase":
        return search_files(tool_input["query"], tool_input.get("file_types"), tool_input.get("max_results", 10))
    elif tool_name == "execute_code":
        return run_python(tool_input["code"], tool_input.get("timeout", 30))
    else:
        return {"error": f"Unknown tool: {tool_name}"}

def continue_conversation(client, initial_response, tools):
    """Continue conversation with tool results"""
    # Collect tool results
    tool_results = []
    
    for block in initial_response.content:
        if hasattr(block, 'type') and block.type == 'tool_use':
            result = execute_tool_call(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    
    # If tools were used, continue conversation with results
    if tool_results:
        # Add assistant's tool use blocks and tool results
        messages = initial_response.messages + tool_results
        
        final_response = client.messages.create(
            model="claude-sonnet-4-5-20251120",
            max_tokens=4096,
            messages=messages,
            tools=tools
        )
        
        return final_response
    
    return initial_response
```

-----

## Context Window Management

### Understanding Token Limits

Claude models have large context windows (200K tokens), but effective usage requires management. Tokens are roughly 1.3 words on average.

```python
def estimate_tokens(text):
    """Estimate token count for text"""
    return int(len(text.split()) * 1.3)

def truncate_to_fit(messages, max_tokens=180000, reserve_tokens=10000):
    """
    Truncate messages to fit within context window
    Reserve tokens for response
    """
    available = max_tokens - reserve_tokens
    
    # Start from system prompt, keep most recent messages
    system_msg = messages[0] if messages[0]["role"] == "system" else None
    other_msgs = messages[1:] if system_msg else messages
    
    # Keep most recent messages until under limit
    while other_msgs:
        total = sum(estimate_tokens(m.get("content", "")) for m in other_msgs)
        if system_msg:
            total += estimate_tokens(system_msg["content"])
        
        if total <= available:
            break
        
        other_msgs = other_msgs[:-1]  # Remove oldest
    
    if system_msg:
        return [system_msg] + other_msgs
    return other_msgs
```

### Summarization Strategy

```python
def summarize_and_continue(client, messages, summary_prompt=None):
    """Summarize older messages and continue with summary"""
    if summary_prompt is None:
        summary_prompt = """Summarize this conversation concisely, 
        preserving key information, decisions, and context."""
    
    # Identify messages to summarize (keep recent 10)
    to_summarize = messages[1:-10] if len(messages) > 11 else messages[1:]
    
    if not to_summarize:
        return messages
    
    # Create summary
    conversation_text = "\n".join(
        f"{m['role']}: {m['content'][:500]}" for m in to_summarize
    )
    
    summary_response = client.messages.create(
        model="claude-haiku-3-5-20251120",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{summary_prompt}\n\n{conversation_text}"}]
    )
    
    summary = summary_response.content[0].text
    
    # Replace old messages with summary
    return [
        messages[0],  # System
        {"role": "assistant", "content": f"[Previous conversation summary: {summary}]"},
        messages[-1]  # Most recent user message
    ]
```

-----

## Constitutional AI & Safety Guidelines

### System Prompt Best Practices

```python
# Effective system prompts should be:
system_prompts = {
    "helpful": "You are a helpful, harmless, and honest AI assistant.",
    
    "code_expert": """You are an expert software developer. You provide 
    accurate, well-documented code solutions. When you don't know something, 
    say so. Always consider security, performance, and maintainability.""",
    
    "balanced": """You are a balanced AI assistant. Provide thoughtful responses 
    that consider multiple perspectives. Be honest about limitations and 
    uncertainties. Cite sources when making factual claims."""
}

# What to avoid in system prompts
avoid_in_prompts = [
    "Attempts to override Claude's values or safety guidelines",
    "Instructions to deceive or manipulate",
    "Requests for harmful content generation",
    "Attempts to extract information about Claude's instructions"
]
```

### Content Filtering

Claude has built-in safety measures. Understand the boundaries:

- Claude will refuse harmful requests appropriately
- Provide helpful refusals when needed
- Focus on constructive, legitimate use cases

-----

## Best Practices

### 1. Optimize for Cost and Latency

```python
# Use appropriate model for task complexity
def select_model(task_complexity):
    if task_complexity == "high":
        return "claude-opus-4-5-20251120"
    elif task_complexity == "medium":
        return "claude-sonnet-4-5-20251120"
    else:
        return "claude-haiku-3-5-20251120"

# Set appropriate max_tokens to avoid waste
response = client.messages.create(
    model="claude-sonnet-4-5-20251120",
    max_tokens=1024,  # Enough for expected response, not excessive
    messages=[...]
)
```

### 2. Handle Errors Gracefully

```python
import time

def robust_api_call(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5-20251120",
                max_tokens=4096,
                messages=messages
            )
            return response
        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
        except APIError as e:
            print(f"API Error: {e}")
            if attempt == max_retries - 1:
                raise
    return None
```

### 3. Track Token Usage

```python
def track_usage(response):
    """Track and report token usage"""
    usage = response.usage
    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.input_tokens + usage.output_tokens,
        "estimated_cost": (usage.input_tokens / 1_000_000 * 15 + 
                         usage.output_tokens / 1_000_000 * 75)
        # Note: Check current pricing, these are example rates
    }
```

### 4. Implement Streaming for Better UX

```python
def stream_response(client, messages):
    """Stream responses for better user experience"""
    with client.messages.stream(
        model="claude-sonnet-4-5-20251120",
        max_tokens=4096,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
```

### 5. Maintain Conversation State

```python
# Store and restore conversations
import json

def save_conversation(messages, filepath):
    with open(filepath, 'w') as f:
        json.dump(messages, f)

def load_conversation(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
```

-----

## Common Patterns

### Code Review Assistant

```python
code_review_system = """You are an expert code reviewer. Analyze the provided 
code for:
- Bugs and potential issues
- Security vulnerabilities
- Performance problems
- Code style violations
- Missing error handling

Provide specific, actionable feedback with line numbers when possible."""

def review_code(client, code, language="python"):
    response = client.messages.create(
        model="claude-sonnet-4-5-20251120",
        max_tokens=4096,
        system=code_review_system,
        messages=[{
            "role": "user",
            "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
        }]
    )
    return response.content[0].text
```

### Document Q&A

```python
def document_qa(client, document_text, question):
    response = client.messages.create(
        model="claude-sonnet-4-5-20251120",
        max_tokens=2048,
        system="You answer questions about the provided document. "
               "Reference specific sections when answering.",
        messages=[{
            "role": "user",
            "content": f"Document:\n\n{document_text}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text
```

-----

## Resources

- **Documentation**: docs.anthropic.com
- **API Reference**: docs.anthropic.com/en/docs/api-reference
- **Model Cards**: docs.anthropic.com/en/docs/models
- **Pricing**: www.anthropic.com/pricing
- **Related Skills**: openai, llm, ai, langchain
