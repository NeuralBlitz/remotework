"""
Async and Streaming Support for Mito
"""

import asyncio
import aiofiles
from typing import AsyncIterator, Iterator, Callable, Any, List, Optional
from dataclasses import dataclass
import json
import time


class AsyncBase:
    """Base class for async operations"""
    
    async def run(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class StreamChunk:
    content: str
    done: bool = False
    metadata: dict = None


class AsyncPipeline:
    """Async pipeline for streaming data"""
    
    def __init__(self):
        self.steps: List[Callable] = []
    
    def add_step(self, func: Callable) -> "AsyncPipeline":
        self.steps.append(func)
        return self
    
    async def execute(self, input_data: Any) -> AsyncIterator[Any]:
        """Execute pipeline yielding results"""
        data = input_data
        for step in self.steps:
            if asyncio.iscoroutinefunction(step):
                data = await step(data)
            else:
                data = step(data)
            yield data


class StreamProcessor:
    """Process streaming data"""
    
    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size
        self.buffer: List[str] = []
    
    def process(self, text: str) -> Iterator[str]:
        """Process text in chunks"""
        words = text.split()
        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i:i + self.chunk_size])
            yield chunk
    
    async def process_async(self, text: str) -> AsyncIterator[str]:
        """Process text in chunks async"""
        for chunk in self.process(text):
            yield chunk
            await asyncio.sleep(0)


class AsyncGenerator:
    """Async generator wrapper"""
    
    def __init__(self, generator_func: Callable):
        self.generator_func = generator_func
    
    def __aiter__(self):
        return self
    
    async def __anext__(self) -> Any:
        try:
            return next(self.generator_func)
        except StopIteration:
            raise StopAsyncIteration


async def stream_text(
    prompt: str,
    model_name: str = "gpt2",
    max_tokens: int = 100
) -> AsyncIterator[StreamChunk]:
    """Stream text generation token by token"""
    from python.ai import TextGenerator
    
    gen = TextGenerator(model_name=model_name)
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: gen.generate(prompt, max_length=max_tokens)
    )
    
    text = result.get("choices", [{}])[0].get("text", "")
    
    for i in range(0, len(text), 10):
        yield StreamChunk(
            content=text[i:i+10],
            done=False
        )
        await asyncio.sleep(0.01)
    
    yield StreamChunk(content="", done=True)


async def stream_file_read(filepath: str, chunk_size: int = 1024) -> AsyncIterator[bytes]:
    """Stream file reading"""
    async with aiofiles.open(filepath, 'rb') as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk


async def batch_process(
    items: List[Any],
    processor: Callable,
    batch_size: int = 10
) -> List[Any]:
    """Process items in batches"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        if asyncio.iscoroutinefunction(processor):
            batch_results = await asyncio.gather(*[processor(item) for item in batch])
        else:
            batch_results = [processor(item) for item in batch]
        
        results.extend(batch_results)
    
    return results


async def run_with_timeout(coro, timeout: float):
    """Run coroutine with timeout"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout} seconds")


class AsyncCache:
    """Async in-memory cache"""
    
    def __init__(self, ttl: int = 3600):
        self.cache: dict = {}
        self.ttl = ttl
    
    async def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            item = self.cache[key]
            if time.time() - item["time"] < self.ttl:
                return item["value"]
            del self.cache[key]
        return None
    
    async def set(self, key: str, value: Any):
        self.cache[key] = {"value": value, "time": time.time()}
    
    async def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]
    
    async def clear(self):
        self.cache.clear()


class WebSocketHandler:
    """WebSocket handler for real-time streaming"""
    
    def __init__(self, websocket):
        self.websocket = websocket
    
    async def send_stream(self, stream: AsyncIterator):
        """Send streaming data via WebSocket"""
        async for chunk in stream:
            if isinstance(chunk, StreamChunk):
                data = json.dumps({
                    "content": chunk.content,
                    "done": chunk.done,
                    "metadata": chunk.metadata or {}
                })
            else:
                data = json.dumps({"content": str(chunk)})
            
            await self.websocket.send(data)
    
    async def receive(self) -> dict:
        """Receive message from WebSocket"""
        message = await self.websocket.receive()
        return json.loads(message.get("text", "{}"))


async def create_grpc_stream(generator_func: Callable) -> Any:
    """Create gRPC streaming response"""
    async for item in generator_func():
        yield item


class EventEmitter:
    """Async event emitter"""
    
    def __init__(self):
        self.listeners: dict = {}
    
    def on(self, event: str, callback: Callable):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    async def emit(self, event: str, *args, **kwargs):
        if event in self.listeners:
            for callback in self.listeners[event]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(*args, **kwargs)


if __name__ == '__main__':
    async def test():
        async for chunk in stream_text("Hello world"):
            print(f"Chunk: {chunk.content}, Done: {chunk.done}")
    
    asyncio.run(test())
