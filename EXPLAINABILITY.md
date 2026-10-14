# Explainability

## Inputs
The agent accepts a JSON object containing a non-empty `readings` map, an optional `site_id`, and optional per-metric `limits` with numeric `min` and `max` values. If no limits are supplied, illustrative defaults are used.

## Decision
Each metric is assigned one of `WITHIN_RANGE`, `OUT_OF_RANGE`, `MISSING`, `INVALID`, or `UNCONFIGURED`. A supplied numeric value is compared directly with the configured inclusive bounds. The report includes the value, expected range, evidence, and suggested review action. Severity is a simple range-excursion heuristic, not a water-health risk assessment.

## Limits
The tool does not validate legal or site-specific standards, account for sensor uncertainty, infer root causes, control treatment equipment, or certify potable-water safety. Default ranges are illustrative and must be reviewed by qualified staff. It does not replace laboratory testing, validated instruments, permit requirements, or emergency procedures.

## Tool: assess-water-quality
### Inputs and Data Sources
Uses readings and optional limits supplied by the caller.
### Decision and Reasoning
Compares numeric values against configured inclusive lower and upper bounds.
### Outputs and Evidence
Returns status, value, range, unit, evidence, and review action.
### Limits and Constraints
No external standards or sensors are consulted.
### Failure Handling
Rejects empty readings and malformed bounds; flags non-numeric values.
### Human Review
Qualified operators confirm results and limits before operational decisions.

## Tool: detect-process-anomalies
### Inputs and Data Sources
Uses the same caller-supplied reading map and bounds.
### Decision and Reasoning
Treats missing, invalid, unconfigured, and out-of-range values as review flags.
### Outputs and Evidence
Provides per-metric status and reason.
### Limits and Constraints
Flags are deterministic screening findings, not confirmed equipment faults.
### Failure Handling
Invalid input is reported as an error; unusual metrics without limits are not silently passed.
### Human Review
Investigate sensor quality and process context using approved procedures.

## Tool: generate-operations-report
### Inputs and Data Sources
Uses the same input and assessment results.
### Decision and Reasoning
Summarizes finding counts and whether operator review is needed.
### Outputs and Evidence
Returns a JSON report with timestamp, site identifier, findings, summary, and limitations.
### Limits and Constraints
Does not write to plant systems or trigger alarms.
### Failure Handling
CLI errors on missing files, malformed JSON, or invalid input.
### Human Review
Review the report alongside plant logs, calibration records, and lab results.
