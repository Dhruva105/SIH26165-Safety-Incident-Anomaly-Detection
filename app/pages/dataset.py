import streamlit as st
from utils import PUBLIC, read_json_if_exists, read_csv_if_exists

st.markdown('<div class="eyebrow">PROJECT EVIDENCE / DATASET</div>', unsafe_allow_html=True)
st.title("Data source and coverage")
st.markdown('<div class="page-deck">The application is fitted on OSHA Severe Injury Reports. The dataset describes a defined category of reported severe injuries, not every workplace event.</div>', unsafe_allow_html=True)
summary = read_json_if_exists(PUBLIC / "dataset_summary.json")
if summary:
    c1, c2, c3 = st.columns(3)
    c1.metric("Records inspected", f"{summary.get('rows', 0):,}")
    c2.metric("Columns", summary.get("columns", "—"))
    c3.metric("Exact duplicate rows", summary.get("exact_duplicate_rows", "—"))
    st.write(f"**Event dates:** {summary.get('event_date_min')} to {summary.get('event_date_max')}")
    st.write(f"**Unique UPA values:** {summary.get('unique_upa', '—'):,}")
else:
    st.warning("Run `python -m safety_anomaly.cli audit` to regenerate the data audit.")
missing = read_csv_if_exists(PUBLIC / "missingness.csv")
if missing is not None:
    st.markdown("### Missingness by field")
    st.dataframe(missing, use_container_width=True, hide_index=True)
st.markdown(
    """### Source coverage

OSHA defines reportable severe injuries for this dataset as work-related amputations, inpatient hospitalizations or loss of an eye. The reporting requirement began on 1 January 2015. The public dataset represents incidents under federal OSHA jurisdiction and excludes incidents under OSHA-approved State Plans. It does not include work-related fatalities, all recordable injuries or near misses.

### Feature governance

The primary model excludes source record identifiers, employer name, addresses, city/state/ZIP, coordinates, inspection identifiers and injury-outcome indicators. These exclusions reduce direct identification exposure and avoid using outcomes as model inputs.
"""
)
st.markdown("[Open the official OSHA Severe Injury Reports source](https://www.osha.gov/severeinjury)")
