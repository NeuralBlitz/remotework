from art_crit import Artwork, Critique


def analyze_artwork(artwork: Artwork) -> Critique:
    technical = 7.0
    conceptual = 7.0
    historical = 7.0

    if artwork.style != "unknown":
        technical += 1.0
        conceptual += 1.0

    style_bonus = {"impressionist": 2.0, "renaissance": 2.0, "baroque": 1.5}
    if artwork.style in style_bonus:
        historical += style_bonus[artwork.style]

    return Critique(artwork, technical, conceptual, historical, "Analyzed by AI")


def style_score(style: str) -> float:
    scores = {"impressionist": 8.0, "renaissance": 9.0, "baroque": 7.5, "unknown": 5.0}
    return scores.get(style, 5.0)


def compare_artists(artworks: list[Artwork], artist_name: str) -> float:
    filtered = [a for a in artworks if a.artist == artist_name]
    if not filtered:
        return 0.0
    return len(filtered) * style_score("unknown")
