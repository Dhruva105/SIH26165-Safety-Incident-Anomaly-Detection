"""Evaluate K-Means pattern groupings on a deterministic OSHA report sample.

This is descriptive, unlabeled clustering evaluation. The metrics do not
measure hazard prediction or anomaly-detection accuracy.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

from safety_anomaly.features.build import build_features

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/raw/January2015toNovember2025.csv"


def top_value(values: pd.Series) -> str:
    cleaned = values.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.isin(["", "Unknown", "nan", "None"])]
    counts = cleaned.value_counts()
    return str(counts.index[0]) if not counts.empty else "Not recorded"


def run(input_path: Path, sample_size: int, output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(input_path, low_memory=False)
    required = [
        "EventDate", "Primary NAICS", "EventTitle", "SourceTitle",
        "Secondary Source Title", "Final Narrative", "NatureTitle", "Part of Body Title",
    ]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
    frame = frame[required].copy()
    frame["EventDate"] = pd.to_datetime(frame["EventDate"], errors="coerce")
    frame = frame.dropna(subset=["EventDate", "EventTitle"]).reset_index(drop=True)
    if len(frame) > sample_size:
        frame = frame.sample(n=sample_size, random_state=42).reset_index(drop=True)
    features = build_features(
        frame, representation="structured_text", random_state=42,
        svd_components=24, min_category_frequency=15,
        max_text_features=2500, text_min_df=3,
    )
    rows: list[dict] = []
    final_labels: dict[int, list[int]] = {}
    seeds = (13, 42, 77)
    for k in (4, 6, 8, 10):
        labels_by_seed: dict[int, list[int]] = {}
        for seed in seeds:
            model = KMeans(n_clusters=k, random_state=seed, n_init=10, max_iter=300)
            labels_by_seed[seed] = model.fit_predict(features.X).tolist()
        labels = labels_by_seed[42]
        ari_pairs = [
            adjusted_rand_score(labels_by_seed[13], labels_by_seed[42]),
            adjusted_rand_score(labels_by_seed[13], labels_by_seed[77]),
            adjusted_rand_score(labels_by_seed[42], labels_by_seed[77]),
        ]
        rows.append({
            "k": k,
            "sample_size": len(frame),
            "feature_dimensions": int(features.X.shape[1]),
            "silhouette_sample_2000": float(silhouette_score(
                features.X, labels, sample_size=min(2000, len(frame)), random_state=42
            )),
            "davies_bouldin": float(davies_bouldin_score(features.X, labels)),
            "calinski_harabasz": float(calinski_harabasz_score(features.X, labels)),
            "mean_pairwise_ari_across_seeds_13_42_77": float(sum(ari_pairs) / len(ari_pairs)),
            "cluster_sizes": ";".join(str(value) for value in sorted(pd.Series(labels).value_counts().tolist())),
        })
        final_labels[k] = labels

    selected_k = 8  # documented exploratory trade-off: inspectable themes without over-fragmenting
    labels = final_labels[selected_k]
    prof = frame.copy()
    prof["cluster_id"] = labels
    profile_rows = []
    for cluster_id in range(selected_k):
        group = prof.loc[prof["cluster_id"] == cluster_id]
        profile_rows.append({
            "cluster_id": cluster_id + 1,
            "records": len(group),
            "most_common_event": top_value(group["EventTitle"]),
            "most_common_source": top_value(group["SourceTitle"]),
            "most_common_injury": top_value(group["NatureTitle"]),
            "most_common_body_part": top_value(group["Part of Body Title"]),
        })

    evaluation = pd.DataFrame(rows)
    profiles = pd.DataFrame(profile_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    evaluation.to_csv(output_dir / "cluster_evaluation.csv", index=False)
    profiles.to_csv(output_dir / "cluster_profiles.csv", index=False)
    return evaluation, profiles


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--sample-size", type=int, default=5000)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "artifacts/public")
    args = parser.parse_args()
    evaluation, profiles = run(args.input, args.sample_size, args.output_dir)
    print("Cluster evaluation:")
    print(evaluation.to_string(index=False))
    print("\nSelected k=8 profiles:")
    print(profiles.to_string(index=False))


if __name__ == "__main__":
    main()
