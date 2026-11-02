"""Bounded, reproducible experiment grids."""
from __future__ import annotations

import itertools
import pandas as pd
import numpy as np
from .detectors import run_isolation_forest, run_lof


def run_experiment_grid(X: np.ndarray, *, random_state: int = 42, quick: bool = False,
                        lof_max_rows: int = 10000,
                        iforest_estimators: tuple[int, ...] = (100, 200, 300),
                        iforest_contamination: tuple[float, ...] = (0.01, 0.03, 0.05),
                        lof_neighbors: tuple[int, ...] = (15, 25, 35),
                        lof_contamination: tuple[float, ...] = (0.01, 0.03, 0.05),
                        lof_metrics: tuple[str, ...] = ("euclidean", "manhattan")) -> tuple[pd.DataFrame, dict[str, dict]]:
    """Run small transparent IF/LOF grids and return summary plus best results.

    Best here means the first configuration under a predeclared operational
    default, not an objectively superior detector. No ground-truth labels exist.
    """
    records = []
    predictions = {}
    if_configs = [(100, 0.01), (100, 0.03), (200, 0.03)] if quick else list(
        itertools.product(iforest_estimators, iforest_contamination)
    )
    for n_estimators, contamination in if_configs:
        result = run_isolation_forest(
            X, contamination=contamination, n_estimators=n_estimators,
            random_state=random_state,
        )
        key = f"iforest_n{n_estimators}_c{contamination:.2f}"
        predictions[key] = {"labels": result.labels, "scores": result.scores, "result": result}
        records.append(_result_record(key, result))

    if len(X) > lof_max_rows:
        raise ValueError(
            f"LOF sample has {len(X):,} rows, exceeding configured safety limit "
            f"{lof_max_rows:,}. Reduce --sample-size or explicitly raise the limit after benchmarking."
        )
    lof_configs = [(15, 0.01, "euclidean"), (15, 0.03, "euclidean"),
                   (25, 0.03, "euclidean")] if quick else list(
        itertools.product(lof_neighbors, lof_contamination, lof_metrics)
    )
    for neighbors, contamination, metric in lof_configs:
        result = run_lof(X, n_neighbors=neighbors, contamination=contamination, metric=metric)
        key = f"lof_k{neighbors}_c{contamination:.2f}_{metric}"
        predictions[key] = {"labels": result.labels, "scores": result.scores, "result": result}
        records.append(_result_record(key, result))

    return pd.DataFrame(records), predictions


def _result_record(key: str, result) -> dict:
    n = len(result.labels)
    return {
        "experiment_id": key,
        "model": result.model_name,
        "n_observations": n,
        "n_anomalies": int((result.labels == -1).sum()),
        "anomaly_percent": float((result.labels == -1).mean() * 100),
        "runtime_seconds": round(float(result.runtime_seconds), 4),
        "parameters": str(result.parameters),
    }
