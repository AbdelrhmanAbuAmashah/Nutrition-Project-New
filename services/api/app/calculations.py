from decimal import ROUND_HALF_UP, Decimal

NUTRIENTS = ("calories", "protein", "carbs", "fat", "fiber", "sodium")
CALCULATION_VERSION = "1"


def rounded(value: Decimal | None):
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) if value is not None else None


def portion(values: dict, grams: Decimal, basis: Decimal = Decimal(100)) -> dict:
    if basis <= 0 or grams <= 0:
        raise ValueError("positive mass required")
    return {
        key: Decimal(str(values[key])) * grams / basis if values.get(key) is not None else None
        for key in NUTRIENTS
    }


def total(rows: list[dict]) -> dict:
    result = {}
    known = {}
    missing = []
    for key in NUTRIENTS:
        values = [Decimal(str(row[key])) for row in rows if row.get(key) is not None]
        known[key] = rounded(sum(values, Decimal(0)))
        if len(values) != len(rows):
            result[key] = None
            missing.append(key)
        else:
            result[key] = known[key]
    return {"values": result, "known_totals": known, "missing": missing, "complete": not missing}


def check_restrictions(
    substances: set[str], ingredient_coverage: str, restrictions: list, allergy_status: str
) -> dict:
    matches = [
        {"substance_id": r.substance_id, "kind": r.kind}
        for r in restrictions
        if r.confirmed and r.substance_id in substances
    ]
    hard = any(r["kind"] in ("allergy", "intolerance") for r in matches)
    status = (
        "conflict"
        if hard
        else "unknown"
        if ingredient_coverage != "documented" or allergy_status == "unknown"
        else "no_recorded_conflict"
    )
    return {
        "status": status,
        "matches": matches,
        "cross_contact": "unknown",
        "recommendation_eligible": not hard and status != "unknown",
    }
