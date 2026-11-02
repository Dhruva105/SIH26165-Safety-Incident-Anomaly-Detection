import pandas as pd
from safety_anomaly.features.build import build_features


def test_structured_text_features_are_finite_and_dense():
    n = 40
    frame = pd.DataFrame({
        "Primary NAICS": ["111111", "222222"] * 20,
        "EventTitle": ["Fall from height", "Caught in machinery"] * 20,
        "SourceTitle": ["Ladder", "Machine"] * 20,
        "Secondary Source Title": ["Floor", "Guard"] * 20,
        "NatureTitle": ["Fracture", "Laceration"] * 20,
        "Part of Body Title": ["Leg", "Hand"] * 20,
        "Final Narrative": ["worker fell from ladder injury", "worker hand caught in machine"] * 20,
        "EventDate": pd.date_range("2020-01-01", periods=n, freq="D"),
    })
    result = build_features(frame, representation="structured_text", svd_components=8, text_min_df=1, min_category_frequency=2)
    assert result.X.shape[0] == n
    assert result.X.shape[1] >= 2
    assert result.X.isfinite().all() if hasattr(result.X, "isfinite") else __import__("numpy").isfinite(result.X).all()
