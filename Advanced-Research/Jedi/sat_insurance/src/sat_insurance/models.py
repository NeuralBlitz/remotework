from sat_insurance import RiskAssessment, Satellite


def assess_risk(satellite: Satellite) -> RiskAssessment:
    launch_risk = 0.05 if satellite.launch_year > 2010 else 0.1
    orbital_risk = orbital_decay_rate(satellite.orbit_type)
    debris_risk = 0.02 + (satellite.age * 0.005)
    return RiskAssessment(satellite, launch_risk, orbital_risk, debris_risk)


def calculate_premium(assessment: RiskAssessment) -> float:
    return assessment.satellite.value_usd * assessment.premium_rate


def orbital_decay_rate(orbit_type: str) -> float:
    rates = {"LEO": 0.15, "MEO": 0.05, "GEO": 0.01, "HEO": 0.03}
    return rates.get(orbit_type, 0.1)
