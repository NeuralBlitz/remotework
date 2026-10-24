"""
Mito Logging System
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON log formatter."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class MitoLogger:
    _instance: Optional[logging.Logger] = None
    
    def __init__(
        self,
        name: str = "mito",
        level: str = "INFO",
        log_file: Optional[str] = None,
        json_format: bool = False,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 5
    ):
        self.name = name
        self.level = getattr(logging, level.upper())
        self.log_file = log_file
        self.json_format = json_format
        self.max_bytes = max_bytes
        self.backup_count = backup_count
    
    def get_logger(self) -> logging.Logger:
        if MitoLogger._instance is not None:
            return MitoLogger._instance
        
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.handlers.clear()
        
        formatter = JSONFormatter() if self.json_format else logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if self.log_file:
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        MitoLogger._instance = logger
        return logger
    
    @staticmethod
    def get_default_logger() -> logging.Logger:
        if MitoLogger._instance is None:
            return MitoLogger().get_logger()
        return MitoLogger._instance


def get_logger(name: str = "mito") -> logging.Logger:
    """Get logger instance."""
    return MitoLogger().get_logger()


def log_request(logger: logging.Logger, method: str, path: str, status: int, duration: float):
    """Log HTTP request."""
    logger.info(f"{method} {path} {status} {duration:.3f}s")


def log_error(logger: logging.Logger, error: Exception, context: dict = None):
    """Log error with context."""
    logger.error(f"Error: {str(error)}", extra={"context": context or {}})


def log_model_load(logger: logging.Logger, model_name: str, duration: float):
    """Log model loading."""
    logger.info(f"Model loaded: {model_name} ({duration:.2f}s)")


def log_inference(logger: logging.Logger, model_name: str, duration: float, tokens: int):
    """Log inference."""
    logger.info(f"Inference: {model_name} - {tokens} tokens in {duration:.2f}s")


class LogCapture:
    """Context manager to capture logs for testing."""
    
    def __init__(self, logger_name: str = "mito", level: int = logging.DEBUG):
        self.logger_name = logger_name
        self.level = level
        self.handler = None
        self.records = []
    
    def __enter__(self):
        logger = logging.getLogger(self.logger_name)
        self.handler = logging.Handler()
        self.handler.setLevel(self.level)
        self.handler.emit = lambda r: self.records.append(r)
        logger.addHandler(self.handler)
        return self
    
    def __exit__(self, *args):
        logger = logging.getLogger(self.logger_name)
        logger.removeHandler(self.handler)
    
    def get_logs(self) -> list:
        return [r.getMessage() for r in self.records]
    
    def has_error(self) -> bool:
        return any(r.levelno >= logging.ERROR for r in self.records)


if __name__ == '__main__':
    logger = get_logger()
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
