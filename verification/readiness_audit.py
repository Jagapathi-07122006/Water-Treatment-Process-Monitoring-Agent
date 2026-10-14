from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'agent.yaml','README.md','SOUL.md','RULES.md','DUTIES.md','AGENTS.md','EXPLAINABILITY.md',
    'requirements.txt','.env.example','.gitignore','pytest.ini','core/__init__.py','core/monitor.py','core/cli.py',
    'tools/assess-water-quality.yaml','tools/detect-process-anomalies.yaml','tools/generate-operations-report.yaml',
    'skills/water-quality-monitoring/SKILL.md','skills/process-anomaly-review/SKILL.md','skills/operations-reporting/SKILL.md',
    'tests/test_monitor.py','examples/process_case.json'
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
manifest = (ROOT / 'agent.yaml').read_text(encoding='utf-8')
if 'name: water-treatment-process-monitoring-agent' not in manifest:
    missing.append('agent.yaml: expected lowercase slug')
if missing:
    print('FAIL:', ', '.join(missing)); sys.exit(1)
print(f'PASS: all {len(REQUIRED)}/{len(REQUIRED)} required files present')
