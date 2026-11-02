"""Dataset quality summaries and audit exports."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from .io import load_incidents


def audit_frame(frame: pd.DataFrame) -> dict:
    """Return a JSON-serializable, non-destructive dataset audit."""
    date_values = pd.to_datetime(frame.get("EventDate"), errors="coerce") if "EventDate" in frame else pd.Series(dtype="datetime64[ns]")
    missing = frame.isna().sum().sort_values(ascending=False)
    missing_table = pd.DataFrame({
        "column": missing.index.astype(str),
        "missing_count": missing.values.astype(int),
        "missing_percent": (missing.values / max(len(frame), 1) * 100).round(3),
    })
    duplicated_ids = int(frame["ID"].duplicated(keep=False).sum()) if "ID" in frame else None
    unique_upa = int(frame["UPA"].nunique(dropna=True)) if "UPA" in frame else None
    narrative = frame.get("Final Narrative", pd.Series(dtype="string")).fillna("").astype(str)
    result = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "column_names": [str(c) for c in frame.columns],
        "exact_duplicate_rows": int(frame.duplicated().sum()),
        "unique_upa": unique_upa,
        "missing_upa": int(frame["UPA"].isna().sum()) if "UPA" in frame else None,
        "duplicated_id_rows_including_first": duplicated_ids,
        "id_distinct_values_among_repeated": int(frame.loc[frame["ID"].duplicated(keep=False), "ID"].nunique()) if "ID" in frame else None,
        "event_date_min": str(date_values.min().date()) if len(date_values) and date_values.notna().any() else None,
        "event_date_max": str(date_values.max().date()) if len(date_values) and date_values.notna().any() else None,
        "invalid_event_dates": int(date_values.isna().sum()) if len(date_values) else None,
        "empty_narratives": int(narrative.str.strip().eq("").sum()),
        "dtypes": {str(k): str(v) for k, v in frame.dtypes.items()},
    }
    result["missingness"] = missing_table.to_dict(orient="records")
    return result


def run_audit(csv_path: str | Path, output_dir: str | Path) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    frame = load_incidents(csv_path)
    audit = audit_frame(frame)
    pd.DataFrame(audit["missingness"]).to_csv(output / "missingness.csv", index=False)
    pd.DataFrame({"column": list(audit["dtypes"]), "dtype": list(audit["dtypes"].values())}).to_csv(output / "data_dictionary_seed.csv", index=False)
    import json
    (output / "audit_summary.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return audit
