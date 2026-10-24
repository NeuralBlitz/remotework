"""Tests for core infrastructure modules"""

import sys
import os
import time
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestEventBus:
    def test_import(self):
        from events import EventBus, Event, EventPriority, EventHandler
        from events import EventStore

    def test_event_create(self):
        from events import Event, EventPriority
        event = Event.create("test.event", {"key": "value"}, source="test")
        assert event.type == "test.event"
        assert event.data["key"] == "value"
        assert event.source == "test"
        assert event.priority == EventPriority.NORMAL

    def test_event_to_dict(self):
        from events import Event
        event = Event.create("test", {"a": 1})
        d = event.to_dict()
        assert d["type"] == "test"
        assert d["data"]["a"] == 1

    def test_event_from_dict(self):
        from events import Event
        original = Event.create("test", {"a": 1})
        restored = Event.from_dict(original.to_dict())
        assert restored.type == original.type
        assert restored.data == original.data

    def test_eventbus_subscribe_emit(self):
        from events import EventBus
        bus = EventBus()
        results = []
        bus.subscribe(["test.event"], lambda e: results.append(e.data))
        bus.emit_simple("test.event", {"msg": "hello"})
        assert len(results) == 1
        assert results[0]["msg"] == "hello"

    def test_eventbus_wildcard(self):
        from events import EventBus
        bus = EventBus()
        results = []
        bus.subscribe(["*"], lambda e: results.append(e.type))
        bus.emit_simple("event.a", {})
        bus.emit_simple("event.b", {})
        assert len(results) == 2

    def test_eventbus_history(self):
        from events import EventBus
        bus = EventBus()
        bus.emit_simple("a", {})
        bus.emit_simple("b", {})
        assert len(bus.get_history()) == 2
        assert len(bus.get_history(event_type="a")) == 1

    def test_eventbus_middleware(self):
        from events import EventBus, Event
        bus = EventBus()
        bus.add_middleware(lambda e: None if e.type == "blocked" else e)
        results = []
        bus.subscribe(["*"], lambda e: results.append(e.type))
        bus.emit_simple("allowed", {})
        bus.emit_simple("blocked", {})
        assert results == ["allowed"]

    def test_global_functions(self):
        from events import emit, subscribe, get_event_bus
        results = []
        subscribe(["global.test"], lambda e: results.append(1))
        emit("global.test", {})
        assert len(results) == 1


class TestWorkflow:
    def test_import(self):
        from workflow import Workflow, WorkflowBuilder, StepConfig, StepStatus, WorkflowStatus

    def test_simple_workflow(self):
        from workflow import Workflow, StepConfig

        def step_a(context):
            return {"a": 1}

        def step_b(context):
            return context["step_a"]["a"] + 1

        wf = Workflow("test")
        wf.add_step(StepConfig(name="step_a", func=step_a))
        wf.add_step(StepConfig(name="step_b", func=step_b, depends_on=["step_a"]))

        result = wf.execute()
        assert result.status.value == "success"
        assert result.step_results["step_a"].result == {"a": 1}
        assert result.step_results["step_b"].result == 2

    def test_workflow_failure(self):
        from workflow import Workflow, StepConfig

        def failing_step(context):
            raise ValueError("boom")

        wf = Workflow("test")
        wf.add_step(StepConfig(name="fail", func=failing_step))

        result = wf.execute()
        assert result.status.value == "failed"
        assert "boom" in result.error

    def test_workflow_builder(self):
        from workflow import WorkflowBuilder

        def step_a(context):
            return 1

        def step_b(context):
            return context["a"] + 1

        wf = (WorkflowBuilder("builder-test")
              .step("a", step_a)
              .step("b", step_b, depends_on=["a"])
              .build())

        result = wf.execute()
        assert result.status.value == "success"


class TestScheduler:
    def test_import(self):
        from scheduler import TaskScheduler, CronExpression, ScheduleType, TaskState

    def test_cron_parse(self):
        from scheduler import CronExpression
        cron = CronExpression.parse("*/5 * * * *")
        assert cron.minute == "*/5"
        assert cron.hour == "*"

    def test_cron_matches(self):
        from scheduler import CronExpression
        from datetime import datetime
        cron = CronExpression.parse("0 9 * * *")
        dt = datetime(2024, 1, 15, 9, 0)
        assert cron.matches(dt) is True
        dt2 = datetime(2024, 1, 15, 10, 0)
        assert cron.matches(dt2) is False

    def test_schedule_once(self):
        from scheduler import TaskScheduler, TaskState
        scheduler = TaskScheduler()
        results = []
        task = scheduler.schedule_once("test", lambda: results.append(1), run_at=time.time() - 1)
        scheduler.run_pending()
        assert len(results) == 1
        assert task.state == TaskState.COMPLETED

    def test_schedule_interval(self):
        from scheduler import TaskScheduler, TaskState
        scheduler = TaskScheduler()
        results = []
        task = scheduler.schedule_interval("test", lambda: results.append(1), seconds=0.01, max_runs=3)
        for _ in range(5):
            scheduler.run_pending()
            time.sleep(0.02)
        assert len(results) == 3
        assert task.state == TaskState.COMPLETED


class TestFeatureFlags:
    def test_import(self):
        from features import FeatureFlagManager, FlagType, FeatureFlag

    def test_create_and_check(self):
        from features import FeatureFlagManager, FlagType
        import tempfile
        manager = FeatureFlagManager(flags_file=tempfile.mktemp())
        manager.create("my-feature", FlagType.BOOLEAN, enabled=True)
        assert manager.is_enabled("my-feature") is True
        assert manager.is_enabled("nonexistent") is False

    def test_rollout_percentage(self):
        from features import FeatureFlagManager, FlagType
        import tempfile
        manager = FeatureFlagManager(flags_file=tempfile.mktemp())
        manager.create("rollout", FlagType.BOOLEAN, rollout_percentage=50)
        enabled_count = sum(1 for i in range(100) if manager.is_enabled("rollout", user_id=f"user-{i}"))
        assert 30 < enabled_count < 70  # roughly 50%

    def test_blocked_user(self):
        from features import FeatureFlagManager, FlagType
        import tempfile
        manager = FeatureFlagManager(flags_file=tempfile.mktemp())
        manager.create("feature", FlagType.BOOLEAN, blocked_users={"bad-user"})
        assert manager.is_enabled("feature", user_id="good-user") is True
        assert manager.is_enabled("feature", user_id="bad-user") is False

    def test_segments(self):
        from features import FeatureFlagManager, FlagType
        import tempfile
        manager = FeatureFlagManager(flags_file=tempfile.mktemp())
        manager.create("beta", FlagType.BOOLEAN, segments={"plan": "pro"})
        assert manager.is_enabled("beta", context={"plan": "pro"}) is True
        assert manager.is_enabled("beta", context={"plan": "free"}) is False


class TestSessions:
    def test_import(self):
        from sessions import SessionManager, Session

    def test_create_get(self):
        from sessions import SessionManager
        import tempfile
        mgr = SessionManager(persist_file=tempfile.mktemp())
        session = mgr.create(user_id="user1", ttl=60)
        assert session.user_id == "user1"
        assert mgr.get(session.id) is not None

    def test_set_get_data(self):
        from sessions import SessionManager
        import tempfile
        mgr = SessionManager(persist_file=tempfile.mktemp())
        session = mgr.create()
        session.set("key", "value")
        assert session.get("key") == "value"

    def test_delete(self):
        from sessions import SessionManager
        import tempfile
        mgr = SessionManager(persist_file=tempfile.mktemp())
        session = mgr.create()
        assert mgr.delete(session.id) is True
        assert mgr.get(session.id) is None


class TestAuditLog:
    def test_import(self):
        from audit import AuditLog, AuditLevel, AuditEntry, AuditQueryBuilder, AuditCategory

    def test_log_and_query(self):
        from audit import AuditLog, AuditLevel
        import tempfile
        log = AuditLog(log_dir=tempfile.mkdtemp())
        entry = log.log("user.login", "user1", "auth", level=AuditLevel.INFO)
        assert entry.action == "user.login"
        results = log.query_action(actor="user1")
        assert len(results) == 1

    def test_query_builder(self):
        from audit import AuditLog, AuditLevel, AuditCategory
        import tempfile
        log = AuditLog(log_dir=tempfile.mkdtemp())
        log.log("login", "alice", "auth", category=AuditCategory.AUTH)
        log.log("login", "bob", "auth", category=AuditCategory.AUTH)
        log.log("delete", "alice", "data", level=AuditLevel.WARNING)
        assert log.query().actor("alice").count() == 2
        assert log.query().category(AuditCategory.AUTH).count() == 2

    def test_stats(self):
        from audit import AuditLog, AuditCategory
        import tempfile
        log = AuditLog(log_dir=tempfile.mkdtemp())
        log.log("action1", "u1", "r1", category=AuditCategory.USER)
        log.log("action2", "u2", "r2", category=AuditCategory.API)
        stats = log.get_stats()
        assert stats["total"] == 2
        assert stats["unique_actors"] == 2
        assert "by_category" in stats

    def test_integrity(self):
        from audit import AuditLog
        import tempfile
        log = AuditLog(log_dir=tempfile.mkdtemp())
        log.log("test", "user", "resource")
        result = log.verify_integrity()
        assert result["integrity_rate"] == 1.0

    def test_export(self):
        from audit import AuditLog
        import tempfile
        log = AuditLog(log_dir=tempfile.mkdtemp())
        log.log("test", "user", "resource")
        json_str = log.export_json()
        assert "test" in json_str
        csv_str = log.export_csv()
        assert "test" in csv_str


class TestMessageQueue:
    def test_import(self):
        from msgqueue import MessageQueue, MessagePriority, MessageState, Message

    def test_enqueue_dequeue(self):
        from msgqueue import MessageQueue, MessagePriority
        q = MessageQueue()
        msg = q.enqueue("test", {"data": "hello"}, MessagePriority.HIGH)
        assert q.queue_size("test") == 1
        dequeued = q.dequeue("test")
        assert dequeued.body["data"] == "hello"
        assert dequeued.state.value == "processing"

    def test_complete(self):
        from msgqueue import MessageQueue
        q = MessageQueue()
        msg = q.enqueue("test", {"a": 1})
        dequeued = q.dequeue("test")
        q.complete(dequeued.id)
        stats = q.get_stats()
        assert stats["completed"] == 1

    def test_priority_ordering(self):
        from msgqueue import MessageQueue, MessagePriority
        q = MessageQueue()
        q.enqueue("test", {"pri": "low"}, MessagePriority.LOW)
        q.enqueue("test", {"pri": "critical"}, MessagePriority.CRITICAL)
        msg = q.dequeue("test")
        assert msg.body["pri"] == "critical"

    def test_purge(self):
        from msgqueue import MessageQueue
        q = MessageQueue()
        q.enqueue("test", {})
        q.enqueue("test", {})
        assert q.purge("test") == 2
        assert q.queue_size("test") == 0


class TestHTTPClient:
    def test_import(self):
        from httpclient import HTTPClient, GraphQLClient, APIClient, Response

    def test_client_init(self):
        from httpclient import HTTPClient
        client = HTTPClient("https://httpbin.org", headers={"X-Test": "1"})
        assert client.base_url == "https://httpbin.org"
        assert client.default_headers["X-Test"] == "1"

    def test_graphql_client_init(self):
        from httpclient import GraphQLClient
        client = GraphQLClient("https://api.example.com/graphql", headers={"Auth": "token"})
        assert client.endpoint == "https://api.example.com/graphql"

    def test_api_client_init(self):
        from httpclient import APIClient
        client = APIClient("https://api.example.com", token="tok123")
        assert client.client.base_url == "https://api.example.com"


class TestResilience:
    def test_import(self):
        from resilience import CircuitBreaker, CircuitBreakerConfig, CircuitState
        from resilience import RetryPolicy, Bulkhead, Timeout, FallbackChain
        from resilience import circuit_breaker, retry, bulkhead, timeout, fallback

    def test_circuit_breaker_closed(self):
        from resilience import CircuitBreaker, CircuitState
        cb = CircuitBreaker("test")
        assert cb.state == CircuitState.CLOSED
        result = cb.call(lambda: 42)
        assert result == 42

    def test_circuit_breaker_opens(self):
        from resilience import CircuitBreaker, CircuitBreakerConfig, CircuitState
        config = CircuitBreakerConfig(failure_threshold=2)
        cb = CircuitBreaker("test", config)

        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
            except:
                pass

        assert cb.state == CircuitState.OPEN

    def test_circuit_breaker_decorator(self):
        from resilience import circuit_breaker, CircuitState

        @circuit_breaker("test-dec")
        def my_func():
            return "ok"

        assert my_func() == "ok"
        assert my_func.circuit_breaker.state == CircuitState.CLOSED

    def test_retry_success(self):
        from resilience import RetryPolicy
        call_count = [0]

        def flaky():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("flaky")
            return "success"

        policy = RetryPolicy(max_attempts=5, base_delay=0.01)
        result = policy.execute(flaky)
        assert result == "success"
        assert call_count[0] == 3

    def test_retry_decorator(self):
        from resilience import retry

        @retry(max_attempts=3, base_delay=0.01)
        def always_ok():
            return "ok"

        assert always_ok() == "ok"

    def test_bulkhead(self):
        from resilience import Bulkhead
        bh = Bulkhead("test", max_concurrent=2)
        result = bh.call(lambda: "ok")
        assert result == "ok"
        stats = bh.get_stats()
        assert stats["max_concurrent"] == 2


class TestHealthChecks:
    def test_import(self):
        from health import HealthCheck, HealthRegistry, HealthStatus, CheckResult
        from health import check_disk_space, check_port, get_health_registry

    def test_registry(self):
        from health import HealthRegistry, HealthStatus
        registry = HealthRegistry()
        registry.register("test", lambda: {"status": "healthy", "message": "OK"})
        status = registry.get_status()
        assert status == HealthStatus.HEALTHY

    def test_registry_unhealthy(self):
        from health import HealthRegistry, HealthStatus
        registry = HealthRegistry()
        registry.register("failing", lambda: (_ for _ in ()).throw(ValueError("down")))
        status = registry.get_status()
        assert status == HealthStatus.UNHEALTHY

    def test_report(self):
        from health import HealthRegistry
        registry = HealthRegistry()
        registry.register("test", lambda: {"status": "healthy", "message": "OK"})
        report = registry.get_report()
        assert report["status"] == "healthy"
        assert report["summary"]["total"] == 1

    def test_check_disk_space(self):
        from health import check_disk_space
        result = check_disk_space("/", min_free_gb=0.001)
        assert result["status"] in ("healthy", "unhealthy")

    def test_check_port_closed(self):
        from health import check_port
        result = check_port("localhost", 19999, timeout=1)
        assert result["status"] == "unhealthy"


class TestCrypto:
    def test_import(self):
        from crypto import sha256, hmac_sign, jwt_encode, jwt_decode, generate_token

    def test_sha256(self):
        from crypto import sha256
        assert sha256("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    def test_hmac_sign_verify(self):
        from crypto import hmac_sign, hmac_verify
        sig = hmac_sign("data", "secret")
        assert hmac_verify("data", "secret", sig)
        assert not hmac_verify("wrong", "secret", sig)

    def test_jwt(self):
        from crypto import jwt_encode, jwt_decode
        token = jwt_encode({"user": "test"}, "secret")
        payload = jwt_decode(token, "secret")
        assert payload["user"] == "test"

    def test_generate_token(self):
        from crypto import generate_token
        token = generate_token(16)
        assert len(token) > 0

    def test_base64(self):
        from crypto import encode_base64, decode_base64
        encoded = encode_base64("hello")
        assert decode_base64(encoded) == b"hello"

    def test_sha3(self):
        from crypto import sha3_256, sha3_512
        h = sha3_256("test")
        assert len(h) == 64
        h2 = sha3_512("test")
        assert len(h2) == 128

    def test_blake2(self):
        from crypto import blake2b, blake2s
        h = blake2b("test")
        assert len(h) == 128
        h2 = blake2s("test")
        assert len(h2) == 64

    def test_hash_with_salt(self):
        from crypto import hash_with_salt, verify_with_salt
        hashed, salt = hash_with_salt("password")
        assert verify_with_salt("password", hashed, salt)
        assert not verify_with_salt("wrong", hashed, salt)

    def test_jwt_with_claims(self):
        from crypto import jwt_encode, jwt_decode, jwt_get_claims
        token = jwt_encode({"user": "test"}, "secret", issuer="mito", audience="api")
        payload = jwt_decode(token, "secret", issuer="mito", audience="api")
        assert payload["user"] == "test"
        assert payload["iss"] == "mito"
        claims = jwt_get_claims(token)
        assert claims["user"] == "test"

    def test_api_key(self):
        from crypto import generate_api_key
        key = generate_api_key("sk")
        assert key.startswith("sk_")

    def test_password_strength(self):
        from crypto import password_strength
        result = password_strength("MyStr0ng!Pass")
        assert result["strength"] in ("strong", "very_strong")
        weak = password_strength("password")
        assert weak["strength"] == "weak"

    def test_hash_multiple(self):
        from crypto import hash_multiple
        import tempfile, os
        f = tempfile.NamedTemporaryFile(delete=False, mode="w")
        f.write("test data")
        f.close()
        hashes = hash_multiple(f.name, ["md5", "sha256"])
        assert "md5" in hashes
        assert "sha256" in hashes
        os.unlink(f.name)

    def test_derive_key_pbkdf2(self):
        from crypto import derive_key_pbkdf2
        key, salt = derive_key_pbkdf2("password", iterations=1000)
        assert len(key) == 32
        assert len(salt) == 16

    def test_generate_variants(self):
        from crypto import generate_uuid, generate_nanoid, generate_otp
        assert len(generate_uuid()) == 36
        assert len(generate_nanoid()) == 21
        assert len(generate_otp(6)) == 6
        assert len(generate_otp(8, alphanumeric=True)) == 8


class TestSerializers:
    def test_import(self):
        from serializers import to_json, from_json, to_csv, from_csv

    def test_json_roundtrip(self):
        from serializers import to_json, from_json
        data = {"a": 1, "b": [2, 3]}
        assert from_json(to_json(data)) == data

    def test_csv_roundtrip(self):
        from serializers import to_csv, from_csv
        rows = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
        text = to_csv(rows)
        assert len(from_csv(text)) == 2

    def test_flatten_unflatten(self):
        from serializers import flatten_dict, unflatten_dict
        d = {"a": {"b": {"c": 1}}}
        flat = flatten_dict(d)
        assert flat["a.b.c"] == 1
        assert unflatten_dict(flat) == d

    def test_deep_merge(self):
        from serializers import deep_merge
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = deep_merge(base, override)
        assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}


class TestDateTimeUtils:
    def test_import(self):
        from datetime_utils import now, utcnow, format, relative_time

    def test_now(self):
        from datetime_utils import now
        assert now() is not None

    def test_format(self):
        from datetime_utils import format
        from datetime import datetime
        dt = datetime(2024, 1, 15, 10, 30, 0)
        assert format(dt, "%Y-%m-%d") == "2024-01-15"

    def test_add_days(self):
        from datetime_utils import add_days
        from datetime import datetime
        dt = datetime(2024, 1, 1)
        result = add_days(dt, 5)
        assert result.day == 6

    def test_start_of_day(self):
        from datetime_utils import start_of_day
        sod = start_of_day()
        assert sod.hour == 0
        assert sod.minute == 0

    def test_is_weekend(self):
        from datetime_utils import is_weekend
        from datetime import datetime
        saturday = datetime(2024, 1, 13)
        assert is_weekend(saturday) is True

    def test_timer(self):
        from datetime_utils import Timer
        import time
        t = Timer()
        t.start()
        time.sleep(0.01)
        elapsed = t.stop()
        assert elapsed > 0


class TestStrings:
    def test_import(self):
        from strings import slugify, truncate, snake_case, camel_case

    def test_slugify(self):
        from strings import slugify
        assert slugify("Hello World!") == "hello-world"

    def test_truncate(self):
        from strings import truncate
        assert truncate("hello world", 8) == "hello..."

    def test_snake_case(self):
        from strings import snake_case
        assert snake_case("HelloWorld") == "hello_world"
        assert snake_case("hello-world") == "hello_world"

    def test_camel_case(self):
        from strings import camel_case
        assert camel_case("hello_world") == "helloWorld"

    def test_pascal_case(self):
        from strings import pascal_case
        assert pascal_case("hello_world") == "HelloWorld"

    def test_random_string(self):
        from strings import random_string
        s = random_string(10)
        assert len(s) == 10

    def test_is_email(self):
        from strings import is_email
        assert is_email("test@example.com") is True
        assert is_email("not-an-email") is False

    def test_extract_emails(self):
        from strings import extract_emails
        emails = extract_emails("Contact us at info@test.com or support@test.com")
        assert len(emails) == 2

    def test_levenshtein(self):
        from strings import levenshtein
        assert levenshtein("kitten", "sitting") == 3

    def test_similarity(self):
        from strings import similarity
        assert similarity("hello", "hello") == 1.0
        assert similarity("hello", "world") < 1.0


class TestValidators:
    def test_import(self):
        from validators import is_email, is_url, is_ipv4, is_uuid

    def test_email(self):
        from validators import is_email
        assert is_email("test@example.com")
        assert not is_email("bad")

    def test_url(self):
        from validators import is_url
        assert is_url("https://example.com")
        assert not is_url("not a url")

    def test_ipv4(self):
        from validators import is_ipv4
        assert is_ipv4("192.168.1.1")
        assert not is_ipv4("999.999.999.999")

    def test_uuid(self):
        from validators import is_uuid
        assert is_uuid("550e8400-e29b-41d4-a716-446655440000")

    def test_credit_card(self):
        from validators import is_credit_card
        assert is_credit_card("4532015112830366")  # valid Luhn

    def test_slug(self):
        from validators import is_slug
        assert is_slug("hello-world")
        assert not is_slug("Hello World!")

    def test_semver(self):
        from validators import is_semver
        assert is_semver("1.2.3")
        assert is_semver("1.0.0-beta.1")

    def test_validator_class(self):
        from validators import Validator
        v = Validator()
        v.field("email").required().email()
        v.field("name").required().min_len(2)
        assert v.is_valid({"email": "test@example.com", "name": "Alice"})
        assert not v.is_valid({"email": "bad", "name": ""})


class TestParsers:
    def test_import(self):
        from parsers import parse_env, parse_ini, parse_query_string

    def test_parse_env(self):
        from parsers import parse_env
        result = parse_env("KEY=value\n# comment\nFOO=bar")
        assert result["KEY"] == "value"
        assert result["FOO"] == "bar"

    def test_parse_ini(self):
        from parsers import parse_ini
        result = parse_ini("[section]\nkey=value")
        assert result["section"]["key"] == "value"

    def test_query_string(self):
        from parsers import parse_query_string, build_query_string
        params = parse_query_string("a=1&b=2")
        assert params["a"] == "1"
        assert build_query_string(params) == "a=1&b=2"

    def test_parse_headers(self):
        from parsers import parse_headers
        result = parse_headers("Content-Type: application/json\nAuthorization: Bearer token")
        assert result["Content-Type"] == "application/json"

    def test_parse_size(self):
        from parsers import parse_size, format_size
        assert parse_size("1KB") == 1024
        assert parse_size("1MB") == 1048576
        assert "KB" in format_size(2048)

    def test_parse_duration(self):
        from parsers import parse_duration
        assert parse_duration("30s") == 30.0
        assert parse_duration("5m") == 300.0
        assert parse_duration("2h") == 7200.0


class TestGenerators:
    def test_import(self):
        from generators import uuid4, password, mock_user, lorem_words

    def test_uuid(self):
        from generators import uuid4
        u = uuid4()
        assert len(u) == 36

    def test_password(self):
        from generators import password
        pwd = password(20)
        assert len(pwd) == 20

    def test_mock_user(self):
        from generators import mock_user
        user = mock_user()
        assert "email" in user
        assert "first_name" in user

    def test_mock_list(self):
        from generators import mock_list, mock_user
        users = mock_list(mock_user, 5)
        assert len(users) == 5

    def test_lorem(self):
        from generators import lorem_words, lorem_paragraphs
        assert len(lorem_words(20).split()) == 20
        assert len(lorem_paragraphs(2).split("\n\n")) == 2

    def test_random_ip(self):
        from generators import random_ip
        ip = random_ip()
        parts = ip.split(".")
        assert len(parts) == 4


class TestProviders:
    def test_import(self):
        from providers import MistralProvider, CohereProvider, GroqProvider
        from providers import TogetherProvider, OllamaProvider, FireworksProvider
        from providers import LLMRouter, ChatMessage

    def test_chat_message(self):
        from providers import ChatMessage
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_llm_router(self):
        from providers import LLMRouter
        router = LLMRouter()
        available = router.available_providers()
        assert isinstance(available, list)


class TestVectorStores:
    def test_import(self):
        from vectorstores import VectorStore, VectorDocument

    def test_add_search(self):
        from vectorstores import VectorStore, VectorDocument
        import uuid
        store = VectorStore(dimension=3)
        store.add(VectorDocument(id=str(uuid.uuid4()), content="hello", embedding=[1.0, 0.0, 0.0]))
        store.add(VectorDocument(id=str(uuid.uuid4()), content="world", embedding=[0.0, 1.0, 0.0]))
        results = store.search([1.0, 0.0, 0.0], top_k=1)
        assert len(results) == 1
        assert results[0][0].content == "hello"
        assert results[0][1] > 0.9

    def test_delete(self):
        from vectorstores import VectorStore, VectorDocument
        store = VectorStore()
        doc = VectorDocument(id="test", content="test", embedding=[1.0, 0.0])
        store.add(doc)
        assert store.count() == 1
        store.delete("test")
        assert store.count() == 0

    def test_save_load(self):
        from vectorstores import VectorStore, VectorDocument
        import tempfile, os
        store = VectorStore(dimension=2)
        store.add(VectorDocument(id="a", content="hello", embedding=[1.0, 0.0]))
        path = tempfile.mktemp(suffix=".json")
        store.save(path)
        store2 = VectorStore(dimension=2)
        store2.load(path)
        assert store2.count() == 1
        os.unlink(path)

    def test_stats(self):
        from vectorstores import VectorStore, VectorDocument
        store = VectorStore(dimension=3)
        store.add(VectorDocument(id="1", content="hello world", embedding=[1.0, 0.0, 0.0]))
        stats = store.get_stats()
        assert stats["count"] == 1
        assert stats["dimension"] == 3


class TestPrompts:
    def test_import(self):
        from prompts import PromptTemplate, FewShotTemplate, PromptChain, PromptLibrary

    def test_template_render(self):
        from prompts import PromptTemplate
        t = PromptTemplate("test", "Hello {{name}}, welcome to {{place}}")
        result = t.render(name="Alice", place="Wonderland")
        assert "Alice" in result
        assert "Wonderland" in result

    def test_template_variables(self):
        from prompts import PromptTemplate
        t = PromptTemplate("test", "{{a}} and {{b}}")
        assert set(t.variables) == {"a", "b"}

    def test_template_validate(self):
        from prompts import PromptTemplate
        t = PromptTemplate("test", "{{a}} {{b}}")
        assert len(t.validate(a=1)) == 1
        assert len(t.validate(a=1, b=2)) == 0

    def test_few_shot(self):
        from prompts import FewShotTemplate, FewShotExample
        fs = FewShotTemplate("classify", "Classify sentiment")
        fs.add_example("I love it", "positive")
        fs.add_example("Terrible", "negative")
        result = fs.render("This is great")
        assert "positive" in result
        assert "negative" in result
        assert "This is great" in result

    def test_library(self):
        from prompts import PromptLibrary
        lib = PromptLibrary()
        assert lib.get("summarize") is not None
        result = lib.render("summarize", text="Hello world", style="brief")
        assert "Hello world" in result

    def test_library_search(self):
        from prompts import PromptLibrary
        lib = PromptLibrary()
        results = lib.search("code")
        assert len(results) > 0

    def test_chain(self):
        from prompts import PromptTemplate, PromptChain
        chain = PromptChain("test")
        chain.add_step(PromptTemplate("step1", "First: {{input}}"), output_key="step1")
        chain.add_step(PromptTemplate("step2", "Second: {{step1}}"), output_key="step2")
        results = chain.render({"input": "hello"})
        assert len(results) == 2


class TestAgentsExtended:
    def test_research_agent(self):
        from agents import ResearchAgent
        agent = ResearchAgent()
        result = agent.research("AI safety", depth=2)
        assert result["topic"] == "AI safety"
        assert len(result["questions"]) == 2

    def test_code_agent(self):
        from agents import CodeAgent
        agent = CodeAgent()
        code = agent.generate("hello world function", "python")
        assert "python" in code
        issues = agent.review("print('hello') # TODO")
        assert len(issues) >= 1

    def test_data_agent(self):
        from agents import DataAgent
        agent = DataAgent()
        result = agent.analyze([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        assert result["row_count"] == 2
        assert "a" in result["columns"]

    def test_planner_agent(self):
        from agents import PlannerAgent
        agent = PlannerAgent()
        steps = agent.plan("Build a website")
        assert len(steps) == 4
        result = agent.execute_plan(0)
        assert result["completed"] is True


class TestFormatters:
    def test_import(self):
        from formatters import table, box, colored, tree, progress_bar

    def test_table(self):
        from formatters import table
        result = table([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        assert "a" in result
        assert "1" in result

    def test_box(self):
        from formatters import box
        result = box("hello")
        assert "hello" in result
        assert "┌" in result

    def test_colored(self):
        from formatters import colored, red, green
        assert "hello" in colored("hello", "red")
        assert "hello" in red("hello")
        assert "hello" in green("hello")

    def test_tree(self):
        from formatters import tree
        result = tree({"a": 1, "b": {"c": 2}})
        assert "a:" in result
        assert "c:" in result

    def test_progress_bar(self):
        from formatters import progress_bar
        bar = progress_bar(50, 100)
        assert "50.0%" in bar

    def test_markdown_table(self):
        from formatters import markdown_table
        result = markdown_table([{"name": "Alice", "age": 30}])
        assert "name" in result
        assert "---" in result

    def test_success_error(self):
        from formatters import success, error, warning
        assert "✓" in success("ok")
        assert "✗" in error("fail")
        assert "⚠" in warning("warn")


class TestConverters:
    def test_import(self):
        from converters import dict_to_xml, xml_to_dict, toml_to_dict

    def test_xml_roundtrip(self):
        from converters import dict_to_xml, xml_to_dict
        data = {"root": {"name": "test", "value": "42"}}
        xml = dict_to_xml(data["root"], "root")
        assert "test" in xml
        parsed = xml_to_dict(xml)
        assert parsed["root"]["name"] == "test"

    def test_toml(self):
        from converters import toml_to_dict, dict_to_toml
        toml_str = '[section]\nkey = "value"'
        result = toml_to_dict(toml_str)
        assert result["section"]["key"] == "value"

    def test_hex_bytes(self):
        from converters import hex_to_bytes, bytes_to_hex
        assert bytes_to_hex(b"\x48\x65\x6c\x6c\x6f") == "48656c6c6f"
        assert hex_to_bytes("48656c6c6f") == b"Hello"

    def test_binary(self):
        from converters import int_to_binary, binary_to_int
        assert int_to_binary(10) == "00001010"
        assert binary_to_int("00001010") == 10

    def test_roman(self):
        from converters import int_to_roman, roman_to_int
        assert int_to_roman(42) == "XLII"
        assert roman_to_int("XLII") == 42

    def test_temperature(self):
        from converters import celsius_to_fahrenheit, fahrenheit_to_celsius
        assert celsius_to_fahrenheit(0) == 32
        assert fahrenheit_to_celsius(32) == 0

    def test_rgb_hex(self):
        from converters import rgb_to_hex, hex_to_rgb
        assert rgb_to_hex(255, 128, 0) == "#ff8000"
        assert hex_to_rgb("#ff8000") == (255, 128, 0)

    def test_markdown_to_plain(self):
        from converters import markdown_to_plain
        assert markdown_to_plain("# Hello **world**") == "Hello world"

    def test_json_csv(self):
        from converters import json_to_csv, csv_to_json
        data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        csv_str = json_to_csv(data)
        assert "a" in csv_str
        result = csv_to_json(csv_str)
        assert len(result) == 2


class TestKnowledgeGraph:
    def test_import(self):
        from knowledge import KnowledgeGraph, Entity, Relation

    def test_add_entities(self):
        from knowledge import KnowledgeGraph, Entity
        kg = KnowledgeGraph()
        kg.add_entity(Entity(id="e1", type="person", name="Alice"))
        kg.add_entity(Entity(id="e2", type="person", name="Bob"))
        assert kg.get_entity("e1").name == "Alice"
        assert len(kg.find_by_name("Alice")) == 1

    def test_relations(self):
        from knowledge import KnowledgeGraph, Entity, Relation
        kg = KnowledgeGraph()
        kg.add_entity(Entity(id="a", type="person", name="Alice"))
        kg.add_entity(Entity(id="b", type="person", name="Bob"))
        kg.add_relation(Relation(source="a", target="b", type="knows"))
        rels = kg.get_relations("a")
        assert len(rels) == 1
        assert rels[0].type == "knows"

    def test_neighbors(self):
        from knowledge import KnowledgeGraph, Entity, Relation
        kg = KnowledgeGraph()
        kg.add_entity(Entity(id="a", type="p", name="A"))
        kg.add_entity(Entity(id="b", type="p", name="B"))
        kg.add_entity(Entity(id="c", type="p", name="C"))
        kg.add_relation(Relation(source="a", target="b", type="r"))
        kg.add_relation(Relation(source="b", target="c", type="r"))
        neighbors = kg.get_neighbors("a")
        assert isinstance(neighbors, set)

    def test_stats(self):
        from knowledge import KnowledgeGraph, Entity, Relation
        kg = KnowledgeGraph()
        kg.add_entity(Entity(id="a", type="person", name="A"))
        kg.add_entity(Entity(id="b", type="org", name="B"))
        stats = kg.get_stats()
        assert stats["entities"] == 2
        assert "person" in stats["entity_types"]


class TestMiddleware:
    def test_import(self):
        from middleware import CORSMiddleware, AuthMiddleware, RateLimitMiddleware
        from middleware import RequestIDMiddleware, LoggingMiddleware, MiddlewareStack

    def test_cors(self):
        from middleware import CORSMiddleware, MiddlewareContext
        mw = CORSMiddleware()
        ctx = MiddlewareContext("req-1", "/api", "OPTIONS", {}, 0, {})
        result = mw.process_request(ctx)
        assert result is not None
        assert result["status"] == 204

    def test_auth(self):
        from middleware import AuthMiddleware, MiddlewareContext
        mw = AuthMiddleware(api_keys=["valid-key"])
        ctx = MiddlewareContext("req-1", "/api", "GET", {"Authorization": "Bearer valid-key"}, 0, {})
        assert mw.process_request(ctx) is None
        ctx2 = MiddlewareContext("req-2", "/api", "GET", {}, 0, {})
        assert mw.process_request(ctx2) is not None

    def test_rate_limit(self):
        from middleware import RateLimitMiddleware, MiddlewareContext
        mw = RateLimitMiddleware(rate=2, period=60, key_func=lambda c: "test")
        ctx = MiddlewareContext("r1", "/api", "GET", {}, 0, {})
        assert mw.process_request(ctx) is None
        assert mw.process_request(ctx) is None
        assert mw.process_request(ctx)["status"] == 429

    def test_stack(self):
        from middleware import MiddlewareStack, RequestIDMiddleware, LoggingMiddleware, MiddlewareContext
        stack = MiddlewareStack()
        stack.add(RequestIDMiddleware())
        stack.add(LoggingMiddleware())
        ctx = MiddlewareContext("r1", "/api", "GET", {}, 0, {})
        response = {"status": 200, "body": "ok"}
        result = stack.process_response(ctx, response)
        assert "X-Request-ID" in result.get("headers", {})
