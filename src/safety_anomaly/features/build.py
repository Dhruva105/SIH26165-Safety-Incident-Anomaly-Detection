"""Build compact numeric representations from structured and narrative features."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_CATEGORICAL = ["Primary NAICS", "EventTitle", "SourceTitle", "Secondary Source Title"]
SUPPLEMENTARY_CATEGORICAL = ["NatureTitle", "Part of Body Title"]
TEXT_COLUMN = "Final Narrative"
DATE_COLUMN = "EventDate"


@dataclass
class FeatureResult:
    """Feature matrix and fitted transformers for one modeling representation."""
    X: np.ndarray
    row_positions: np.ndarray
    feature_names: list[str]
    representation: str
    svd: TruncatedSVD | None
    encoder: OneHotEncoder
    vectorizer: TfidfVectorizer | None


def _clean_category(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
    return values.fillna("Unknown").replace("", "Unknown").astype(str)


def make_date_features(frame: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(frame.get(DATE_COLUMN), errors="coerce")
    valid = dates.notna()
    year = dates.dt.year.astype(float)
    month = dates.dt.month.astype(float)
    weekday = dates.dt.dayofweek.astype(float)
    return pd.DataFrame({
        "year_scaled": ((year.fillna(year.median() if valid.any() else 2015) - 2015) / 10).astype(float),
        "month_sin": np.sin(2 * np.pi * month.fillna(1) / 12),
        "month_cos": np.cos(2 * np.pi * month.fillna(1) / 12),
        "weekday_sin": np.sin(2 * np.pi * weekday.fillna(0) / 7),
        "weekday_cos": np.cos(2 * np.pi * weekday.fillna(0) / 7),
    }, index=frame.index)


def build_features(
    frame: pd.DataFrame,
    *,
    representation: str = "structured_text",
    random_state: int = 42,
    svd_components: int = 24,
    min_category_frequency: int = 15,
    max_text_features: int = 2500,
    text_min_df: int = 3,
    include_injury_categories: bool = False,
) -> FeatureResult:
    """Encode selected fields and reduce to a dense low-dimensional matrix.

    Supported representations:
      - structured: industry, event/source categories and date-derived features.
      - structured_injury: adds injury nature and body-part categories.
      - structured_text: adds TF-IDF representation of incident narratives.
    """
    allowed = {"structured", "structured_injury", "structured_text"}
    if representation not in allowed:
        raise ValueError(f"representation must be one of {sorted(allowed)}")
    if len(frame) < 3:
        raise ValueError("At least three rows are required to build features.")

    categorical = list(BASE_CATEGORICAL)
    add_injury = representation == "structured_injury" or include_injury_categories
    if add_injury:
        categorical.extend(SUPPLEMENTARY_CATEGORICAL)
    for col in categorical:
        if col not in frame:
            frame = frame.copy()
            frame[col] = "Unknown"

    cat_frame = pd.DataFrame({c: _clean_category(frame[c]) for c in categorical}, index=frame.index)
    encoder = OneHotEncoder(
        handle_unknown="ignore",
        min_frequency=min_category_frequency,
        sparse_output=True,
        dtype=np.float32,
    )
    cat_matrix = encoder.fit_transform(cat_frame)

    date_matrix = make_date_features(frame).to_numpy(dtype=np.float32)
    base_matrix = sparse.hstack([cat_matrix, sparse.csr_matrix(date_matrix)], format="csr")

    vectorizer = None
    if representation == "structured_text":
        narrative = frame.get(TEXT_COLUMN, pd.Series("", index=frame.index)).fillna("").astype(str)
        vectorizer = TfidfVectorizer(
            max_features=max_text_features,
            min_df=text_min_df,
            max_df=0.97,
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents="unicode",
            dtype=np.float32,
            token_pattern=r"(?u)\b\w\w+\b",
        )
        try:
            text_matrix = vectorizer.fit_transform(narrative)
            combined = sparse.hstack([base_matrix, text_matrix], format="csr")
        except ValueError:
            # Small samples may not contain enough terms for min_df/max_df.
            vectorizer = None
            combined = base_matrix
    else:
        combined = base_matrix

    max_components = min(svd_components, combined.shape[0] - 1, combined.shape[1] - 1)
    if max_components < 2:
        dense = combined.toarray().astype(np.float32)
        names = [f"feature_{i}" for i in range(dense.shape[1])]
        return FeatureResult(dense, np.arange(len(frame)), names, representation, None, encoder, vectorizer)

    svd = TruncatedSVD(n_components=max_components, random_state=random_state)
    reduced = svd.fit_transform(combined).astype(np.float32)
    scaler = StandardScaler()
    reduced = scaler.fit_transform(reduced).astype(np.float32)
    names = [f"latent_{i + 1}" for i in range(reduced.shape[1])]
    return FeatureResult(reduced, np.arange(len(frame)), names, representation, svd, encoder, vectorizer)
