"""
Mito Utilities
Common helper functions and tools
"""

import os
import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass
import base64



def ensure_dir(path: str) -> Path:
    """Ensure directory exists"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """Calculate file hash"""
    hash_obj = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def read_json(path: str) -> Dict:
    """Read JSON file"""
    with open(path, 'r') as f:
        return json.load(f)


def write_json(path: str, data: Any, indent: int = 2):
    """Write JSON file"""
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)


def load_prompt_template(path: str, **kwargs) -> str:
    """Load prompt template with variables"""
    with open(path, 'r') as f:
        template = f.read()
    
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", str(value))
    
    return template


def sanitize_filename(name: str) -> str:
    """Sanitize filename"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate text to length"""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def batch(items: List[Any], size: int) -> List[List[Any]]:
    """Split items into batches"""
    return [items[i:i + size] for i in range(0, len(items), size)]


def flatten(items: List[Union[List, Any]]) -> List[Any]:
    """Flatten nested list"""
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def deduplicate(items: List[Any]) -> List[Any]:
    """Remove duplicates while preserving order"""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def parse_key_value(text: str, delimiter: str = "=") -> Dict[str, str]:
    """Parse key=value pairs"""
    result = {}
    for line in text.strip().split('\n'):
        if delimiter in line:
            key, value = line.split(delimiter, 1)
            result[key.strip()] = value.strip()
    return result


def slugify(text: str) -> str:
    """Convert text to URL slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """Format seconds to human readable duration"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def parse_markdown(text: str) -> Dict[str, Any]:
    """Simple markdown parser"""
    lines = text.split('\n')
    result = {
        "title": "",
        "headings": [],
        "code_blocks": [],
        "links": [],
        "text": []
    }
    
    in_code = False
    code_content = []
    
    for line in lines:
        if line.startswith('```'):
            if in_code:
                result["code_blocks"].append('\n'.join(code_content))
                code_content = []
            in_code = not in_code
        elif in_code:
            code_content.append(line)
        elif line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            content = line.lstrip('# ').strip()
            result["headings"].append({"level": level, "text": content})
            if level == 1 and not result["title"]:
                result["title"] = content
        elif line.startswith('[') and '](' in line:
            match = re.search(r'\[([^\]]+)\]\(([^\)]+)\)', line)
            if match:
                result["links"].append({"text": match.group(1), "url": match.group(2)})
        elif line.strip():
            result["text"].append(line.strip())
    
    return result


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def encode_base64(data: Union[str, bytes]) -> str:
    """Encode to base64"""
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data).decode()


def decode_base64(data: str) -> bytes:
    """Decode from base64"""
    return base64.b64decode(data)


class DictWalker:
    """Walk nested dict/json"""
    
    def __init__(self, data: Union[Dict, List]):
        self.data = data
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get value by dot-separated path"""
        keys = path.split('.')
        current = self.data
        
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
            
            if current is None:
                return default
        
        return current
    
    def set(self, path: str, value: Any):
        """Set value by dot-separated path"""
        keys = path.split('.')
        current = self.data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def flatten(self, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten nested dict"""
        items = []
        
        for k, v in self.data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(DictWalker(v).flatten(new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        
        return dict(items)


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))
            
            raise last_exception
        
        return wrapper
    return decorator


def memoize(func):
    """Memoization decorator"""
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    wrapper.cache = cache
    wrapper.clear = lambda: cache.clear()
    return wrapper


if __name__ == '__main__':
    print(sanitize_filename("test@file.txt"))
    print(format_size(1024 * 1024 * 50))
    print(slugify("Hello World!"))
