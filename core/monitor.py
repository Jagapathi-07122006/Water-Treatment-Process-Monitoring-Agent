"""Rule-based review of supplied water-treatment readings; not a safety controller."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

DEFAULT_LIMITS = {
    "ph": {"min": 6.5, "max": 8.5, "unit": "pH"},
    "turbidity_ntu": {"min": 0.0, "max": 1.0, "unit": "NTU"},
    "free_chlorine_mg_l": {"min": 0.2, "max": 4.0, "unit": "mg/L"},
    "temperature_c": {"min": 0.0, "max": 35.0, "unit": "°C"},
    "flow_rate_m3_h": {"min": 0.0, "max": 1000.0, "unit": "m³/h"},
}


def assess_readings(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Input must be a JSON object")
    readings = payload.get("readings")
    if not isinstance(readings, dict) or not readings:
        raise ValueError("'readings' must be a non-empty object")
    limits = payload.get("limits", DEFAULT_LIMITS)
    if not isinstance(limits, dict):
        raise ValueError("'limits' must be an object")
    findings = []
    reviewed = 0
    for metric, value in readings.items():
        if value is None:
            findings.append({"metric": metric, "status": "MISSING", "severity": "medium", "evidence": "No reading supplied", "action": "Verify sensor availability and collect a valid reading."})
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            findings.append({"metric": metric, "status": "INVALID", "severity": "medium", "evidence": f"Expected numeric reading; received {type(value).__name__}", "action": "Check data type, units, and sensor transmission."})
            continue
        if metric not in limits:
            findings.append({"metric": metric, "status": "UNCONFIGURED", "severity": "low", "value": value, "evidence": "No operating range configured", "action": "Have an authorized process engineer define a validated operating range."})
            continue
        bound = limits[metric]
        if not isinstance(bound, dict) or not isinstance(bound.get("min"), (int, float)) or not isinstance(bound.get("max"), (int, float)) or bound["min"] > bound["max"]:
            raise ValueError(f"Invalid limits for metric '{metric}'")
        reviewed += 1
        low, high = bound["min"], bound["max"]
        if value < low or value > high:
            # Severity reflects configured range excursion only, not health risk.
            span = max(high - low, 1e-12)
            distance = low - value if value < low else value - high
            severity = "high" if distance / span >= 0.25 else "medium"
            findings.append({"metric": metric, "status": "OUT_OF_RANGE", "severity": severity, "value": value, "unit": bound.get("unit", ""), "expected_range": [low, high], "evidence": f"Reading is outside configured range [{low}, {high}]", "action": "Verify the reading and sensor calibration; follow approved site procedures and escalate to qualified operators."})
        else:
            findings.append({"metric": metric, "status": "WITHIN_RANGE", "severity": "info", "value": value, "unit": bound.get("unit", ""), "expected_range": [low, high], "evidence": "Reading is within configured range", "action": "Continue routine monitoring."})
    counts = {key: sum(1 for f in findings if f["status"] == key) for key in ("OUT_OF_RANGE", "MISSING", "INVALID", "UNCONFIGURED", "WITHIN_RANGE")}
    return {"agent": "water-treatment-process-monitoring-agent", "generated_at": datetime.now(timezone.utc).isoformat(), "site_id": payload.get("site_id", "unspecified"), "summary": {"metrics_received": len(readings), "metrics_with_validated_limits": reviewed, "finding_counts": counts, "operator_review_required": any(f["status"] in {"OUT_OF_RANGE", "MISSING", "INVALID", "UNCONFIGURED"} for f in findings)}, "findings": findings, "limitations": ["Ranges are illustrative defaults and may not match local permits, plant design, or applicable standards.", "This tool is a screening aid, not a treatment controller or proof that water is safe.", "Confirm alarms and results using validated instruments, site procedures, and qualified personnel."]}
