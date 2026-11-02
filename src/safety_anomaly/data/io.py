"""Input/output helpers for the OSHA incident CSV."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "UPA", "EventDate", "Primary NAICS", "Final Narrative", "NatureTitle",
    "Part of Body Title", "EventTitle", "SourceTitle", "Secondary Source Title",
}


def load_incidents(path: str | Path, *, usecols: list[str] | None = None) -> pd.DataFrame:
    """Load incident records and validate the minimum schema.

    The reader uses UTF-8 BOM support and disables chunk type inference warnings.
    Original data are returned without in-place modification.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path.resolve()}")
    frame = pd.read_csv(csv_path, encoding="utf-8-sig", low_memory=False, usecols=usecols)
    if usecols is None:
        missing = REQUIRED_COLUMNS.difference(frame.columns)
        if missing:
            raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return frame


def count_csv_rows(path: str | Path, chunksize: int = 100_000) -> int:
    """Count data rows without loading the complete CSV into memory."""
    total = 0
    for chunk in pd.read_csv(path, encoding="utf-8-sig", low_memory=False, chunksize=chunksize):
        total += len(chunk)
    return total
