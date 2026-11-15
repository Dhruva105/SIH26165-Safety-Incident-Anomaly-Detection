import numpy as np
import pandas as pd

from safety_anomaly.operational_review import IncidentReviewEngine, build_review_prompts


def small_history(n=160):
    return pd.DataFrame({
        "EventDate": pd.date_range("2019-01-01", periods=n, freq="D"),
        "Primary NAICS": ["236220", "311811", "484121", "332710"] * (n // 4),
        "EventTitle": ["Fall to lower level", "Caught in machinery", "Vehicle incident", "Struck by object"] * (n // 4),
        "SourceTitle": ["Ladder", "Conveyor", "Truck", "Metal object"] * (n // 4),
        "Secondary Source Title": ["Floor", "Guard", "Loading dock", "Material"] * (n // 4),
        "Final Narrative": [
            "Worker fell from ladder while accessing elevated work area.",
            "Employee hand caught in conveyor during cleaning task.",
            "Driver injured during vehicle movement in loading area.",
            "Worker struck by falling metal object during handling.",
        ] * (n // 4),
        "NatureTitle": ["Fracture", "Laceration", "Sprain", "Contusion"] * (n // 4),
        "Part of Body Title": ["Leg", "Hand", "Back", "Head"] * (n // 4),
    })


def test_engine_can_fit_and_assess_new_incident():
    engine = IncidentReviewEngine.fit(small_history(), sample_size=160, n_estimators=40)
    assessment = engine.assess({
        "EventDate": "2025-03-14",
        "Primary NAICS": "236220",
        "EventTitle": "Fall to lower level",
        "SourceTitle": "Ladder",
        "Secondary Source Title": "Wet floor",
        "Final Narrative": "Worker slipped while descending an access ladder at the work site.",
    })
    assert 0 <= assessment.reference_percentile <= 100
    assert isinstance(assessment.flagged_for_review, bool)
    assert len(assessment.similar_cases) > 0
    assert assessment.pattern_group.startswith("Pattern group ")
    assert assessment.cluster_size > 0
    assert "dominant_event" in assessment.pattern_summary
    assert "probability" in assessment.limitations


def test_review_prompts_add_category_specific_checks():
    prompts = build_review_prompts("Caught in machinery", "Conveyor", "Hand caught in the moving belt")
    areas = {item["area"] for item in prompts}
    assert "Machine and caught-in hazards" in areas
    assert "Immediate response" in areas
