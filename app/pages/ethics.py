import streamlit as st

st.title("Ethics, Bias & Limitations")
st.markdown("""
### Reporting and selection bias
The source contains reported severe injuries within its collection and jurisdiction. It does not represent all workplace injuries, near-misses, unsafe acts or all employers.

### False positives
An unusual event is not necessarily harmful, preventable or indicative of negligence. Rare-but-valid cases and data-quality issues can be flagged.

### Feature and representation bias
Industry and event categories have different frequencies. Sparse categories, reporting practices, and missing fields can influence anomaly scores.

### Privacy
Public outputs omit direct record identifiers, employer names, street addresses, ZIP codes, exact coordinates and raw narratives. Record-level manual-review worksheets remain local/private.

### Responsible interpretation
Do not use model outputs to rank employers, make employment decisions, assign blame, or replace domain-expert investigation. Treat scores as exploratory signals requiring independent review.

### Evaluation limitation
Without independently verified anomaly labels, Jaccard, ARI and score correlations describe agreement between models, not correctness. Manual review is subjective and should use a predefined rubric and independent reviewers where possible.
""")
