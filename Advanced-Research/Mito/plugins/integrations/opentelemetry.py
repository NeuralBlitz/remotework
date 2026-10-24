"""
OpenTelemetry Plugin
Distributed tracing with OpenTelemetry.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.opentelemetry")

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


_tracer = None


def _get_tracer():
    global _tracer
    if not OTEL_AVAILABLE:
        raise ImportError("opentelemetry-api and opentelemetry-sdk not installed")
    if _tracer is None:
        provider = TracerProvider()
        processor = SimpleSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer(__name__)
    return _tracer


def otel_start_span_cmd(name: str = "mito.span", attrs: str = "") -> Dict:
    import json
    tracer = _get_tracer()
    attributes = json.loads(attrs) if attrs else {}
    ctx = tracer.start_span(name, attributes=attributes)
    return {"status": "span_started", "name": name, "trace_id": format(ctx.trace_id, "032x")}


def otel_record_event_cmd(name: str = "event", attrs: str = "") -> Dict:
    import json
    tracer = _get_tracer()
    current = trace.get_current_span()
    attributes = json.loads(attrs) if attrs else {}
    current.add_event(name, attributes=attributes)
    return {"status": "event_recorded", "name": name}


def otel_set_status_cmd(code: int = 1, description: str = "") -> Dict:
    from opentelemetry.trace import Status, StatusCode
    current = trace.get_current_span()
    status_code = StatusCode.OK if code == 0 else StatusCode.ERROR
    current.set_status(Status(status_code, description))
    return {"status": "ok", "code": str(status_code)}


def otel_add_span_attr_cmd(key: str = "", value: str = "") -> Dict:
    tracer = _get_tracer()
    current = trace.get_current_span()
    current.set_attribute(key, value)
    return {"status": "ok", "key": key, "value": value}


def otel_shutdown_cmd() -> Dict:
    from opentelemetry.sdk.trace import TracerProvider
    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()
    return {"status": "shutdown"}


def register(plugin):
    plugin.register_command("start_span", otel_start_span_cmd)
    plugin.register_command("record_event", otel_record_event_cmd)
    plugin.register_command("set_status", otel_set_status_cmd)
    plugin.register_command("add_span_attr", otel_add_span_attr_cmd)
    plugin.register_command("shutdown", otel_shutdown_cmd)


PLUGIN_METADATA = {
    "name": "opentelemetry", "version": "1.0.0",
    "description": "OpenTelemetry distributed tracing and observability",
    "author": "Mito Team", "license": "MIT",
    "tags": ["tracing", "opentelemetry", "observability", "distributed"],
    "dependencies": ["opentelemetry-api", "opentelemetry-sdk"], "permissions": ["tracing_write"],
    "min_mito_version": "1.0.1",
}

opentelemetry_plugin = {"metadata": PLUGIN_METADATA, "register": register}
