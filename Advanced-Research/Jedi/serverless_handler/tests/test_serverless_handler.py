import pytest
from datetime import datetime, timezone
from serverless_handler.functions import FunctionRegistry, ServerlessFunction
from serverless_handler.events import EventMapper, TriggerEvent
from serverless_handler.runtime import FunctionRuntime, InvocationResult


def test_function_creation() -> None:
    f = ServerlessFunction(name="my-func", handler=lambda x: x)
    assert f.timeout_ms == 30000
    assert f.memory_mb == 256


def test_function_invoke() -> None:
    f = ServerlessFunction(name="add", handler=lambda x: x["a"] + x["b"])
    assert f.invoke({"a": 2, "b": 3}) == 5


def test_registry_register() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: None))
    assert reg.function_count == 1


def test_registry_register_duplicate_raises() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: None))
    with pytest.raises(ValueError):
        reg.register(ServerlessFunction(name="f1", handler=lambda x: None))


def test_registry_unregister() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: None))
    assert reg.unregister("f1")
    assert reg.function_count == 0


def test_registry_get_not_found() -> None:
    reg = FunctionRegistry()
    with pytest.raises(KeyError):
        reg.get("missing")


def test_registry_list_by_trigger() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: None, triggers=["http"]))
    reg.register(ServerlessFunction(name="f2", handler=lambda x: None, triggers=["cron"]))
    assert len(reg.list_functions("http")) == 1


def test_registry_list_all() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: None))
    reg.register(ServerlessFunction(name="f2", handler=lambda x: None))
    assert len(reg.list_functions()) == 2


def test_trigger_event_creation() -> None:
    e = TriggerEvent(event_type="INSERT", source="pg_table", payload={"id": 1})
    assert e.event_type == "INSERT"


def test_trigger_event_to_dict() -> None:
    e = TriggerEvent(event_type="INSERT", source="pg", payload={"id": 1}, event_id="evt-1")
    d = e.to_dict()
    assert d["event_type"] == "INSERT"
    assert d["event_id"] == "evt-1"


def test_event_mapper_add_mapping() -> None:
    m = EventMapper()
    m.add_mapping("INSERT", "f1")
    assert m.mapping_count == 1


def test_event_mapper_get_targets() -> None:
    m = EventMapper()
    m.add_mapping("INSERT", "f1")
    m.add_mapping("INSERT", "f2")
    assert len(m.get_targets("INSERT")) == 2


def test_event_mapper_remove_mapping() -> None:
    m = EventMapper()
    m.add_mapping("INSERT", "f1")
    assert m.remove_mapping("INSERT", "f1")
    assert m.mapping_count == 0


def test_event_mapper_remove_missing() -> None:
    m = EventMapper()
    assert not m.remove_mapping("INSERT", "f1")


def test_event_mapper_get_event_types() -> None:
    m = EventMapper()
    m.add_mapping("INSERT", "f1")
    m.add_mapping("UPDATE", "f2")
    assert sorted(m.get_event_types()) == ["INSERT", "UPDATE"]


def test_runtime_invoke_success() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: x.get("val", 0) * 2))
    rt = FunctionRuntime(reg)
    result = rt.invoke("f1", {"val": 5})
    assert result.success
    assert result.result == 10
    assert result.duration_ms >= 0


def test_runtime_invoke_failure() -> None:
    reg = FunctionRegistry()

    def bad_handler(x: dict) -> None:
        raise RuntimeError("boom")

    reg.register(ServerlessFunction(name="bad", handler=bad_handler))
    rt = FunctionRuntime(reg)
    result = rt.invoke("bad", {})
    assert not result.success
    assert "boom" in result.error


def test_runtime_invoke_not_found() -> None:
    reg = FunctionRegistry()
    rt = FunctionRuntime(reg)
    with pytest.raises(KeyError):
        rt.invoke("nope", {})


def test_runtime_dispatch_event() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: "ok"))
    reg.register(ServerlessFunction(name="f2", handler=lambda x: "ok"))
    rt = FunctionRuntime(reg)
    event = TriggerEvent(event_type="INSERT", source="pg", payload={})
    results = rt.dispatch_event(event, ["f1", "f2"])
    assert len(results) == 2
    assert all(r.success for r in results)


def test_runtime_get_invocations() -> None:
    reg = FunctionRegistry()
    reg.register(ServerlessFunction(name="f1", handler=lambda x: "ok"))
    rt = FunctionRuntime(reg)
    rt.invoke("f1", {})
    rt.invoke("f1", {})
    assert len(rt.get_invocations("f1")) == 2
    assert len(rt.get_invocations()) == 2


def test_runtime_failed_invocations() -> None:
    reg = FunctionRegistry()

    def bad(x: dict) -> None:
        raise ValueError("err")

    reg.register(ServerlessFunction(name="bad", handler=bad))
    reg.register(ServerlessFunction(name="good", handler=lambda x: "ok"))
    rt = FunctionRuntime(reg)
    rt.invoke("bad", {})
    rt.invoke("good", {})
    assert len(rt.get_failed_invocations()) == 1


def test_runtime_success_rate() -> None:
    reg = FunctionRegistry()

    def sometimes_fail(x: dict) -> str:
        if x.get("fail"):
            raise RuntimeError("fail")
        return "ok"

    reg.register(ServerlessFunction(name="f", handler=sometimes_fail))
    rt = FunctionRuntime(reg)
    rt.invoke("f", {})
    rt.invoke("f", {})
    rt.invoke("f", {"fail": True})
    assert abs(rt.success_rate - 2 / 3) < 0.001


def test_runtime_empty_success_rate() -> None:
    reg = FunctionRegistry()
    rt = FunctionRuntime(reg)
    assert rt.success_rate == 0.0
    assert rt.invocation_count == 0
