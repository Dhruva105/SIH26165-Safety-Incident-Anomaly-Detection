from pathlib import Path
import streamlit as st
from utils import PUBLIC, read_json_if_exists

st.title("Safety-Incident Anomaly Pattern Detection")
st.subheader("An exploratory comparison of Isolation Forest and Local Outlier Factor")
st.write("This project examines unusual patterns in publicly available occupational severe-injury incident reports. It combines structured incident classifications with textual narratives and compares two unsupervised anomaly-detection approaches.")
st.info("Anomaly detection identifies observations that differ from learned data patterns. It does not predict accidents, establish negligence, or provide a validated workplace-risk score.")
summary = read_json_if_exists(PUBLIC / "dataset_summary.json")
meta = read_json_if_exists(PUBLIC / "run_metadata.json")
if summary:
    a, b, c = st.columns(3)
    a.metric("Dataset records", f"{summary.get('rows', 0):,}")
    b.metric("Dataset columns", summary.get("columns", "—"))
    c.metric("Event-date coverage", f"{summary.get('event_date_min', '—')} to {summary.get('event_date_max', '—')}")
else:
    st.caption("Dataset summary will appear after running the audit or experiment pipeline.")
if meta:
    st.markdown("### Latest experiment run")
    a, b, c = st.columns(3)
    a.metric("Model sample", f"{meta.get('model_sample_rows', 0):,}")
    b.metric("Feature dimensions", meta.get("feature_dimensions", "—"))
    c.metric("Experiments", meta.get("experiment_count", "—"))
    st.caption(f"Representation: {meta.get('representation', 'unknown')}")
else:
    st.markdown("### Project objectives")
    st.markdown("""1. Prepare and audit workplace incident records.
2. Compare Isolation Forest and Local Outlier Factor under controlled parameters.
3. Visualize detections, examine consistency and document limitations.""")
st.markdown("### Analysis workflow")
st.code("Raw incident reports → data audit → feature engineering → Isolation Forest + LOF → PCA → consistency and manual review", language="text")
