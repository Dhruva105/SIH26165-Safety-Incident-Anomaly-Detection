import streamlit as st
from utils import PUBLIC, read_json_if_exists, read_csv_if_exists

st.title("Dataset & Data Quality")
st.write("The project uses OSHA Severe Injury Reports. The dataset represents reported severe injuries in its reporting scope; it is not a census of all workplace incidents or near-misses.")
summary = read_json_if_exists(PUBLIC / "dataset_summary.json")
if summary:
    c1, c2, c3 = st.columns(3)
    c1.metric("Records", f"{summary.get('rows', 0):,}")
    c2.metric("Columns", summary.get("columns", "—"))
    c3.metric("Exact duplicate rows", summary.get("exact_duplicate_rows", "—"))
    st.write(f"**Event-date range:** {summary.get('event_date_min')} to {summary.get('event_date_max')}")
else:
    st.warning("Run the audit first: `python -m safety_anomaly.cli audit`.")
missing = read_csv_if_exists(PUBLIC / "missingness.csv")
if missing is not None:
    st.subheader("Missingness by column")
    st.dataframe(missing, use_container_width=True, hide_index=True)
else:
    st.caption("Missingness table will be available after running the audit command.")
st.subheader("Feature governance")
st.markdown("""- Identifiers and direct employer/location fields are excluded from modeling.
- Hospitalized, Amputation and Loss of Eye are excluded from primary model inputs because they describe outcomes.
- Repeated `ID` values are not treated as duplicate incidents; `UPA` is the inspected unique identifier.""")
