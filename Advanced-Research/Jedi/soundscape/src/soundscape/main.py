from soundscape.models import generate_ambient


def main() -> None:
    sound = generate_ambient("forest", base_freq=220, num_layers=4)
    print(f"Sound: {sound.name}")
    print(f"Layers: {len(sound.layers)}")


if __name__ == "__main__":
    main()
