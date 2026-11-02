import streamlit as st
import plotly.express as px
from utils import PUBLIC, read_csv_if_exists, require_results

st.title("Anomaly Explorer")
st.write("This explorer uses a public-safe export. It does not expose UPA, employer names, street addresses, ZIP codes, exact coordinates or full incident narratives.")
if not require_results():
    st.stop()
data = read_csv_if_exists(PUBLIC / "anomaly_explorer.csv")
if data is None or data.empty:
    st.warning("No public anomaly records are available.")
    st.stop()
labels = sorted(data["model_label"].dropna().unique().tolist())
selected = st.multiselect("Record group", labels, default=labels)
filtered = data[data["model_label"].isin(selected)]
if "EventTitle" in filtered:
    event_options = sorted(filtered["EventTitle"].dropna().unique().tolist())
    events = st.multiselect("Event type", event_options)
    if events:
        filtered = filtered[filtered["EventTitle"].isin(events)]
st.metric("Records in current view", f"{len(filtered):,}")
if not filtered.empty:
    st.plotly_chart(px.histogram(filtered, x="anomaly_score_normalized", color="model_label", nbins=30, title="Normalized anomaly score distribution"), use_container_width=True)
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)
else:
    st.info("No rows match the selected filters.")
