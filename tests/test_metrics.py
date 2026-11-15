import numpy as np
import pandas as pd
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


def test_pairwise_agreement_table_and_outcome_proxy_table():
    from types import SimpleNamespace
    from safety_anomaly.evaluation.metrics import pairwise_agreement_table, outcome_proxy_table

    predictions = {
        "if_a": {"labels": np.array([-1, 1, 1, -1]), "scores": np.array([4., 1., 2., 3.]),
                 "result": SimpleNamespace(model_name="Isolation Forest")},
        "lof_a": {"labels": np.array([-1, 1, -1, 1]), "scores": np.array([3., 1., 4., 2.]),
                  "result": SimpleNamespace(model_name="Local Outlier Factor")},
    }
    pairs = pairwise_agreement_table(predictions)
    assert len(pairs) == 1
    assert pairs.loc[0, "jaccard_anomaly_sets"] == 1 / 3

    frame = pd.DataFrame({"Hospitalized": [1, 0, 1, 0], "Amputation": [0, 0, 1, 0],
                          "Loss of Eye": [0, 0, 0, 0]})
    proxies = outcome_proxy_table(frame, predictions, ["if_a"])
    hosp = proxies[proxies["outcome_field"] == "Hospitalized"].set_index("indicator_status")
    assert hosp.loc["present", "records"] == 2
    assert hosp.loc["absent", "records"] == 2
