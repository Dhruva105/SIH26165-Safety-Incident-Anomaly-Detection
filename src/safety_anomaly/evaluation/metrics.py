"""Evaluation measures for label-free anomaly detector comparison."""
from __future__ import annotations
import numpy as np
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
