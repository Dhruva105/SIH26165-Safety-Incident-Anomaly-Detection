from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "artifacts" / "public"

@st.cache_data(show_spinner=False)
def read_csv_if_exists(path: str):
    file = Path(path)
    if not file.exists():
        return None
    return pd.read_csv(file)

@st.cache_data(show_spinner=False)
def read_json_if_exists(path: str):
    file = Path(path)
    if not file.exists():
        return None
    return json.loads(file.read_text(encoding="utf-8"))

def require_results():
    summary = read_json_if_exists(PUBLIC / "run_metadata.json")
    if summary is None:
        st.warning("No experiment results are available yet. Run the pipeline using the command in the README, then refresh this page.")
        st.code("python -m safety_anomaly.cli run --quick --sample-size 1000")
        return False
    return True
