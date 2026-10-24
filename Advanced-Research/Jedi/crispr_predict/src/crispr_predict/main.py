from crispr_predict import GuideRNA
from crispr_predict.models import predict_efficiency


def main() -> None:
    guide = GuideRNA(sequence="ATCGATCGATCGATCG")
    result = predict_efficiency(guide)
    print(f"Guide: {guide.sequence}")
    print(f"Efficiency: {result.efficiency:.2f}")
    print(f"Off-target score: {result.off_target_score:.2f}")


if __name__ == "__main__":
    main()
