# Water Treatment Process Monitoring Agent

A local Python tool that screens supplied water-treatment readings against configured operating ranges and produces explainable review findings.

## Features
- Checks pH, turbidity, free chlorine, temperature, and flow against illustrative default bounds.
- Flags missing, invalid, unconfigured, and out-of-range readings.
- Accepts site-specific `limits` in the input JSON.
- Generates a JSON report with evidence, review actions, and limitations.
- Includes tests, example data, three tool schemas, three skills, and a readiness audit.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python verification/readiness_audit.py
python -m core.cli examples/process_case.json --output report.json
```

## Input format

```json
{
  "site_id": "plant-01",
  "readings": {"ph": 7.2, "turbidity_ntu": 0.4, "free_chlorine_mg_l": 0.5},
  "limits": {"ph": {"min": 6.5, "max": 8.5, "unit": "pH"}}
}
```

If `limits` is provided, it replaces the default map, so include every metric you intend to assess. Bounds are inclusive.

## Safety and limitations
Default bounds are illustrative, not authoritative legal or plant-specific limits. Validate all ranges with qualified process staff and applicable permits. This software does not connect to sensors, SCADA, PLCs, or actuators; it does not control dosing or certify water safety. Use validated measurements, laboratory results, approved site procedures, and qualified human judgment.
