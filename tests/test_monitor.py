import pytest
from core.monitor import assess_readings


def test_in_range_readings():
    report = assess_readings({"readings": {"ph": 7.1, "free_chlorine_mg_l": 0.5}})
    assert report["summary"]["finding_counts"]["WITHIN_RANGE"] == 2
    assert report["summary"]["operator_review_required"] is False


def test_out_of_range_flagged():
    report = assess_readings({"readings": {"turbidity_ntu": 1.8}})
    assert report["findings"][0]["status"] == "OUT_OF_RANGE"
    assert report["summary"]["operator_review_required"] is True


def test_missing_reading_flagged():
    report = assess_readings({"readings": {"ph": None}})
    assert report["findings"][0]["status"] == "MISSING"


def test_unknown_metric_not_silently_accepted():
    report = assess_readings({"readings": {"new_sensor": 12}})
    assert report["findings"][0]["status"] == "UNCONFIGURED"


def test_invalid_value_flagged():
    report = assess_readings({"readings": {"ph": "7.0"}})
    assert report["findings"][0]["status"] == "INVALID"


def test_rejects_empty_readings():
    with pytest.raises(ValueError):
        assess_readings({"readings": {}})


def test_rejects_bad_limits():
    with pytest.raises(ValueError):
        assess_readings({"readings": {"ph": 7}, "limits": {"ph": {"min": 9, "max": 2}}})


def test_report_contains_limitations():
    report = assess_readings({"readings": {"ph": 7}})
    assert len(report["limitations"]) >= 3
