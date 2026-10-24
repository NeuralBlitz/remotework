import pytest
from cloud_security.iam import IAMManager, Permission, Role
from cloud_security.policies import SecurityPolicy, PolicyEngine, PolicyEffect
from cloud_security.audit import AuditLogger, AuditEvent


def test_create_role() -> None:
    mgr = IAMManager()
    role = mgr.create_role("reader", {Permission.READ})
    assert role.name == "reader"
    assert role.has_permission(Permission.READ)


def test_create_duplicate_role_raises() -> None:
    mgr = IAMManager()
    mgr.create_role("reader")
    with pytest.raises(ValueError):
        mgr.create_role("reader")


def test_grant_permission() -> None:
    mgr = IAMManager()
    mgr.create_role("dev")
    mgr.grant_permission("dev", Permission.WRITE)
    assert mgr.get_role("dev").has_permission(Permission.WRITE)


def test_revoke_permission() -> None:
    mgr = IAMManager()
    mgr.create_role("dev", {Permission.READ, Permission.WRITE})
    mgr.revoke_permission("dev", Permission.WRITE)
    assert not mgr.get_role("dev").has_permission(Permission.WRITE)


def test_assign_role() -> None:
    mgr = IAMManager()
    mgr.create_role("admin", {Permission.ADMIN})
    mgr.assign_role("alice", "admin")
    assert "admin" in mgr.get_user_roles("alice")


def test_assign_unknown_role_raises() -> None:
    mgr = IAMManager()
    with pytest.raises(KeyError):
        mgr.assign_role("bob", "nonexistent")


def test_check_access() -> None:
    mgr = IAMManager()
    mgr.create_role("writer", {Permission.WRITE})
    mgr.assign_role("alice", "writer")
    assert mgr.check_access("alice", Permission.WRITE)
    assert not mgr.check_access("alice", Permission.ADMIN)


def test_role_inheritance() -> None:
    mgr = IAMManager()
    mgr.create_role("base", {Permission.READ})
    mgr.create_role(
        "extended",
        {Permission.WRITE},
    )
    mgr.get_role("extended").inherits_from.append("base")
    mgr.assign_role("user1", "extended")
    assert mgr.check_access("user1", Permission.WRITE)
    assert mgr.check_access("user1", Permission.READ)


def test_remove_role() -> None:
    mgr = IAMManager()
    mgr.create_role("viewer")
    mgr.assign_role("bob", "viewer")
    mgr.remove_role("bob", "viewer")
    assert "viewer" not in mgr.get_user_roles("bob")


def test_policy_allow() -> None:
    engine = PolicyEngine()
    engine.add_policy(SecurityPolicy("p1", PolicyEffect.ALLOW, ["read"], ["*"]))
    assert engine.evaluate("read", "table1")


def test_policy_deny() -> None:
    engine = PolicyEngine()
    engine.add_policy(SecurityPolicy("p1", PolicyEffect.DENY, ["delete"], ["users"]))
    assert not engine.evaluate("delete", "users")


def test_policy_no_match() -> None:
    engine = PolicyEngine()
    engine.add_policy(SecurityPolicy("p1", PolicyEffect.ALLOW, ["read"], ["logs"]))
    assert not engine.evaluate("write", "logs")


def test_policy_remove() -> None:
    engine = PolicyEngine()
    engine.add_policy(SecurityPolicy("p1", PolicyEffect.ALLOW, ["*"], ["*"]))
    assert engine.remove_policy("p1")
    assert engine.policy_count == 0
    assert not engine.remove_policy("p1")


def test_audit_log() -> None:
    logger = AuditLogger()
    logger.log("alice", "SELECT", "users", "success")
    assert logger.event_count == 1


def test_audit_get_events_by_user() -> None:
    logger = AuditLogger()
    logger.log("alice", "SELECT", "t1", "success")
    logger.log("bob", "INSERT", "t2", "success")
    events = logger.get_events("alice")
    assert len(events) == 1
    assert events[0].user == "alice"


def test_audit_failed_events() -> None:
    logger = AuditLogger()
    logger.log("alice", "SELECT", "t1", "success")
    logger.log("bob", "DELETE", "t2", "denied")
    failed = logger.get_failed_events()
    assert len(failed) == 1
    assert failed[0].result == "denied"


def test_audit_clear() -> None:
    logger = AuditLogger()
    logger.log("u", "a", "r", "ok")
    logger.clear()
    assert logger.event_count == 0
