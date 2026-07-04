"""Weight converter: kg, g, lb, oz — using kg as the base unit."""

# Conversion factors to kg
_TO_KG = {
    "kg": 1.0,
    "g": 0.001,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a weight value from one unit to another.

    Supported units: kg (kilograms), g (grams), lb (pounds), oz (ounces).

    Args:
        value: The numeric value to convert.
        from_unit: The source unit.
        to_unit: The target unit.

    Returns:
        The converted value as a float.

    Raises:
        ValueError: If either unit is not one of the supported units.
    """
    if from_unit not in _TO_KG:
        raise ValueError(f"Unknown unit: {from_unit!r}")
    if to_unit not in _TO_KG:
        raise ValueError(f"Unknown unit: {to_unit!r}")

    # Convert to kg, then to target unit
    kg = value * _TO_KG[from_unit]
    return kg / _TO_KG[to_unit]
