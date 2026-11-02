import streamlit as st
import plotly.express as px
from utils import PUBLIC, read_json_if_exists, read_csv_if_exists, require_results

st.title("Experimental Results")
if not require_results():
    st.stop()
meta = read_json_if_exists(PUBLIC / "run_metadata.json") or {}
summary = read_csv_if_exists(PUBLIC / "experiment_summary.csv")
metrics = read_json_if_exists(PUBLIC / "agreement_metrics.json") or {}
coords = read_csv_if_exists(PUBLIC / "pca_coordinates.csv")
for name, value in [("Jaccard similarity", metrics.get("jaccard_anomaly_sets")), ("Adjusted Rand Index", metrics.get("adjusted_rand_index")), ("Spearman score correlation", metrics.get("spearman_score_correlation"))]:
    pass
c1, c2, c3 = st.columns(3)
c1.metric("Jaccard similarity", f"{metrics.get('jaccard_anomaly_sets', float('nan')):.3f}" if metrics.get('jaccard_anomaly_sets') is not None else "—")
c2.metric("Adjusted Rand Index", f"{metrics.get('adjusted_rand_index', float('nan')):.3f}" if metrics.get('adjusted_rand_index') is not None else "—")
c3.metric("Spearman correlation", f"{metrics.get('spearman_score_correlation', float('nan')):.3f}" if metrics.get('spearman_score_correlation') is not None else "—")
st.caption("These values measure agreement between unsupervised model outputs. They do not measure detection accuracy.")
if summary is not None:
    st.subheader("Hyperparameter experiment summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(summary, x="experiment_id", y="anomaly_percent", color="model", title="Flagged observations by configuration"), use_container_width=True)
if coords is not None:
    st.subheader("PCA projections")
    for filename, title in [("pca_iforest.png", "Isolation Forest"), ("pca_lof.png", "Local Outlier Factor")]:
        path = PUBLIC / filename
        if path.exists():
            st.image(str(path), caption=title, use_container_width=True)
st.caption(f"Representation: {meta.get('representation', 'unknown')} · Model sample: {meta.get('model_sample_rows', 'unknown')}")
