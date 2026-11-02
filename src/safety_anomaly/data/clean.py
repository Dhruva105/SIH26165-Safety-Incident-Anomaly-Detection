"""Conservative data cleaning. Raw source values remain untouched on disk."""
from __future__ import annotations

import pandas as pd


def normalize_text_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return a copy with whitespace normalized and blank strings set to NA."""
    output = frame.copy()
    for column in columns:
        if column in output.columns:
            values = output[column].astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
            output[column] = values.mask(values.eq(""), pd.NA)
    return output


def prepare_records(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize selected text fields and parse dates without dropping records."""
    columns = [
        "Primary NAICS", "Final Narrative", "NatureTitle", "Part of Body Title",
        "EventTitle", "SourceTitle", "Secondary Source Title",
    ]
    output = normalize_text_columns(frame, columns)
    if "EventDate" in output:
        output["EventDate"] = pd.to_datetime(output["EventDate"], errors="coerce")
    return output
