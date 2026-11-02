import numpy as np
import pytest
from safety_anomaly.evaluation.metrics import agreement_metrics, jaccard_anomaly_sets


def test_jaccard_and_agreement_metrics():
    a = np.array([-1, -1, 1, 1])
    b = np.array([-1, 1, -1, 1])
    assert jaccard_anomaly_sets(a, b) == pytest.approx(1 / 3)
    result = agreement_metrics(a, b, [4, 3, 2, 1], [4, 2, 3, 1])
    assert result["intersection"] == 1
    assert -1 <= result["adjusted_rand_index"] <= 1
    assert result["spearman_score_correlation"] == pytest.approx(0.8)


def test_mismatched_lengths_raise():
    with pytest.raises(ValueError):
        agreement_metrics([-1, 1], [-1])
