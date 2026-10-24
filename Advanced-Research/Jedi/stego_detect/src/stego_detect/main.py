from stego_detect import ImageSteg
from stego_detect.models import analyze_image


def main() -> None:
    img = ImageSteg("test.png", 640, 480, 8)
    result = analyze_image(img)
    print(f"Image: {result.image.image_path}")
    print(f"Has hidden data: {result.has_hidden_data}")


if __name__ == "__main__":
    main()
