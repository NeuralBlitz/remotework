from art_crit import Artwork, Critique
from art_crit.models import compare_artists, style_score


class TestArtwork:
    def test_creation(self) -> None:
        a = Artwork("Mona Lisa", "Da Vinci", 1503, "renaissance")
        assert a.title == "Mona Lisa"

    def test_era_medieval(self) -> None:
        a = Artwork("Test", "Artist", 1300)
        assert a.era == "medieval"

    def test_era_renaissance(self) -> None:
        a = Artwork("Test", "Artist", 1500)
        assert a.era == "renaissance"

    def test_era_contemporary(self) -> None:
        a = Artwork("Test", "Artist", 2000)
        assert a.era == "contemporary"


class TestCritique:
    def test_overall_score(self) -> None:
        c = Critique(Artwork("t", "a", 2000), 8.0, 7.0, 9.0)
        assert c.overall_score == 8.0

    def test_is_masterpiece(self) -> None:
        c = Critique(Artwork("t", "a", 2000), 9.0, 8.0, 8.0)
        assert c.is_masterpiece is True


class TestHelpers:
    def test_style_score(self) -> None:
        assert style_score("impressionist") > style_score("unknown")

    def test_compare_artists(self) -> None:
        artworks = [Artwork("t1", "A", 1900), Artwork("t2", "A", 1920)]
        score = compare_artists(artworks, "A")
        assert score > 0
