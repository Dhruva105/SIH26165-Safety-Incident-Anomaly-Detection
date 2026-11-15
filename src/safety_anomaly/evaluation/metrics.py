"""Evaluation measures for label-free anomaly detector comparison."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from scipy.stats import spearmanr


def jaccard_anomaly_sets(labels_a, labels_b) -> float:
    a = np.asarray(labels_a) == -1
    b = np.asarray(labels_b) == -1
    union = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / union) if union else 1.0


def agreement_metrics(labels_a, labels_b, scores_a=None, scores_b=None) -> dict:
    a, b = np.asarray(labels_a), np.asarray(labels_b)
    if len(a) != len(b):
        raise ValueError("Prediction arrays must have equal length.")
    result = {
        "jaccard_anomaly_sets": jaccard_anomaly_sets(a, b),
        "adjusted_rand_index": float(adjusted_rand_score(a, b)),
        "anomalies_a": int((a == -1).sum()),
        "anomalies_b": int((b == -1).sum()),
        "intersection": int(np.logical_and(a == -1, b == -1).sum()),
    }
    if scores_a is not None and scores_b is not None:
        corr = spearmanr(np.asarray(scores_a), np.asarray(scores_b), nan_policy="omit").statistic
        result["spearman_score_correlation"] = float(corr) if np.isfinite(corr) else None
    return result


def pairwise_agreement_table(predictions: dict) -> pd.DataFrame:
    """Compare anomaly-set and score agreement for every pair of configurations."""
    rows = []
    keys = list(predictions)
    for i, key_a in enumerate(keys):
        a = predictions[key_a]
        for key_b in keys[i + 1:]:
            b = predictions[key_b]
            metrics = agreement_metrics(a["labels"], b["labels"], a["scores"], b["scores"])
            rows.append({
                "configuration_a": key_a,
                "model_a": a["result"].model_name,
                "configuration_b": key_b,
                "model_b": b["result"].model_name,
                **metrics,
            })
    return pd.DataFrame(rows)


def outcome_proxy_table(frame: pd.DataFrame, predictions: dict, config_keys: list[str]) -> pd.DataFrame:
    """Describe detector flags by held-out OSHA injury-outcome indicators.

    Outcome fields are intentionally not inputs to feature construction. This is
    a descriptive association analysis, not anomaly ground truth or accuracy.
    """
    outcomes = {
        "Hospitalized": "reported_hospitalization_present",
        "Amputation": "reported_amputation_present",
        "Loss of Eye": "reported_eye_loss_present",
    }
    rows = []
    for key in config_keys:
        if key not in predictions:
            continue
        flagged = np.asarray(predictions[key]["labels"]) == -1
        for column, label in outcomes.items():
            if column not in frame:
                continue
            values = pd.to_numeric(frame[column], errors="coerce")
            valid = values.notna().to_numpy()
            present = (values.fillna(0).to_numpy() > 0)
            for status, mask in (("present", valid & present), ("absent", valid & ~present)):
                count = int(mask.sum())
                flagged_count = int((flagged & mask).sum())
                rows.append({
                    "configuration": key,
                    "model": predictions[key]["result"].model_name,
                    "outcome_field": column,
                    "outcome_indicator": label,
                    "indicator_status": status,
                    "records": count,
                    "flagged_records": flagged_count,
                    "flag_rate_percent": round(100 * flagged_count / count, 3) if count else None,
                })
    return pd.DataFrame(rows)
