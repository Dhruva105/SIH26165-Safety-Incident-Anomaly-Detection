"""Operational incident screening and review support.

The detector provides an exploratory comparison against historical patterns. It
is not a validated safety-risk model, incident forecast, compliance assessment,
or substitute for qualified safety review.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import NearestNeighbors

from safety_anomaly.features.build import FeatureResult, build_features, transform_features

MODEL_VERSION = "1.2.0"
DEFAULT_CONTAMINATION = 0.03
DEFAULT_CLUSTER_COUNT = 8


@dataclass
class Assessment:
    anomaly_score: float
    reference_percentile: float
    flagged_for_review: bool
    reference_threshold: float
    similar_cases: list[dict[str, Any]]
    signal_label: str
    limitations: str
    pattern_group: str
    cluster_size: int
    pattern_summary: dict[str, str]


class IncidentReviewEngine:
    """Fit and apply a transparent unsupervised review model."""

    def __init__(self, features: FeatureResult, detector: IsolationForest,
                 neighbors: NearestNeighbors, training_scores: np.ndarray,
                 reference_rows: pd.DataFrame, clusterer: KMeans,
                 cluster_assignments: np.ndarray, cluster_profiles: dict[int, dict[str, Any]],
                 contamination: float = DEFAULT_CONTAMINATION):
        self.features = features
        self.detector = detector
        self.neighbors = neighbors
        self.training_scores = np.asarray(training_scores, dtype=float)
        self.reference_rows = reference_rows.reset_index(drop=True)
        self.clusterer = clusterer
        self.cluster_assignments = np.asarray(cluster_assignments, dtype=int)
        self.cluster_profiles = cluster_profiles
        self.contamination = float(contamination)
        self.threshold = float(np.quantile(self.training_scores, 1 - self.contamination))
        self.model_version = MODEL_VERSION

    @classmethod
    def fit(cls, source: pd.DataFrame, *, sample_size: int = 5000,
            random_state: int = 42, contamination: float = DEFAULT_CONTAMINATION,
            n_estimators: int = 250, n_clusters: int = DEFAULT_CLUSTER_COUNT) -> "IncidentReviewEngine":
        required = ["EventDate", "Primary NAICS", "EventTitle", "SourceTitle",
                    "Secondary Source Title", "Final Narrative"]
        missing = [col for col in required if col not in source.columns]
        if missing:
            raise ValueError(f"Historical file is missing required columns: {', '.join(missing)}")
        if not 0 < contamination <= 0.5:
            raise ValueError("contamination must be between 0 and 0.5")

        clean = source[required + [c for c in ("NatureTitle", "Part of Body Title") if c in source]].copy()
        clean["EventDate"] = pd.to_datetime(clean["EventDate"], errors="coerce")
        clean = clean.dropna(subset=["EventDate", "EventTitle"]).reset_index(drop=True)
        if len(clean) < 100:
            raise ValueError("At least 100 valid historical records are required to fit the review model.")
        if len(clean) > sample_size:
            clean = clean.sample(n=sample_size, random_state=random_state).reset_index(drop=True)

        features = build_features(
            clean,
            representation="structured_text",
            random_state=random_state,
            svd_components=24,
            min_category_frequency=15,
            max_text_features=2500,
            text_min_df=3,
        )
        detector = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1,
        ).fit(features.X)
        scores = -detector.score_samples(features.X)
        neighbors = NearestNeighbors(n_neighbors=min(6, len(features.X)), metric="euclidean", n_jobs=-1)
        neighbors.fit(features.X)
        cluster_count = min(max(2, int(n_clusters)), len(features.X) - 1)
        clusterer = KMeans(n_clusters=cluster_count, random_state=random_state, n_init=10, max_iter=300)
        cluster_assignments = clusterer.fit_predict(features.X)

        # Keep only non-identifying comparison attributes; do not retain raw
        # narratives, source IDs, employer names, or precise location fields.
        safe_columns = [c for c in ["EventDate", "Primary NAICS", "EventTitle", "SourceTitle",
                                    "NatureTitle", "Part of Body Title"] if c in clean.columns]
        reference_rows = clean[safe_columns].copy()
        reference_rows["EventDate"] = reference_rows["EventDate"].dt.year.astype("Int64")
        reference_rows["Industry sector"] = reference_rows["Primary NAICS"].astype("string").str[:2]
        reference_rows = reference_rows.drop(columns=["Primary NAICS"], errors="ignore")
        reference_rows["cluster_id"] = cluster_assignments

        def top_category(values: pd.Series) -> str:
            cleaned_values = values.dropna().astype(str).str.strip()
            cleaned_values = cleaned_values[~cleaned_values.isin(["", "Unknown", "nan", "None"])]
            counts = cleaned_values.value_counts()
            return str(counts.index[0]) if not counts.empty else "Not recorded"

        cluster_profiles: dict[int, dict[str, Any]] = {}
        for cluster_id in range(cluster_count):
            group = reference_rows.loc[reference_rows["cluster_id"] == cluster_id]
            cluster_profiles[cluster_id] = {
                "size": int(len(group)),
                "dominant_event": top_category(group.get("EventTitle", pd.Series(dtype=str))),
                "dominant_source": top_category(group.get("SourceTitle", pd.Series(dtype=str))),
                "dominant_injury": top_category(group.get("NatureTitle", pd.Series(dtype=str))),
                "dominant_body_part": top_category(group.get("Part of Body Title", pd.Series(dtype=str))),
            }
        return cls(
            features, detector, neighbors, scores, reference_rows, clusterer,
            cluster_assignments, cluster_profiles, contamination
        )

    def assess(self, incident: dict[str, Any], *, top_k: int = 5) -> Assessment:
        row = pd.DataFrame([{
            "EventDate": pd.to_datetime(incident.get("EventDate"), errors="coerce"),
            "Primary NAICS": str(incident.get("Primary NAICS") or "Unknown"),
            "EventTitle": str(incident.get("EventTitle") or "Unknown"),
            "SourceTitle": str(incident.get("SourceTitle") or "Unknown"),
            "Secondary Source Title": str(incident.get("Secondary Source Title") or "Unknown"),
            "Final Narrative": str(incident.get("Final Narrative") or ""),
            "NatureTitle": str(incident.get("NatureTitle") or "Unknown"),
            "Part of Body Title": str(incident.get("Part of Body Title") or "Unknown"),
        }])
        if pd.isna(row.loc[0, "EventDate"]):
            raise ValueError("A valid incident date is required.")
        vector = transform_features(row, self.features)
        score = float(-self.detector.score_samples(vector)[0])
        percentile = float((self.training_scores <= score).mean() * 100)
        distances, indices = self.neighbors.kneighbors(vector, n_neighbors=min(top_k, len(self.reference_rows)))
        matches: list[dict[str, Any]] = []
        for distance, index in zip(distances[0], indices[0]):
            item = self.reference_rows.iloc[int(index)].to_dict()
            item["similarity_distance"] = float(distance)
            item["EventDate"] = int(item["EventDate"]) if pd.notna(item.get("EventDate")) else None
            matches.append(item)
        flagged = score >= self.threshold
        cluster_id = int(self.clusterer.predict(vector)[0])
        cluster_profile = self.cluster_profiles.get(cluster_id, {})
        return Assessment(
            anomaly_score=score,
            reference_percentile=percentile,
            flagged_for_review=bool(flagged),
            reference_threshold=self.threshold,
            similar_cases=matches,
            signal_label="Unusual relative to the reference sample" if flagged else "Closer to common reference patterns",
            limitations=(
                "This percentile ranks the submitted record against the fitted reference sample. "
                "It is not a probability of injury, a calibrated risk score, proof of a control failure, "
                "or a measure of legal compliance. The reference data contain reported severe injuries "
                "under federal OSHA jurisdiction only. A qualified safety professional must review the case."
            ),
            pattern_group=f"Pattern group {cluster_id + 1:02d}",
            cluster_size=int(cluster_profile.get("size", 0)),
            pattern_summary={key: str(value) for key, value in cluster_profile.items() if key != "size"},
        )

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, target, compress=3)

    @classmethod
    def load(cls, path: str | Path) -> "IncidentReviewEngine":
        engine = joblib.load(path)
        if not isinstance(engine, cls):
            raise TypeError("The model artifact is not a supported IncidentReviewEngine.")
        return engine


def build_review_prompts(event_title: str, source_title: str, narrative: str) -> list[dict[str, str]]:
    """Return rule-based questions and possible controls to verify, not advice."""
    text = " ".join([event_title or "", source_title or "", narrative or ""]).lower()
    prompts = [
        {"area": "Immediate response", "prompt": "Has the area been made safe, affected work paused where necessary, and any injured person given appropriate emergency response?"},
        {"area": "Sequence of events", "prompt": "Can the task, equipment state, environment, and sequence immediately before the event be reconstructed from evidence?"},
        {"area": "Existing controls", "prompt": "Which controls were expected to prevent exposure, and were they suitable, available, used, and functioning?"},
        {"area": "Contributing conditions", "prompt": "Were workload, supervision, maintenance, training, procedures, communication, or environmental conditions relevant?"},
        {"area": "Corrective action", "prompt": "Does each action have an owner, due date, and a way to verify that it reduces the identified exposure?"},
    ]
    rules = [
        (("fall", "ladder", "roof", "scaffold", "elevated", "height"), "Falls and access", "Check the work surface, edge protection, ladder/scaffold condition, access method, and whether fall protection was suitable for the task."),
        (("caught", "entangled", "crush", "pinch", "machine", "conveyor", "press"), "Machine and caught-in hazards", "Check point-of-operation and moving-part guards, interlocks, safe clearing methods, and hazardous-energy isolation during servicing."),
        (("electr", "shock", "arc flash", "energized", "wire", "power line"), "Electrical exposure", "Verify the energy source, isolation and test-before-touch process, qualified-person involvement, equipment condition, and approach boundaries."),
        (("struck", "vehicle", "forklift", "truck", "backing", "load", "falling object"), "Struck-by and vehicle movement", "Check pedestrian/vehicle separation, travel paths, visibility, reversing controls, load stability, and exclusion zones."),
        (("burn", "fire", "explosion", "weld", "torch", "hot work"), "Fire, heat and hot work", "Check ignition sources, hot-work controls, combustible materials, fire protection, ventilation, and task-appropriate protective equipment."),
        (("chemical", "vapor", "vapour", "gas", "fume", "solvent", "exposure"), "Chemical and airborne exposure", "Check substance identification, current safety data, ventilation, containment, exposure controls, and emergency arrangements."),
    ]
    for keywords, area, prompt in rules:
        if any(word in text for word in keywords):
            prompts.append({"area": area, "prompt": prompt})
    return prompts
