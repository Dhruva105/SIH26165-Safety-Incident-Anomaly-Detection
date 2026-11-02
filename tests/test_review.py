import pandas as pd
from safety_anomaly.evaluation.review import create_blinded_review_sheet, public_anomaly_export


def test_blinded_review_and_public_export_hide_identifiers():
    frame = pd.DataFrame({
        "UPA": [1, 2, 3, 4], "Employer": ["A", "B", "C", "D"],
        "EventDate": ["2020-01-01"] * 4, "EventTitle": ["Fall"] * 4,
        "Final Narrative": ["worker fell"] * 4,
    })
    review = create_blinded_review_sheet(frame, [-1, -1, 1, 1], [-1, 1, -1, 1], sample_per_group=2)
    assert "UPA" not in review.columns
    assert "model_label" not in review.columns
    public = public_anomaly_export(frame, [-1, 1, -1, 1], [1.0, 0.2, 0.8, 0.1])
    assert "Employer" not in public.columns
    assert "UPA" not in public.columns
    assert "Final Narrative" not in public.columns
