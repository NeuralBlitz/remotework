from art_crit import Artwork
from art_crit.models import analyze_artwork


def main() -> None:
    artwork = Artwork("Starry Night", "Van Gogh", 1889, "post-impressionist")
    critique = analyze_artwork(artwork)
    print(f"Artwork: {artwork.title}")
    print(f"Score: {critique.overall_score:.1f}")


if __name__ == "__main__":
    main()
