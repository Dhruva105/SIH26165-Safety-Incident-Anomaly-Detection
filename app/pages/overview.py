import streamlit as st
from utils import PUBLIC, read_json_if_exists

st.markdown('<div class="eyebrow">PROJECT / SIH26165</div>', unsafe_allow_html=True)
st.title("From incident reports to repeatable review")
st.markdown(
    '<div class="page-deck">Worksite combines pattern grouping, unusual-case screening and historical comparisons in a human-led workflow for workplace incident review.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """### The problem being addressed

Workplace incident narratives carry information about tasks, equipment, exposures and surrounding conditions. When reports are examined one at a time, recurring configurations can be difficult to compare consistently. The project uses a public severe-injury reporting dataset to explore patterns and builds a reviewer workflow around those findings.

### What the application does

1. **Group recurring patterns:** K-Means groups incidents in a structured-text feature space.
2. **Screen unusual records:** Isolation Forest identifies records that differ from the fitted reference sample.
3. **Show historical context:** nearest-neighbour retrieval returns comparable records from the sample.
4. **Support action:** a human checklist and follow-up fields turn the result into a review record.

### What the project does not claim

It does not predict future accidents, produce a validated safety-risk score, establish causality or replace a qualified safety professional.
"""
)
summary = read_json_if_exists(PUBLIC / "dataset_summary.json")
meta = read_json_if_exists(PUBLIC / "run_metadata.json")
if summary:
    st.markdown("### Source file inspected")
    c1, c2, c3 = st.columns(3)
    c1.metric("Source records", f"{summary.get('rows', 0):,}")
    c2.metric("Columns", summary.get("columns", "—"))
    c3.metric("Event-date range", f"{summary.get('event_date_min', '—')} to {summary.get('event_date_max', '—')}")
if meta:
    st.caption(
        f"Stored IF/LOF comparison run: {meta.get('model_sample_rows', '—'):,} records · "
        f"{meta.get('feature_dimensions', '—')} feature dimensions · {meta.get('experiment_count', '—')} experiment configurations."
    )
st.markdown("### Project sequence")
st.code(
    "Incident narrative + metadata → structured/text features → K-Means pattern group → Isolation Forest screen → similar historical records → human review and follow-up",
    language="text",
)
