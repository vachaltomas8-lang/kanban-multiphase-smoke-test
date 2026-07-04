"""Length converter: m, km, mi, ft — using meters as the base unit."""

# Conversion factors to meters
_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a length value from one unit to another.

    Supported units: m (meters), km (kilometers), mi (miles), ft (feet).

    Args:
        value: The numeric value to convert.
        from_unit: The source unit.
        to_unit: The target unit.

    Returns:
        The converted value as a float.

    Raises:
        ValueError: If either unit is not one of the supported units.
    """
    if from_unit not in _TO_METERS:
        raise ValueError(f"Unknown unit: {from_unit!r}")
    if to_unit not in _TO_METERS:
        raise ValueError(f"Unknown unit: {to_unit!r}")

    # Convert to meters, then to target unit
    meters = value * _TO_METERS[from_unit]
    return meters / _TO_METERS[to_unit]
