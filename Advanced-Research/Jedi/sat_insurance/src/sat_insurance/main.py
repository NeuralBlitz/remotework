from sat_insurance import Satellite
from sat_insurance.models import assess_risk, calculate_premium


def main() -> None:
    sat = Satellite("S1", "Hubble", "LEO", 1990, 2.5e9)
    assessment = assess_risk(sat)
    premium = calculate_premium(assessment)
    print(f"Satellite: {sat.name}")
    print(f"Total risk: {assessment.total_risk:.2%}")
    print(f"Premium: ${premium:,.0f}")


if __name__ == "__main__":
    main()
