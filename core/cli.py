"""Command line interface for the water treatment monitoring agent."""
import argparse, json
from pathlib import Path
from .monitor import assess_readings

def main():
    parser = argparse.ArgumentParser(description="Review water treatment process readings")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = assess_readings(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
