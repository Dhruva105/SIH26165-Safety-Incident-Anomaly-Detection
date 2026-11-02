"""End-to-end pipeline orchestration with bounded LOF execution."""
from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, timezone
import pandas as pd
import numpy as np

from safety_anomaly.config import load_config, resolve_project_path
from safety_anomaly.data.io import load_incidents
from safety_anomaly.data.audit import audit_frame
from safety_anomaly.data.clean import prepare_records
from safety_anomaly.features.build import build_features
from safety_anomaly.models.experiments import run_experiment_grid
from safety_anomaly.evaluation.metrics import agreement_metrics
from safety_anomaly.evaluation.review import create_blinded_review_sheet, public_anomaly_export
from safety_anomaly.visualization.plots import create_pca_projection, save_pca_figure


def deterministic_sample(frame: pd.DataFrame, size: int | None, random_state: int) -> pd.DataFrame:
    if size is None or size >= len(frame):
        return frame.copy().reset_index(drop=True)
    if size < 100:
        raise ValueError("For analysis, sample_size must be at least 100 (use >= 20 only in unit tests).")
    return frame.sample(n=size, random_state=random_state).sort_index().reset_index(drop=True)


def _write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def run_pipeline(dataset_path: str | Path | None = None, *, config_path: str | Path = "configs/default.yaml",
                 sample_size: int | None = None, quick: bool = False, representation: str | None = None,
                 output_dir: str | Path | None = None) -> dict:
    config = load_config(resolve_project_path(config_path))
    data_path = resolve_project_path(dataset_path or config["project"]["dataset_path"])
    output_root = resolve_project_path(output_dir or config["project"]["output_dir"])
    public_dir = output_root / "public"
    private_dir = output_root / "private"
    model_dir = output_root / "models"
    for directory in (public_dir, private_dir, model_dir):
        directory.mkdir(parents=True, exist_ok=True)

    raw = load_incidents(data_path)
    audit = audit_frame(raw)
    _write_json(public_dir / "dataset_summary.json", {
        "rows": audit["rows"], "columns": audit["columns"],
        "event_date_min": audit["event_date_min"], "event_date_max": audit["event_date_max"],
        "exact_duplicate_rows": audit["exact_duplicate_rows"], "unique_upa": audit["unique_upa"],
    })
    pd.DataFrame(audit["missingness"]).to_csv(public_dir / "missingness.csv", index=False)
    cleaned = prepare_records(raw)
    seed = int(config["project"].get("random_state", 42))
    exp_cfg = config.get("experiments", {})
    size = sample_size if sample_size is not None else int(exp_cfg.get("sample_size", 5000))
    sample = deterministic_sample(cleaned, size, seed)
    rep = representation or ("structured_text" if config["features"].get("include_text_by_default", True) else "structured")
    feature_cfg = config.get("features", {})
    feature_result = build_features(
        sample,
        representation=rep,
        random_state=seed,
        svd_components=int(feature_cfg.get("svd_components", 24)),
        min_category_frequency=int(feature_cfg.get("min_category_frequency", 15)),
        max_text_features=int(feature_cfg.get("max_text_features", 2500)),
        text_min_df=int(feature_cfg.get("text_min_df", 3)),
    )

    summary, predictions = run_experiment_grid(
        feature_result.X,
        random_state=seed,
        quick=quick,
        lof_max_rows=int(exp_cfg.get("lof_max_rows", 10000)),
        iforest_estimators=tuple(exp_cfg.get("isolation_forest", {}).get("n_estimators", [100, 200, 300])),
        iforest_contamination=tuple(exp_cfg.get("isolation_forest", {}).get("contamination", [0.01, 0.03, 0.05])),
        lof_neighbors=tuple(exp_cfg.get("lof", {}).get("n_neighbors", [15, 25, 35])),
        lof_contamination=tuple(exp_cfg.get("lof", {}).get("contamination", [0.01, 0.03, 0.05])),
        lof_metrics=tuple(exp_cfg.get("lof", {}).get("metric", ["euclidean", "manhattan"])),
    )
    summary.to_csv(public_dir / "experiment_summary.csv", index=False)

    # Select a documented reference pair, not a claimed winner.
    if_key = next((k for k in predictions if k.startswith("iforest_n100_c0.03")), None)
    lof_key = next((k for k in predictions if k.startswith("lof_k15_c0.03")), None)
    if if_key is None or lof_key is None:
        raise RuntimeError("Reference IF/LOF configurations were not produced.")
    if_pred, lof_pred = predictions[if_key], predictions[lof_key]
    metrics = agreement_metrics(if_pred["labels"], lof_pred["labels"], if_pred["scores"], lof_pred["scores"])
    _write_json(public_dir / "agreement_metrics.json", metrics)

    coords, explained = create_pca_projection(feature_result.X, n_components=3, random_state=seed)
    coords.insert(0, "record_number", np.arange(1, len(coords) + 1))
    coords.to_csv(public_dir / "pca_coordinates.csv", index=False)
    _write_json(public_dir / "pca_metadata.json", {"explained_variance_ratio": explained.tolist(), "representation": rep})
    save_pca_figure(coords, if_pred["labels"], public_dir / "pca_iforest.png", "PCA projection: Isolation Forest")
    save_pca_figure(coords, lof_pred["labels"], public_dir / "pca_lof.png", "PCA projection: Local Outlier Factor")

    # Public export omits direct identifiers, employer, location, and raw narrative.
    public_records = public_anomaly_export(sample, if_pred["labels"], if_pred["scores"])
    public_records.to_csv(public_dir / "anomaly_explorer.csv", index=False)
    # Blinded review worksheet is local/private because it contains narrative excerpts.
    review = create_blinded_review_sheet(
        sample, if_pred["labels"], lof_pred["labels"],
        sample_per_group=int(exp_cfg.get("review_size_per_group", 25)), random_state=seed,
    )
    review.to_csv(private_dir / "blinded_manual_review.csv", index=False)

    run_metadata = {
        "status": "completed",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_path": str(data_path),
        "dataset_rows": int(len(raw)),
        "model_sample_rows": int(len(sample)),
        "random_state": seed,
        "quick_grid": bool(quick),
        "feature_dimensions": int(feature_result.X.shape[1]),
        "representation": rep,
        "experiment_count": int(len(summary)),
        "reference_iforest": if_key,
        "reference_lof": lof_key,
        "agreement": metrics,
        "note": "Agreement measures compare two unsupervised partitions; they are not anomaly accuracy metrics.",
    }
    _write_json(public_dir / "run_metadata.json", run_metadata)
    return run_metadata
