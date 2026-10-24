from typing import Any

from pg_masking.models import MaskingRule, MaskingType
from pg_masking.proxy import MaskingProxy
from pg_masking.rules import EmailMasker, PhoneMasker, RegexMasker, create_masker


class TestMaskingRule:
    def test_frozen(self) -> None:
        r = MaskingRule(field_name="email", masking_type=MaskingType.FULL)
        try:
            r.field_name = "x"  # type: ignore[misc]
            assert False
        except AttributeError:
            pass

    def test_roles_exempt(self) -> None:
        r = MaskingRule(
            field_name="email",
            masking_type=MaskingType.PARTIAL,
            roles_exempt=frozenset({"admin"}),
        )
        assert "admin" in r.roles_exempt


class TestEmailMasker:
    def test_masks_email(self) -> None:
        m = EmailMasker()
        result = m.mask("johndoe@example.com")
        assert result.startswith("j")
        assert "@example.com" in result
        assert "***" in result

    def test_short_local(self) -> None:
        m = EmailMasker()
        result = m.mask("a@b.com")
        assert "@b.com" in result


class TestPhoneMasker:
    def test_masks_phone(self) -> None:
        m = PhoneMasker()
        result = m.mask("555-123-4567")
        assert "4567" in result
        assert "***" in result or "***" in result

    def test_short_value(self) -> None:
        m = PhoneMasker()
        result = m.mask("12")
        assert all(c == "*" for c in result)


class TestRegexMasker:
    def test_with_replacement(self) -> None:
        m = RegexMasker(pattern=r"\d+", replacement="XXX")
        assert m.mask("abc123def") == "abcXXXdef"

    def test_default_mask(self) -> None:
        m = RegexMasker(pattern=r"[a-z]+")
        result = m.mask("hello123")
        assert "123" in result
        assert "hello" not in result


class TestCreateMasker:
    def test_full_mask(self) -> None:
        m = create_masker(MaskingType.FULL)
        assert m.mask("secret") == "****"

    def test_hash_mask(self) -> None:
        m = create_masker(MaskingType.HASH)
        result = m.mask("hello")
        assert len(result) == 12
        assert result != "hello"

    def test_redact_mask(self) -> None:
        m = create_masker(MaskingType.REDACT)
        assert m.mask("anything") == "[REDACTED]"

    def test_invalid_type(self) -> None:
        try:
            create_masker("invalid")  # type: ignore[arg-type]
            assert False
        except ValueError:
            pass


class TestMaskingProxy:
    def _sample_rows(self) -> list[dict[str, Any]]:
        return [
            {"name": "Alice", "email": "alice@example.com", "phone": "555-123-4567"},
            {"name": "Bob", "email": "bob@test.org", "phone": "800-555-0100"},
        ]

    def test_masks_for_regular_role(self) -> None:
        proxy = MaskingProxy(
            [
                MaskingRule(field_name="email", masking_type=MaskingType.PARTIAL),
            ]
        )
        result = proxy.apply(self._sample_rows(), role="viewer")
        assert result[0]["email"] != "alice@example.com"
        assert result[0]["name"] == "Alice"

    def test_exempt_for_admin(self) -> None:
        proxy = MaskingProxy(
            [
                MaskingRule(
                    field_name="email",
                    masking_type=MaskingType.FULL,
                    roles_exempt=frozenset({"admin"}),
                ),
            ]
        )
        result = proxy.apply(self._sample_rows(), role="admin")
        assert result[0]["email"] == "alice@example.com"

    def test_no_rules_passthrough(self) -> None:
        proxy = MaskingProxy()
        rows = self._sample_rows()
        result = proxy.apply(rows, role="anyone")
        assert result == rows

    def test_rule_count(self) -> None:
        proxy = MaskingProxy()
        proxy.add_rule(MaskingRule(field_name="x", masking_type=MaskingType.FULL))
        proxy.add_rule(MaskingRule(field_name="y", masking_type=MaskingType.FULL))
        assert proxy.rule_count == 2

    def test_remove_rule(self) -> None:
        proxy = MaskingProxy(
            [
                MaskingRule(field_name="x", masking_type=MaskingType.FULL),
            ]
        )
        proxy.remove_rule("x")
        assert proxy.rule_count == 0
