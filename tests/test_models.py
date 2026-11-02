import numpy as np
from safety_anomaly.models.detectors import run_isolation_forest, run_lof


def test_detectors_return_expected_shapes():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(120, 5)).astype("float32")
    X[:5] += 6
    if_result = run_isolation_forest(X, contamination=0.05, n_estimators=50, random_state=42)
    lof_result = run_lof(X, n_neighbors=10, contamination=0.05)
    assert if_result.labels.shape == (120,)
    assert lof_result.labels.shape == (120,)
    assert np.isfinite(if_result.scores).all()
    assert np.isfinite(lof_result.scores).all()
