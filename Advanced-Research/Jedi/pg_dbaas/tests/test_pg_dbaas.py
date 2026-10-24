from pg_dbaas.factory import DevFactory, ProdFactory, StageFactory
from pg_dbaas.models import DatabaseProfile, DatabaseTier
from pg_dbaas.provisioner import Provisioner


class TestDatabaseProfile:
    def test_frozen(self) -> None:
        p = DatabaseProfile(
            name="x",
            tier=DatabaseTier.DEV,
            host="h",
            port=5432,
            max_connections=10,
            storage_gb=5,
            backup_enabled=False,
            ssl_required=False,
            cpu_cores=1.0,
            ram_gb=2.0,
        )
        try:
            p.name = "y"  # type: ignore[misc]
            assert False
        except AttributeError:
            pass


class TestDevFactory:
    def test_creates_dev_profile(self) -> None:
        f = DevFactory()
        p = f.create_profile("testdb")
        assert p.tier == DatabaseTier.DEV
        assert p.host == "localhost"
        assert not p.backup_enabled
        assert not p.ssl_required

    def test_small_resources(self) -> None:
        f = DevFactory()
        p = f.create_profile("x")
        assert p.max_connections == 10
        assert p.storage_gb == 5


class TestStageFactory:
    def test_creates_stage_profile(self) -> None:
        f = StageFactory()
        p = f.create_profile("stagedb")
        assert p.tier == DatabaseTier.STAGE
        assert p.backup_enabled
        assert not p.ssl_required

    def test_medium_resources(self) -> None:
        f = StageFactory()
        p = f.create_profile("x")
        assert p.max_connections == 50
        assert p.cpu_cores == 2.0


class TestProdFactory:
    def test_creates_prod_profile(self) -> None:
        f = ProdFactory()
        p = f.create_profile("proddb")
        assert p.tier == DatabaseTier.PROD
        assert p.backup_enabled
        assert p.ssl_required

    def test_large_resources(self) -> None:
        f = ProdFactory()
        p = f.create_profile("x")
        assert p.max_connections == 200
        assert p.ram_gb == 64.0


class TestProvisioner:
    def test_provision_dev(self) -> None:
        p = Provisioner()
        profile = p.provision("mydb", DatabaseTier.DEV)
        assert profile.tier == DatabaseTier.DEV
        assert p.count == 1

    def test_provision_prod(self) -> None:
        p = Provisioner()
        profile = p.provision("proddb", DatabaseTier.PROD)
        assert profile.ssl_required

    def test_duplicate_provision_raises(self) -> None:
        p = Provisioner()
        p.provision("dup", DatabaseTier.DEV)
        try:
            p.provision("dup", DatabaseTier.STAGE)
            assert False
        except ValueError:
            pass

    def test_get_profile(self) -> None:
        p = Provisioner()
        p.provision("findme", DatabaseTier.STAGE)
        profile = p.get_profile("findme")
        assert profile is not None
        assert profile.name == "findme"

    def test_list_provisioned(self) -> None:
        p = Provisioner()
        p.provision("b", DatabaseTier.DEV)
        p.provision("a", DatabaseTier.DEV)
        assert p.list_provisioned() == ["a", "b"]

    def test_deprovision(self) -> None:
        p = Provisioner()
        p.provision("gone", DatabaseTier.DEV)
        removed = p.deprovision("gone")
        assert removed.name == "gone"
        assert p.count == 0

    def test_deprovision_missing_raises(self) -> None:
        p = Provisioner()
        try:
            p.deprovision("nope")
            assert False
        except KeyError:
            pass
