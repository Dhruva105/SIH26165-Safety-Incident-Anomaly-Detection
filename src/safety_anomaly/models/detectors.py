"""Isolation Forest and Local Outlier Factor wrappers."""
from __future__ import annotations

from dataclasses import dataclass
import time
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


@dataclass
class DetectionResult:
    model_name: str
    labels: np.ndarray  # -1 means anomaly, +1 means inlier (sklearn convention)
    scores: np.ndarray  # Larger means more anomalous for both wrappers.
    runtime_seconds: float
    parameters: dict


def run_isolation_forest(
    X: np.ndarray,
    *,
    contamination: float = 0.03,
    n_estimators: int = 200,
    max_samples: str | int | float = "auto",
    random_state: int = 42,
) -> DetectionResult:
    if not 0 < float(contamination) <= 0.5:
        raise ValueError("contamination must be in (0, 0.5]")
    started = time.perf_counter()
    model = IsolationForest(
        n_estimators=int(n_estimators), contamination=float(contamination),
        max_samples=max_samples, random_state=int(random_state), n_jobs=-1,
    )
    labels = model.fit_predict(X)
    scores = -model.score_samples(X)
    return DetectionResult(
        "Isolation Forest", labels.astype(int), scores.astype(float),
        time.perf_counter() - started,
        {"contamination": contamination, "n_estimators": n_estimators,
         "max_samples": max_samples, "random_state": random_state},
    )


def run_lof(
    X: np.ndarray,
    *,
    n_neighbors: int = 20,
    contamination: float = 0.03,
    metric: str = "euclidean",
) -> DetectionResult:
    if len(X) < 3:
        raise ValueError("LOF requires at least three observations.")
    if n_neighbors < 2:
        raise ValueError("n_neighbors must be at least 2.")
    if n_neighbors >= len(X):
        n_neighbors = len(X) - 1
    if not 0 < float(contamination) <= 0.5:
        raise ValueError("contamination must be in (0, 0.5]")
    started = time.perf_counter()
    model = LocalOutlierFactor(
        n_neighbors=int(n_neighbors), contamination=float(contamination),
        metric=metric, novelty=False, n_jobs=-1,
    )
    labels = model.fit_predict(X)
    scores = -model.negative_outlier_factor_
    return DetectionResult(
        "Local Outlier Factor", labels.astype(int), scores.astype(float),
        time.perf_counter() - started,
        {"n_neighbors": n_neighbors, "contamination": contamination,
         "metric": metric, "novelty": False},
    )
