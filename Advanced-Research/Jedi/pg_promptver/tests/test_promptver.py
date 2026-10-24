import pytest

from pg_promptver.builder import PromptBuilder
from pg_promptver.models import PromptTemplate
from pg_promptver.versioner import PromptVersioner


class TestPromptTemplate:
    def test_render(self) -> None:
        t = PromptTemplate(
            name="test",
            system_prompt="You are helpful.",
            user_template="Hello {name}, welcome to {place}.",
            variables=["name", "place"],
        )
        result = t.render(name="Alice", place="Wonderland")
        assert "Alice" in result
        assert "Wonderland" in result

    def test_render_missing_var(self) -> None:
        t = PromptTemplate(
            name="test",
            system_prompt="",
            user_template="Hello {name}",
            variables=["name"],
        )
        result = t.render()
        assert "{name}" in result


class TestPromptBuilder:
    def test_build_basic(self) -> None:
        builder = PromptBuilder()
        template = (
            builder.with_name("greeting")
            .with_system("Be polite.")
            .with_user_template("Hello {name}!")
            .build()
        )
        assert template.name == "greeting"
        assert template.variables == ["name"]

    def test_build_with_options(self) -> None:
        builder = PromptBuilder()
        template = (
            builder.with_name("test")
            .with_user_template("Say {word}")
            .with_model("gpt-3.5")
            .with_temperature(0.2)
            .with_max_tokens(512)
            .build()
        )
        assert template.model == "gpt-3.5"
        assert template.temperature == 0.2
        assert template.max_tokens == 512

    def test_build_no_name_raises(self) -> None:
        builder = PromptBuilder()
        builder.with_user_template("hello")
        with pytest.raises(ValueError, match="name"):
            builder.build()

    def test_build_no_template_raises(self) -> None:
        builder = PromptBuilder()
        builder.with_name("test")
        with pytest.raises(ValueError, match="template"):
            builder.build()

    def test_extract_variables(self) -> None:
        vars_ = PromptBuilder._extract_variables("Hello {name}, age {age}, city {city}")
        assert set(vars_) == {"name", "age", "city"}

    def test_chaining(self) -> None:
        builder = PromptBuilder()
        result = builder.with_name("x").with_system("s").with_user_template("u")
        assert result is builder


class TestPromptVersioner:
    def _make_template(self, name: str = "test", system: str = "sys") -> PromptTemplate:
        return PromptTemplate(name=name, system_prompt=system, user_template="hello {x}")

    def test_commit(self) -> None:
        ver = PromptVersioner()
        v = ver.commit(self._make_template(), message="initial")
        assert v.version_id == "v1"
        assert ver.current is not None
        assert ver.current.version_id == "v1"

    def test_multiple_commits(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template(), message="v1")
        ver.commit(self._make_template(system="updated"), message="v2")
        assert len(ver.list_versions()) == 2

    def test_rollback(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template(system="v1"), message="first")
        ver.commit(self._make_template(system="v2"), message="second")
        ver.rollback("v1")
        assert ver.current is not None
        assert ver.current.template.system_prompt == "v1"

    def test_rollback_invalid_raises(self) -> None:
        ver = PromptVersioner()
        with pytest.raises(KeyError):
            ver.rollback("v999")

    def test_get_by_tag(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template(), tags=("stable",))
        ver.commit(self._make_template(), tags=("beta",))
        stable = ver.get_by_tag("stable")
        assert len(stable) == 1

    def test_diff(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template(system="old"), message="v1")
        ver.commit(self._make_template(system="new"), message="v2")
        changes = ver.diff("v1", "v2")
        assert "system_prompt" in changes
        assert changes["system_prompt"] == ("old", "new")

    def test_diff_same_no_changes(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template(), message="v1")
        changes = ver.diff("v1", "v1")
        assert changes == {}

    def test_diff_invalid_raises(self) -> None:
        ver = PromptVersioner()
        ver.commit(self._make_template())
        with pytest.raises(KeyError):
            ver.diff("v1", "v999")
