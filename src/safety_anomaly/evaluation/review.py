"""Generate a blinded, anonymized manual-review worksheet."""
from __future__ import annotations
import hashlib
import numpy as np
import pandas as pd


def create_blinded_review_sheet(frame: pd.DataFrame, labels_a, labels_b, *,
                                sample_per_group: int = 25, random_state: int = 42) -> pd.DataFrame:
    if len(frame) != len(labels_a) or len(frame) != len(labels_b):
        raise ValueError("frame and prediction arrays must have matching lengths")
    a, b = np.asarray(labels_a) == -1, np.asarray(labels_b) == -1
    groups = {
        "both_flagged": np.flatnonzero(a & b),
        "iforest_only": np.flatnonzero(a & ~b),
        "lof_only": np.flatnonzero(~a & b),
        "neither_flagged": np.flatnonzero(~a & ~b),
    }
    rng = np.random.default_rng(random_state)
    selected = []
    group_codes = []
    for name, positions in groups.items():
        if not len(positions):
            continue
        chosen = rng.choice(positions, size=min(sample_per_group, len(positions)), replace=False)
        selected.extend(chosen.tolist())
        group_codes.extend([name] * len(chosen))
    order = rng.permutation(len(selected))
    selected = np.asarray(selected)[order]
    # Group membership and model information are intentionally not exported.
    output_columns = [c for c in ["EventDate", "EventTitle", "SourceTitle", "NatureTitle", "Part of Body Title"] if c in frame]
    descriptions = frame.get("Final Narrative", pd.Series("", index=frame.index)).fillna("").astype(str)
    records = frame.iloc[selected][output_columns].copy().reset_index(drop=True)
    records.insert(0, "review_case", [f"CASE-{i+1:04d}" for i in range(len(records))])
    records["narrative_excerpt"] = descriptions.iloc[selected].str.slice(0, 700).to_numpy()
    records["review_category"] = ""
    records["review_reason"] = ""
    records["reviewer_id"] = ""
    records["review_date"] = ""
    return records


def public_anomaly_export(frame: pd.DataFrame, labels, scores) -> pd.DataFrame:
    """Create a record-level dashboard export without direct identifiers/text.

    Only broad event categories, date components and normalized score are kept.
    No UPA, employer, location, address, ZIP or narrative is exported.
    """
    labels = np.asarray(labels)
    scores = np.asarray(scores, dtype=float)
    safe_cols = [c for c in ["EventDate", "EventTitle", "NatureTitle", "Part of Body Title", "SourceTitle"] if c in frame]
    result = frame[safe_cols].copy().reset_index(drop=True)
    result.insert(0, "record_number", np.arange(1, len(result) + 1))
    result["model_label"] = np.where(labels == -1, "Anomaly", "Inlier")
    low, high = np.nanmin(scores), np.nanmax(scores)
    result["anomaly_score_normalized"] = (scores - low) / (high - low) if high > low else 0.0
    if "EventDate" in result:
        result["EventDate"] = pd.to_datetime(result["EventDate"], errors="coerce").dt.strftime("%Y-%m-%d")
    return result
