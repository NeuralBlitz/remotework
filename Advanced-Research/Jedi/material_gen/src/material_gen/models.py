from material_gen import Material


def generate_perovskite(a: str, b: str, x: str) -> Material:
    formula = f"{a}{b}{x}3"
    return Material(formula=formula, structure="perovskite", bandgap=3.2, stability=0.75)


def calculate_stability(temperature: float, pressure: float) -> float:
    import math

    return math.exp(-temperature / 1000) * pressure


def doping_level(concentration: float) -> str:
    if concentration < 1e19:
        return "low"
    elif concentration < 5e19:
        return "medium"
    return "high"
