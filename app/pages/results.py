import streamlit as st
import pandas as pd
import plotly.express as px
from utils import PUBLIC, read_json_if_exists, read_csv_if_exists, require_results

st.markdown('<div class="eyebrow">PROJECT EVIDENCE / EVALUATION</div>', unsafe_allow_html=True)
st.title("Experimental evidence")
st.markdown('<div class="page-deck">The reported figures are descriptive and unsupervised. They measure model agreement and internal cluster structure, not the ability to predict injury outcomes.</div>', unsafe_allow_html=True)

meta = read_json_if_exists(PUBLIC / "run_metadata.json") or {}
summary = read_csv_if_exists(PUBLIC / "experiment_summary.csv")
metrics = read_json_if_exists(PUBLIC / "agreement_metrics.json") or {}
parameter_pairs = read_csv_if_exists(PUBLIC / "parameter_agreement.csv")
outcome_proxies = read_csv_if_exists(PUBLIC / "outcome_proxy_comparison.csv")
cluster_eval = read_csv_if_exists(PUBLIC / "cluster_evaluation.csv")
cluster_profiles = read_csv_if_exists(PUBLIC / "cluster_profiles.csv")

if not require_results():
    st.stop()

st.markdown("### Isolation Forest and LOF agreement")
a, b, c = st.columns(3)
a.metric("Jaccard", f"{metrics.get('jaccard_anomaly_sets', float('nan')):.3f}" if metrics.get("jaccard_anomaly_sets") is not None else "—")
b.metric("Adjusted Rand", f"{metrics.get('adjusted_rand_index', float('nan')):.3f}" if metrics.get("adjusted_rand_index") is not None else "—")
c.metric("Spearman score correlation", f"{metrics.get('spearman_score_correlation', float('nan')):.3f}" if metrics.get("spearman_score_correlation") is not None else "—")
st.caption(
    f"Selected configurations flagged {metrics.get('anomalies_a', '—')} records each; "
    f"{metrics.get('intersection', '—')} flags overlapped in a {meta.get('model_sample_rows', '—')}-record sample. "
    "Agreement describes consistency, not correctness."
)
if parameter_pairs is not None:
    st.markdown("### Agreement across parameter settings")
    st.dataframe(parameter_pairs, use_container_width=True, hide_index=True)
    st.caption("All pairwise configurations are compared. Within-model and cross-model differences show parameter sensitivity and detector disagreement.")
if outcome_proxies is not None:
    st.markdown("### Post-hoc check against held-out report outcomes")
    st.dataframe(outcome_proxies, use_container_width=True, hide_index=True)
    st.caption("Hospitalized, Amputation and Loss of Eye are excluded from model inputs. These indicators are descriptors of recorded outcomes, not independently adjudicated anomaly labels; they cannot be used to calculate accuracy or false-positive rates.")
if summary is not None:
    st.markdown("### IF/LOF parameter runs")
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(summary, x="experiment_id", y="anomaly_percent", color="model", title="Flagged observations by configuration"), use_container_width=True)

st.markdown("### K-Means cluster-count evaluation")
if cluster_eval is not None:
    st.dataframe(cluster_eval, use_container_width=True, hide_index=True)
    st.caption("k=8 is used as an exploratory compromise between finer separation and across-seed stability. Cluster assignments remain initialization-sensitive and internal metrics are not ground-truth validation.")
if cluster_profiles is not None:
    st.markdown("### Descriptors of the selected k=8 groups")
    st.dataframe(cluster_profiles, use_container_width=True, hide_index=True)

st.markdown("### PCA projections")
for filename, title in [("pca_iforest.png", "Isolation Forest projection"), ("pca_lof.png", "Local Outlier Factor projection")]:
    path = PUBLIC / filename
    if path.exists():
        st.image(str(path), caption=title, use_container_width=True)
st.caption(f"Original IF/LOF experiment: {meta.get('model_sample_rows', 'unknown')} rows · {meta.get('feature_dimensions', 'unknown')} dimensions · {meta.get('experiment_count', 'unknown')} configurations · {meta.get('generated_at_utc', 'date not recorded')}.")
